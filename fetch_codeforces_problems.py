import requests
from bs4 import BeautifulSoup

# Fetch the problem set page
url = 'https://codeforces.com/problemset'
res = requests.get(url)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, 'html.parser')

# Find all problems listed on the page
problems = parsedData.find_all('div', class_='problemindexholder')  # Adjust the class based on inspection

# Extract problem details
for problem in problems:
    # Extract problem name
    problem_name = problem.find('a').text.strip()  # Assuming name is in <a> tag inside each problem
    print(f"Problem Name: {problem_name}")

    # Extract problem tags
    tags = problem.find_all('span', class_='tag-box')  # Assuming tags are in <span> tags with class "tag-box"
    tag_list = [tag.text.strip() for tag in tags]
    print(f"Tags: {tag_list}")

    # If there are other details (e.g., time limit, memory limit), add code to extract those here
