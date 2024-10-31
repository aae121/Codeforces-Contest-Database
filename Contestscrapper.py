import csv
import os
import urllib.request
import json
from datetime import datetime

# Set the directory and CSV file path
directory = r"D:\Downloads\Codeforces"
csv_file_path = os.path.join(directory, "contest.csv")

# Create directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define headers to avoid HTTP 403 error
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

# Initialize list to hold submission details
submissions = []

# Loop to fetch submissions with pagination
offset = 0
count = 1000  # Number of submissions to fetch in one request

# Fetch submissions until no more submissions are available
while True:
    # Construct the API URL with offset and count
    api_url = f"https://codeforces.com/api/problemset.recentStatus?count={count}&offset={offset}"
    req = urllib.request.Request(api_url, headers=headers)

    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())

    # Check if the response is OK
    if data['status'] != 'OK':
        print("Failed to retrieve data from the API.")
        break

    # Check if there are any results returned
    if not data['result']:
        print("No more submissions to retrieve.")
        break

    # Extract necessary information from API response
    for submission in data['result']:
        # Skip submissions without a verdict
        if 'verdict' not in submission:
            continue

        who = submission['author']['members'][0]['handle']
        when = submission['creationTimeSeconds']
        time_consumed = submission.get('timeConsumedMillis', 'N/A')  # Default to 'N/A' if not present
        memory_consumed = submission.get('memoryConsumedBytes', 'N/A')  # Default to 'N/A' if not present

        # Use safe access for programming language
        language = submission.get('programmingLanguage', 'N/A')  # Default to 'N/A'
        problem_name = submission['problem']['name']
        verdict = submission['verdict']

        # Append the data as a tuple
        submissions.append((when, who, problem_name, language, verdict, time_consumed, memory_consumed))

    # Increment offset for the next batch of submissions
    offset += count

# Write to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header
    csv_writer.writerow(['When', 'Who', 'Problem', 'Lang', 'Verdict', 'Time (ms)', 'Memory (bytes)'])

    # Write the submission data
    for submission in submissions:
        # Convert submission time from seconds to a readable format
        readable_time = datetime.utcfromtimestamp(submission[0]).strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow([readable_time] + list(submission[1:]))

print(f"Data has been written to {csv_file_path}")
