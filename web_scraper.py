import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

# Resulting dictionaries
titles = defaultdict(str)
contents = defaultdict(list)

def scrape_article(url):
    """
    Scrapes the article from the given URL and extracts the main title, subtitles, 
    and their corresponding content. The results are stored in the titles and contents dictionaries.
    """
    
    # Send a request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract main title of the article
    title_tag = soup.find('h1', class_='article-title')
    title = title_tag.get_text(strip=True) if title_tag else 'No title found'
    
    titles['article_title'] = title
    
    # Extract subtitles and their contents
    i = 1
    for subtitle_tag in soup.find_all('h2'):
        subtitle = subtitle_tag.get_text(strip=True)
        content = []
        
        # Skip the "Related Articles" section
        if subtitle == "Related Articles":
            continue
        
        # Extract content until the next subtitle tag
        for sibling in subtitle_tag.find_next_siblings():
            if sibling.name == 'h2':
                break
            sibling_text = sibling.get_text(strip=True)
            if sibling_text:
                content.append(sibling_text)
        
        # Store the subtitle and its content
        titles[f'subtitle_{i}'] = subtitle
        i += 1
        contents[subtitle] = " ".join(content)

def extract_questions_and_answers(tree):
    """
    Recursively extracts all questions and answers from the decision tree sections of the article.
    """
    q_and_a = []

    for div in tree:
        question_div = div.find('div', class_='helpjuice-decision-tree-first-question') or div.find('div', class_='helpjuice-decision-tree-tab-content-inner')
        if question_div:
            question_text = question_div.get_text(strip=True)
            if "?" in question_text:
                q_and_a.append({"question": question_text, "answers": []})

            options_div = div.find('div', class_='helpjuice-decision-tree-tabs')
            if options_div:
                answers = []
                follow_ups = options_div.find_all('div', class_='helpjuice-decision-tree-tab-content')
                for follow_up in follow_ups:
                    option_element = follow_up.find_previous_sibling('div', class_='helpjuice-decision-tree-button')
                    if option_element:
                        option_text = option_element.get_text(strip=True)
                        follow_up_text = follow_up.get_text(strip=True)
                        if option_text and follow_up_text:
                            answers.append({"option": option_text, "response": follow_up_text})
                if answers:
                    q_and_a[-1]["answers"].extend(answers)

                follow_up_questions_div = options_div.find_all('div', class_='helpjuice-decision-tree-tab-content')
                follow_up_q_and_a = extract_questions_and_answers(follow_up_questions_div)
                q_and_a.extend(follow_up_q_and_a)
    
    return q_and_a

# URL of the article to scrape from the problem statement
url = "https://support.qsys.com/troubleshooting/troubleshooting-%7C-core-110f-will-not-bootrespond"

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract troubleshooting questions and answers
q_and_a = []
container = soup.find('div', class_='helpjuice-editor-content')  # All data lies in this div tag
if container:
    decision_tree_sections = container.find_all('div', class_='helpjuice-decision-tree')
    q_and_a = extract_questions_and_answers(decision_tree_sections)
else:
    print("Container not found.")

# Scrape the article for titles and contents
scrape_article(url)

# Add troubleshooting steps to the contents dictionary
contents['Troubleshooting Steps'] = q_and_a

# Combine titles and contents into a single result dictionary
result = {
    "titles": titles,
    "contents": contents
}

# Write the result to a JSON file
with open('article_data_sample_output.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)

print("Data has been saved to 'article_data_sample_output.json'.")
