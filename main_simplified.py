from bs4 import BeautifulSoup
import requests
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', "", filename)


def scrape_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    headline = soup.select_one(".arr--story--headline-h1").text.strip()
    sub_headline = soup.select_one(".p-alt").text.strip()
    date = (
        soup.select_one("time.arr__timeago").text.strip()
        if soup.select_one("time.arr__timeago")
        else "Date information not available"
    )

    content_elements = soup.select(
        "p:not(.excluded_class)"
    )  # Assuming a class can be used for exclusion
    content = "\n\n".join(element.text.strip() for element in content_elements)

    markdown_content = f"""
# {headline}

**{sub_headline}**

**Date:** {date}

{content}
"""
    return markdown_content, headline


def main():
    url = input("Enter the URL of the article: ")
    markdown_content, headline = scrape_article(url)
    if markdown_content:
        filename = (
            sanitize_filename("_".join(headline.split()[:5])) or "scraped_article"
        )
        filename += ".md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Article scraped and saved as '{filename}'.")


if __name__ == "__main__":
    main()
