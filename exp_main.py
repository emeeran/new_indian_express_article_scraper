from bs4 import BeautifulSoup
import requests
import re

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def scrape_article(url):
    response = requests.get(url)
    response.raise_for_status()  # Simplifies HTTP status check
    soup = BeautifulSoup(response.text, 'html.parser')

    headline = soup.select_one('.arr--story--headline-h1').text.strip()
    sub_headline = soup.select_one('.p-alt').text.strip()
    date_element = soup.select_one('time.arr__timeago')
    date = date_element.text.strip() if date_element else "Date information not available"

    excluded_selectors = 'div.arr--element-container:nth-child(9) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1) > strong:nth-child(1) > ins:nth-child(1) > a:nth-child(1), .r-1dqbpge > span:nth-child(1)'
    content_elements = soup.select(f'p:not({excluded_selectors})')  # Direct exclusion using CSS selector
    content = '\n\n'.join(element.text.strip() for element in content_elements)

    markdown_content = f'''
<span style="color:red"># {headline}</span>

** {sub_headline}
    
**Date:**{date}
    
{content}
'''
    return markdown_content, headline

def main():
    url = input("Enter the URL of the article: ")
    markdown_content, headline = scrape_article(url)
    if markdown_content:
        filename = '_'.join(headline.split()[:5])
        filename = sanitize_filename(filename) or "scraped_article"
        filename += ".md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Article scraped and saved as '{filename}'.")

if __name__ == "__main__":
    main()
