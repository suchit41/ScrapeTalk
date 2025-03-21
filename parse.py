
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

# Define Prompt Template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {page_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

image_template = (
    "You are an AI image processor. Given the following image URL: {image_url}, "
    "describe its contents in detail, based on the following instruction: {page_description}. "
    "Only extract relevant details without additional commentary."
)

# Load the Groq LLM
model = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="deepseek-r1-distill-llama-70b"
)

# Function to Parse Text Content
def parse_with_Groq(dom_chunks, page_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "page_description": page_description})
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(str(response.content))  # Convert AIMessage to string
    return "\n".join(parsed_results)

# Function to Parse Images
def parse_images_with_Groq(image_urls, page_description):
    prompt = ChatPromptTemplate.from_template(image_template)
    chain = prompt | model

    image_results = {}

    for i, img_url in enumerate(image_urls, start=1):
        response = chain.invoke({"image_url": img_url, "page_description": page_description})
        print(f"Processed image: {i} of {len(image_urls)}")
        image_results[img_url] = response

    return image_results
