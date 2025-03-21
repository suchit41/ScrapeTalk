
import streamlit as st
from scrape import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    exact_body_content,  
    scrape_images
)
from parse import parse_with_Groq, parse_images_with_Groq
from rag_chatbot import rag_chatbot_ui

def main():
    # Sidebar for navigation
    st.sidebar.title("🧠 AI Toolkit")
    app_mode = st.sidebar.selectbox(
        "Choose a tool",
        [
            "Web Scraper & Image Analyzer", 
            "RAG Chatbot"
        ]
    )

    if app_mode == "Web Scraper & Image Analyzer":
        web_scraper_ui()
    else:
        rag_chatbot_ui()

def web_scraper_ui():
    st.title("🕵️ AI Web Scraper & Image Analyzer")

    # Step 1: Input URL
    url = st.text_input("🔗 Enter Website URL")

    if st.button("🚀 Scrape Website"):
        if url:
            st.write("⏳ Scraping the website...")

            # Scrape text content
            dom_content = scrape_website(url)
            body_content = exact_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Scrape images
            images = scrape_images(dom_content, url)

            # Store in Streamlit session state
            st.session_state.dom_content = cleaned_content
            st.session_state.images = images

            st.success("✅ Scraping completed!")

            # Display extracted text
            with st.expander("📜 View Extracted Text"):
                st.text_area("Extracted Content", cleaned_content, height=300)

            # Display extracted images
            if images:
                st.subheader("🖼 Extracted Images")
                cols = st.columns(3)  # Show images in a grid
                for i, img_url in enumerate(images):
                    with cols[i % 3]:
                        st.image(img_url, caption=f"Image {i+1}", use_container_width=True)
            else:
                st.info("No images found.")

    # Step 2: Parse Text Content
    if "dom_content" in st.session_state:
        st.subheader("🧐 Extract Specific Information")
        parse_description = st.text_area("Describe what you want to parse")

        if st.button("🔍 Parse Text"):
            if parse_description:
                st.write("⏳ Parsing text content...")

                # Split DOM content & process with Groq
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_Groq(dom_chunks, parse_description)

                st.subheader("📋 Extracted Information")
                st.write(parsed_result)

    # Step 3: Parse Images from Scraped Content
    if "images" in st.session_state and st.session_state.images:
        st.subheader("📷 Describe Extracted Images")
        image_parse_description = st.text_area("Describe what details you need from images")

        if st.button("🔍 Parse Images"):
            if image_parse_description:
                st.write("⏳ Processing images with AI...")

                # Process images with Groq
                image_descriptions = parse_images_with_Groq(st.session_state.images, image_parse_description)

                st.subheader("📸 Image Descriptions")
                for img_url, description in image_descriptions.items():
                    st.image(img_url, caption=description, use_container_width=True)

if __name__ == "__main__":
    main()
