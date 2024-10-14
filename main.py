import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import os
import re
from PyPDF2 import PdfMerger

# Base URL of the documentation site
BASE_URL = 'https://flet.dev'

# Set to store visited URLs to avoid duplicates
visited_urls = set()

# List to store paths of saved PDF files
pdf_files = []

async def save_page_as_pdf(url, filename):
    print(f"Saving {url} to {filename}")
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    # Settings for page format
    await page.pdf({
        'path': filename,
        'format': 'A4',
        'printBackground': True,
        'margin': {
            'top': '1cm',
            'bottom': '1cm',
            'left': '1cm',
            'right': '1cm'
        }
    })
    await browser.close()

def extract_links(html_nav):
    soup = BeautifulSoup(html_nav, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Ignore external links
        if href.startswith('http') and BASE_URL not in href:
            continue
        # Construct full URL
        full_url = href if href.startswith('http') else BASE_URL + href
        links.append(full_url)
    return links

def crawl_and_save(links):
    tasks = []
    for url in links:
        if url not in visited_urls:
            visited_urls.add(url)
            # Sanitize filename
            filename = re.sub(r'[\\/*?:"<>|]', "_", url.replace(BASE_URL, '').strip('/')) or 'index'
            filename = f"{filename}.pdf"
            filepath = os.path.join('pdf_pages', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            pdf_files.append(filepath)
            tasks.append(save_page_as_pdf(url, filepath))
    return tasks

def merge_pdfs(pdf_files, output_filename):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_filename)
    merger.close()

def main():
    # Provided HTML code of the navigation panel
    html_nav = '''[PASTE YOUR NAVIGATION HTML HERE]'''

    # Extract links from the navigation HTML
    links = extract_links(html_nav)

    # Crawl and save pages
    loop = asyncio.get_event_loop()
    tasks = crawl_and_save(links)
    loop.run_until_complete(asyncio.gather(*tasks))

    # Merge all PDF files into one
    output_pdf = 'Flet_Documentation'
    merge_pdfs(pdf_files, output_pdf)
    print(f"PDF successfully generated: {output_pdf}")

if __name__ == '__main__':
    main()