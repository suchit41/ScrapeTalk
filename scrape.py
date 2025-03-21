# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import time

# import asyncio
# import nest_asyncio

# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     asyncio.set_event_loop(asyncio.new_event_loop())

# nest_asyncio.apply()



# def scrape_website(website):
#     print("Launching the Web Scraper")

#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = webdriver.Chrome(service=Service("./chromedriver"), options=options)

#     try:
#         driver.get(website)
#         time.sleep(5)  # Wait for the page to fully load
#         html = driver.page_source
#         return html
#     finally:
#         driver.quit()

# def extract_body_content(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     return str(soup.body) if soup.body else ""

# def clean_body_content(body_content):
#     soup = BeautifulSoup(body_content, "html.parser")
#     for script in soup(["script", "style"]):
#         script.extract()
#     clean_text = soup.get_text(separator="\n")
#     return "\n".join(line.strip() for line in clean_text.splitlines() if line.strip())


# def split_dom_content(dom_content, max_length=6000):
#     """Splits long text content into smaller chunks."""
#     return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]


# def scrape_images(html_content, base_url):
#     soup = BeautifulSoup(html_content, "html.parser")
#     image_urls = [urljoin(base_url, img["src"]) for img in soup.find_all("img") if img.get("src")]
#     return image_urls


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(website):
    print("Launching the Web Scraper")

    # Set the path to the ChromeDriver
    chrome_driver_path = "./chromedriver"  # Ensure you have chromedriver in this location

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode (remove if you want a visible browser)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up the ChromeDriver service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(website)
        print("Page loading....")
        time.sleep(10)  # Wait for the page to fully load
        html = driver.page_source  # Get the page source
        return html
    finally:
        driver.quit()
        print("Driver quit")

def exact_body_content(html_content):
    """Extracts the body content from the HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    """Removes scripts and styles, and extracts cleaned text."""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract text and clean it
    clean_text = soup.get_text(separator="\n")
    clean_content = "\n".join(line.strip() for line in clean_text.splitlines() if line.strip())
    return clean_content

def split_dom_content(dom_content, max_length=6000):
    """Splits long text content into smaller chunks."""
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]

def scrape_images(html_content, base_url):
    """Extracts all image URLs from the webpage."""
    soup = BeautifulSoup(html_content, "html.parser")
    image_urls = []

    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url:
            full_url = urljoin(base_url, img_url)  # Ensure absolute URL
            image_urls.append(full_url)

    return image_urls