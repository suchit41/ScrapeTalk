# from transformers import pipeline, CLIPProcessor, CLIPModel
# from sentence_transformers import SentenceTransformer, util
# import torch
# import requests
# from PIL import Image
# from io import BytesIO


# import asyncio
# import nest_asyncio

# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     asyncio.set_event_loop(asyncio.new_event_loop())

# nest_asyncio.apply()


# # Load models
# text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# image_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
# processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# def parse_text(text, query):
#     """Extracts relevant content from text using embeddings."""
#     text_chunks = text.split("\n")
#     text_embeddings = text_model.encode(text_chunks, convert_to_tensor=True)
#     query_embedding = text_model.encode(query, convert_to_tensor=True)

#     similarities = util.pytorch_cos_sim(query_embedding, text_embeddings)[0]
#     best_match = torch.argmax(similarities).item()

#     return text_chunks[best_match]

# def parse_images(image_urls, query):
#     """Uses CLIP to describe images based on a query."""
#     descriptions = {}

#     for img_url in image_urls:
#         response = requests.get(img_url)
#         image = Image.open(BytesIO(response.content))

#         inputs = processor(text=[query], images=image, return_tensors="pt", padding=True)
#         outputs = image_model(**inputs)
#         probs = outputs.logits_per_image.softmax(dim=1)
#         score = probs[0].max().item()

#         descriptions[img_url] = f"Relevance Score: {score:.2f}"

#     return descriptions

# def search_similar_image(uploaded_img_path, image_urls):
#     """Finds similar images using CLIP."""
#     uploaded_image = Image.open(uploaded_img_path)
#     uploaded_features = image_model.get_image_features(**processor(images=uploaded_image, return_tensors="pt"))

#     similarities = []
#     for img_url in image_urls:
#         response = requests.get(img_url)
#         image = Image.open(BytesIO(response.content))

#         features = image_model.get_image_features(**processor(images=image, return_tensors="pt"))
#         score = torch.cosine_similarity(uploaded_features, features).item()
#         similarities.append((img_url, score))

#     similarities.sort(key=lambda x: x[1], reverse=True)
#     return [img[0] for img in similarities[:3]]


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