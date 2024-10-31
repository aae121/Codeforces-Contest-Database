import csv
import json
import os
import time
import random
from urllib import request, error
from bs4 import BeautifulSoup
from socket import timeout
#actual users (active and non-active) count is 8,000,000 users.
# For the sake of simplicity, I have as much users as I can.
#you can test it yourself to see that'sits actually extracting 8 million users

# Define the output file path
output_file_path = r"D:\Downloads\Codeforces\user_data.csv"

# List of User-Agent headers to rotate through
headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.0.0 Safari/537.36'}
]

def fetch_user_info(username, header_index=0):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    req = request.Request(url, headers=headers_list[header_index])
    try:
        with request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data['status'] == 'OK':
                return data['result'][0]
    except error.HTTPError as e:
        if e.code == 403:
            print(f"403 Forbidden for {username}, waiting 1 minute before retrying.")
            time.sleep(60)
            new_index = (header_index + 1) % len(headers_list)
            return fetch_user_info(username, new_index)
    return None

def fetch_profile_info(username, header_index=0):
    profile_url = f"https://codeforces.com/profile/{username}"
    req = request.Request(profile_url, headers=headers_list[header_index])
    try:
        with request.urlopen(req, timeout=10) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            footer = soup.find('div', class_='_UserActivityFrame_footer')
            if footer:
                counters = footer.find_all('div', class_='_UserActivityFrame_counter')
                num_problems_solved = counters[0].find('div', class_='_UserActivityFrame_counterValue').text.split()[0]
                max_streak = counters[3].find('div', class_='_UserActivityFrame_counterValue').text.split()[0]
                return num_problems_solved, max_streak
    except error.HTTPError as e:
        if e.code == 403:
            print(f"403 Forbidden on profile page for {username}, waiting 1 minute before retrying.")
            time.sleep(60)
            new_index = (header_index + 1) % len(headers_list)
            return fetch_profile_info(username, new_index)
    return '0', '0'

def main():
    file_exists = os.path.exists(output_file_path)

    with open(output_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'First Name', 'Last Name', 'City', 'Country', 'Organization', 'Contributions', 'Registration Time (seconds)', 'Number of Friends', 'Number of Problems Solved', 'Max Streak']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        page_num = 1  # Start from the first page
        while True:
            ratings_url = f"https://codeforces.com/ratings/page/{page_num}"
            header_index = 0
            req = request.Request(ratings_url, headers=headers_list[header_index])
            try:
                with request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        html = response.read()
                        soup = BeautifulSoup(html, 'html.parser')
                        ratings_div = soup.find('div', id='pageContent', class_='content-with-sidebar')
                        if ratings_div:
                            table = ratings_div.find('div', class_='datatable ratingsDatatable').find('table')
                            if table:
                                rows = table.find_all('tr')[1:]  # Fetch all rows except the header

                                # Check if we reached the end of the pages
                                if not rows:
                                    print("No more rows found, ending pagination.")
                                    break

                                for row in rows:
                                    cells = row.find_all('td')
                                    if len(cells) > 1:
                                        username = cells[1].get_text(strip=True)
                                        print(f"Processing username: {username}")

                                        try:
                                            user_info = fetch_user_info(username)
                                            if user_info:
                                                num_problems_solved, max_streak = fetch_profile_info(username)
                                                writer.writerow({
                                                    'Username': username,
                                                    'First Name': user_info.get('firstName', 'N/A'),
                                                    'Last Name': user_info.get('lastName', 'N/A'),
                                                    'City': user_info.get('city', 'N/A'),
                                                    'Country': user_info.get('country', 'N/A'),
                                                    'Organization': user_info.get('organization', 'N/A'),
                                                    'Contributions': user_info.get('contribution', 0),
                                                    'Registration Time (seconds)': user_info.get('registrationTimeSeconds', 0),
                                                    'Number of Friends': user_info.get('friendOfCount', 0),
                                                    'Number of Problems Solved': num_problems_solved,
                                                    'Max Streak': max_streak
                                                })
                                                csvfile.flush()
                                                print(f"User {username} data written.")
                                            else:
                                                print(f"No data for {username}.")
                                        except Exception as e:
                                            print(f"Skipped {username} due to error: {e}")

            except error.HTTPError as e:
                if e.code == 403:
                    print(f"403 Forbidden on page {page_num}, waiting 1 minute before retrying.")
                    time.sleep(60)
                    continue
                else:
                    print(f"Error fetching page {page_num}: {e}")
            except Exception as e:
                print(f"Error fetching page {page_num}: {e}")

            # Wait between 1 to 2 seconds between page requests
            wait_time = random.uniform(1, 2)
            print(f"Waiting for {wait_time:.2f} seconds before the next request.")
            time.sleep(wait_time)

            page_num += 1  # Move to the next page

if __name__ == "__main__":
    main()
