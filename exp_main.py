import requests
from bs4 import BeautifulSoup
import re

# URL of the web page
url = "https://www.newindianexpress.com/nation/2024/Mar/29/bjp-financially-strangulating-oppn-parties-during-polls-time-congress-gets-fresh-it-notice-of-about-rs-1700-crore"

# Make a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text from the header <h1></h1> tag
    section_content = soup.find('div', {'id': 'section', 'class': 'ie_single_story_container', 'data-env': 'production'})
    h1_content = section_content.find('h1').text.strip()

    pcl_full_content = soup.find('div', {'id': 'pcl-full-content', 'class': 'story_details'})

    # Check if sub_header <h2></h2> tags are found before accessing its text attribute
    h2_element = pcl_full_content.find('h2')
    h2_content = h2_element.text.strip() if h2_element else ""

    # Find all <p></p> tags and extract their text content
    p_elements = pcl_full_content.find_all('p')
    p_contents = [p.text.strip() for p in p_elements]

    # Create a valid filename by replacing invalid characters with underscores
    valid_filename = re.sub(r'[/:*?"<>|]', '_', h1_content.lower()) + '.md'

    # Save as Markdown file with the valid filename
    with open(valid_filename, 'w', encoding='utf-8') as file:
        file.write(f"# {h1_content}\n\n## {h2_content}\n\n")
        for p_content in p_contents:
            file.write(f"{p_content}\n\n")

    print(f"Content saved to {valid_filename}")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
