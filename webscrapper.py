import csv
import time
import urllib.request
import json
from bs4 import BeautifulSoup
import os

# Define URLs
api_url = "https://codeforces.com/api/problemset.problems"
output_csv = r"D:\Downloads\Codeforces\problems_data.csv"

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

    # Extracting time limit
    time_limit_div = soup.find("div", class_="time-limit")
    time_limit = time_limit_div.get_text(strip=True).replace("time limit per test", "").replace("seconds", "").strip() if time_limit_div else "N/A"

    # Extracting memory limit
    memory_limit_div = soup.find("div", class_="memory-limit")
    memory_limit = memory_limit_div.get_text(strip=True).replace("memory limit per test", "").replace("megabytes", "").strip() if memory_limit_div else "N/A"

    # Extracting problem description text
    description_div = soup.find("div", class_="problem-statement")
    description = ""
    if description_div:
        paragraphs = description_div.find_all("p")
        description = "\n".join([p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)])

    # Extracting input specification
    input_spec_div = soup.find("div", class_="input-specification")
    input_spec = ""
    if input_spec_div:
        input_paragraphs = input_spec_div.find_all("p")
        input_spec = "\n".join([p.get_text(" ", strip=True) for p in input_paragraphs if p.get_text(strip=True)])

    # Extracting output specification
    output_spec_div = soup.find("div", class_="output-specification")
    output_spec = ""
    if output_spec_div:
        output_paragraphs = output_spec_div.find_all("p")
        output_spec = "\n".join([p.get_text(" ", strip=True) for p in output_paragraphs if p.get_text(strip=True)])

    return time_limit, memory_limit, description, input_spec, output_spec

# Main function to fetch data and write to CSV
def main():
    # Load problem data from Codeforces API
    problems_data = fetch_problems_data()

    # Check for existing CSV data
    existing_data = set()
    if os.path.exists(output_csv):
        with open(output_csv, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                existing_data.add(row[1])  # Add problem_id to the set

    # Open the CSV for appending new entries
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header if the file is empty
        if not existing_data:
            writer.writerow(["Name", "Problem ID", "Tags", "Time Limit (seconds)", "Memory Limit (megabytes)", "Description", "Input Specification", "Output Specification"])

        # Calculate total execution time
        total_time_seconds = 15  # Changed to 15 seconds for this run
        total_time_minutes = total_time_seconds / 60
        print(f"Total estimated execution time: approximately {total_time_minutes:.1f} minutes.")

        # Ask for user confirmation
        proceed = input("Do you want to proceed with the scraping? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Scraping aborted.")
            return

        # Process each problem (up to a total of 100 problems for this example)
        problem_count = 0
        for problem in problems_data["result"]["problems"]:
            if problem_count >= 100:  # Limit to 100 problems
                break

            # Get basic details
            contest_id = problem.get("contestId")
            index = problem.get("index")
            name = problem.get("name")
            tags = ", ".join(problem.get("tags", []))
            problem_id = f"{contest_id}{index}"

            # Skip if problem already exists in the CSV
            if problem_id in existing_data:
                continue

            # Fetch and parse problem page for additional details
            html = fetch_problem_html(contest_id, index)
            time_limit, memory_limit, description, input_spec, output_spec = parse_problem_html(html)

            # Output full specifications to terminal
            print(f"Input Specification:\n{input_spec}\n")
            print(f"Output Specification:\n{output_spec}\n")

            # Write to CSV
            writer.writerow([name, problem_id, tags, time_limit, memory_limit, description, input_spec, output_spec])

            problem_count += 1

            # Delay to avoid blocking
            time.sleep(1)  # Adjust if needed

if __name__ == "__main__":
    main()
