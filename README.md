# ScrapeTalk: AI-Powered Web Scraper and Chatbot

ScrapeTalk is a Streamlit-based application that combines advanced web scraping capabilities with an AI-driven chatbot. It allows users to extract information from websites, analyze images, and engage in intelligent conversations based on the scraped content.

## Features

1. **Web Scraper & Image Analyzer**
   - Scrape text content and images from any website
   - Extract and clean specific sections of web pages
   - Parse and analyze text based on user-defined criteria
   - Describe and extract information from images using AI

2. **RAG Chatbot**
   - Create a knowledge base from scraped websites or uploaded documents
   - Engage in context-aware conversations using Retrieval-Augmented Generation (RAG)
   - Support for image uploads in chat interactions for enhanced context

## Installation

1. Clone the repository:
    https://github.com/suchit41/ScrapeTalk.git

2. Install dependencies:
    pip install -r requirements.txt


3. Set up environment variables:
- Create a `.env` file in the project root
- Add the following variables:
  ```
  GROQ_API_KEY=your_groq_api_key
  GOOGLE_API_KEY=your_google_api_key
  ```

## Usage

1. Run the application:
     ```
   streamlit run main.py
     ```
3. Use the sidebar to navigate between tools:
- **Web Scraper & Image Analyzer**: Enter a URL to scrape, view extracted content, and parse specific information
- **RAG Chatbot**: Create a knowledge base and engage in AI-powered conversations

## Code Structure

- `main.py`: Main entry point for the Streamlit application
- `scrape.py`: Functions for web scraping and content processing
- `parse.py`: Functions for parsing text and images using Groq
- `rag_chatbot.py`: Implementation of the RAG chatbot

## Dependencies

- streamlit
- selenium
- beautifulsoup4
- langchain_groq
- langchain_google_genai
- langchain_community
- chromadb
- PyPDF2
- python-docx
- Pillow

## Notes

- The web scraper uses Selenium with ChromeDriver. Ensure you have the appropriate version of ChromeDriver in the project directory.
- The RAG chatbot uses Chroma for vector storage. The database is persisted in the `./chroma_db` directory.
- The application uses Groq for text parsing and Google Generative AI for embeddings.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the easy-to-use web app framework
- LangChain for the RAG implementation
- Groq and Google for their AI services
