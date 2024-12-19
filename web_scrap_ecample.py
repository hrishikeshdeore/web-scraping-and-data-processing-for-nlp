from bs4 import BeautifulSoup
import requests

url = "https://insights.blackcoffer.com/ai-and-ml-based-youtube-analytics-and-content-creation-tool-for-optimizing-subscriber-engagement-and-content-strategy/"

# Fetch the HTML
response = requests.get(url, timeout=20)
response.raise_for_status()

# Parse with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract title and text
title = soup.title.string
content = soup.get_text()

print(f"Title: {title}")
print(f"Content: {content}")


