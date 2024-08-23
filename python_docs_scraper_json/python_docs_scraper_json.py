import requests
from bs4 import BeautifulSoup
import json
import re

# URL for the specific Python documentation page
page_url = "https://docs.python.org/3/library/functions.html"

# Fetch and parse the page
page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')

def clean_text(text):
    """Clean the input text by removing '¶' symbols and replacing newlines with spaces."""
    text = text.replace('¶', '').strip()
    return ' '.join(text.split())  # Ensure no multiple spaces

def add_spaces_around_inlines(soup):
    """Add spaces around inline elements in the parsed HTML to ensure proper spacing."""
    inline_elements = ['a', 'span', 'em', 'strong', 'code', 'b', 'i', 'u']
    for tag in soup.find_all(inline_elements):
        if tag.previous_sibling and isinstance(tag.previous_sibling, str):
            tag.insert_before(' ')
        if tag.next_sibling and isinstance(tag.next_sibling, str):
            tag.insert_after(' ')

def replace_hyperlinks(soup):
    """Replace <a> tags with markdown-style hyperlinks, handling both internal and external links."""
    for a in soup.find_all('a', href=True):
        link_text = clean_text(a.get_text(strip=True))
        href = a['href']
        if href.startswith("http"):
            markdown_link = f" ({link_text})[{href}]"
        else:
            markdown_link = f" {link_text}"  # Only text for internal links
        a.replace_with(markdown_link)

def process_dl(dl):
    """Process a <dl> tag and return a dictionary of its contents."""
    sections = {}
    current_key = None
    current_value = []

    for tag in dl.find_all(['dt', 'dd']):
        if tag.name == 'dt':
            if current_key is not None:
                sections[current_key] = " ".join(current_value).strip()
            current_key = clean_text(tag.get_text())
            current_value = []
        elif tag.name == 'dd' and current_key:
            current_value.append(clean_text(tag.get_text()))

    if current_key is not None:
        sections[current_key] = " ".join(current_value).strip()

    return sections

def scrape_page(soup):
    """Scrape the specific page for content."""
    try:
        # Add spaces around inline elements and replace hyperlinks
        add_spaces_around_inlines(soup)
        replace_hyperlinks(soup)

        sections = soup.find_all(['section', 'div'], {'id': True})
        page_data = {}

        for section in sections:
            header = section.find(['h1', 'h2', 'h3'])
            if header:
                title_text = clean_text(header.get_text())
                dl_elements = section.find_all('dl')
                if dl_elements:
                    content = {}
                    for dl in dl_elements:
                        content.update(process_dl(dl))
                    page_data[title_text] = content
                else:
                    content_text = clean_text(section.get_text().replace(title_text, '', 1).strip())
                    page_data[title_text] = content_text

        return page_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return {}

def slugify(key):
    """Convert a string into a slug."""
    key = re.sub(r'\(.*\)', '', key)  # Remove anything in parentheses
    key = re.sub(r'class ', '', key)  # Remove 'class '
    key = re.sub(r'@', '', key)       # Remove '@'
    key = re.sub(r'\.', '-', key)     # Replace periods with hyphens
    key = re.sub(r'[\s]+', '-', key)  # Replace spaces with hyphens
    key = re.sub(r'[^a-zA-Z0-9\-]', '', key)  # Remove all non-alphanumeric characters except hyphens
    return key.lower()

def convert_keys_to_slugs(data):
    """Recursively convert all keys in a dictionary to slugs."""
    if isinstance(data, dict):
        return {slugify(k): convert_keys_to_slugs(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_slugs(i) for i in data]
    else:
        return data

try:
    data = scrape_page(soup)

    # Convert keys to slugs
    data = convert_keys_to_slugs(data)

    # Save the data to a JSON file
    with open(r'C:\test\test\python_functions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Scraping completed, keys converted to slugs, and data saved to python_functions.json")

except Exception as e:
    print(f"An error occurred: {e}")
