import streamlit as st
import os
import chardet
import PyPDF2
import docx
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PIL import Image

# Import scraping functions
from scrape import scrape_website, clean_body_content, exact_body_content

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class RAGChatbot:
    def __init__(self, model_name="deepseek-r1-distill-llama-70b"):
        self.llm = ChatGroq(
            groq_api_key=os.getenv('GROQ_API_KEY'),
            model_name=model_name
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.persist_directory = "./chroma_db"
        self.vectorstore = None

    def create_vector_store_from_text(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_text(documents)
        self.vectorstore = Chroma.from_texts(texts=splits, embedding=self.embeddings, persist_directory=self.persist_directory)
        return self.vectorstore

    def create_vector_store_from_url(self, url):
        try:
            dom_content = scrape_website(url)
            body_content = exact_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)
            return self.create_vector_store_from_text(cleaned_content)
        except Exception as e:
            st.error(f"Error scraping URL: {e}")
            return None

    def retrieve_relevant_context(self, query, k=3):
        if not self.vectorstore:
            return ""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        relevant_docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in relevant_docs])

    def generate_response(self, query, context, image=None):
        template = """
        You are a helpful AI assistant. Use the following context to answer the query:

        Context:
        {context}

        Query: {query}

        If an image is provided, describe its contents and integrate the visual information into the response.

        If the context doesn't contain relevant information, respond based on your general knowledge.
        Provide a clear, concise, and helpful response.
        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm

        query_data = {"context": context, "query": query}
        if image:
            query_data["image"] = image  # If using a model that supports images

        response = chain.invoke(query_data)
        return response.content

def rag_chatbot_ui():
    st.title("🤖 AI Chatbot with Image & Text Input")

    if 'rag_chatbot' not in st.session_state:
        st.session_state.rag_chatbot = RAGChatbot()
        st.session_state.chat_history = []
        st.session_state.knowledge_source = None

    # Sidebar for Knowledge Base
    with st.sidebar:
        st.subheader("📚 Create Knowledge Base")
        source_type = st.radio("Choose Knowledge Source", ["Text Upload", "Web URL"])

        if source_type == "Text Upload":
            uploaded_file = st.file_uploader("Upload a document", type=['txt', 'pdf', 'docx'])
            if uploaded_file:
                document_content = uploaded_file.read().decode('utf-8')
                st.session_state.rag_chatbot.create_vector_store_from_text(document_content)
                st.session_state.knowledge_source = f"Uploaded File: {uploaded_file.name}"
                st.success("Knowledge base created successfully!")

        else:
            url = st.text_input("🔗 Enter Website URL")
            if st.button("🚀 Scrape and Embed URL") and url:
                st.write("⏳ Scraping website...")
                vectorstore = st.session_state.rag_chatbot.create_vector_store_from_url(url)
                if vectorstore:
                    st.session_state.knowledge_source = f"Web URL: {url}"
                    st.success("Website content embedded successfully!")

        if st.session_state.knowledge_source:
            st.info(f"Current Knowledge Source: {st.session_state.knowledge_source}")

    # Chat Interface
    st.subheader("💬 Chat")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "image" in message and message["image"]:
                st.image(message["image"], caption="User uploaded image", use_column_width=True)

    # User Input with Image Upload
    col1, col2 = st.columns([3, 1])
    with col1:
        prompt = st.text_input("Type your message...")

    with col2:
        image_file = st.file_uploader("📷", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    # Handle User Query
    if st.button("Send"):
        if not prompt and not image_file:
            st.warning("Please enter a message or upload an image!")
            return
        
        if not st.session_state.rag_chatbot.vectorstore:
            st.warning("Please create a knowledge base first!")
            return

        # Store user message
        user_message = {"role": "user", "content": prompt}
        if image_file:
            image = Image.open(image_file)
            user_message["image"] = image
            st.image(image, caption="User uploaded image", use_column_width=True)

        st.session_state.chat_history.append(user_message)

        # Retrieve context
        context = st.session_state.rag_chatbot.retrieve_relevant_context(prompt)

        # Generate response
        response_text = st.session_state.rag_chatbot.generate_response(prompt, context, image_file)

        # Store AI response
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response_text)

    # Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

if __name__ == "__main__":
    rag_chatbot_ui()
