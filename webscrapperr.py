import csv
import urllib.request
import json
from bs4 import BeautifulSoup
import os
import time

# Define URLs
api_url = "https://codeforces.com/api/problemset.problems"
output_csv = r"D:\Downloads\Codeforces\problems_data_new.csv"

# Define headers for urllib to avoid request denial
headers = {'User-Agent': 'Mozilla/5.0'}


# Function to fetch JSON data from Codeforces API
def fetch_problems_data():
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
        return json.loads(data)


# Function to fetch HTML page of a specific problem
def fetch_problem_html(contest_id, index):
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        return html


# Function to parse problem HTML and extract required details
def parse_problem_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting time limit without "seconds"
    time_limit_div = soup.find("div", class_="time-limit")
    time_limit = time_limit_div.get_text(strip=True).replace("time limit per test", "").replace("seconds",
                                                                                                "").strip() if time_limit_div else "N/A"

    # Extracting memory limit without "megabytes"
    memory_limit_div = soup.find("div", class_="memory-limit")
    memory_limit = memory_limit_div.get_text(strip=True).replace("memory limit per test", "").replace("megabytes",
                                                                                                      "").strip() if memory_limit_div else "N/A"

    # Extracting only the problem description text
    description_div = soup.find("div", class_="problem-statement")
    if description_div:
        # Remove headers, titles, and unnecessary text from the description
        for header in description_div.find_all(["h1", "h2", "h3", "div"], class_="title"):
            header.decompose()  # Remove header elements
        description = description_div.get_text(" ", strip=True)
    else:
        description = "N/A"

    return time_limit, memory_limit, description


# Main function to fetch data and write to CSV
def main():
    # Load problem data from Codeforces API
    problems_data = fetch_problems_data()

    # Check if the CSV file already exists
    file_exists = os.path.exists(output_csv)

    # Open the CSV for appending new entries
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header if the file is empty or does not exist
        if not file_exists or os.stat(output_csv).st_size == 0:
            writer.writerow(
                ["Name", "Problem ID", "Tags", "Time Limit (seconds)", "Memory Limit (megabytes)", "Description",
                 "Input Specification", "Output Specification"])

        # Process only the first 3,000 problems
        for i, problem in enumerate(problems_data["result"]["problems"]):
            if i >= 3000:  # Stop after 3000 problems
                break

            # Get basic details
            contest_id = problem.get("contestId")
            index = problem.get("index")
            name = problem.get("name")
            tags = ", ".join(problem.get("tags", []))
            problem_id = f"{contest_id}{index}"

            # Fetch and parse problem page for additional details
            html = fetch_problem_html(contest_id, index)
            time_limit, memory_limit, description = parse_problem_html(html)

            # Write to CSV
            writer.writerow([name, problem_id, tags, time_limit, memory_limit, description, "N/A", "N/A"])

            # Optional delay to avoid overwhelming the server; can be adjusted or removed if necessary
            time.sleep(1)


if __name__ == "__main__":
    main()
