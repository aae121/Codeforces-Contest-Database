from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import time
import csv

# Set up Edge WebDriver
edge_driver_path = r"D:\Downloads\edgedriver_win64\msedgedriver.exe"  # Use a raw string for the path
service = Service(edge_driver_path)
options = webdriver.EdgeOptions()

# Uncomment the next line to run Edge in headless mode
# options.add_argument("headless")

# Initialize the WebDriver
driver = webdriver.Edge(service=service, options=options)

def get_contest_writers_from_web():
    # URL for the Codeforces contests page
    url = "https://codeforces.com/contests"
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(3)

    # Retrieve page content
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    # Locate the contest table rows
    contest_rows = soup.select('table tr[data-contestid]')

    # Prepare CSV file for writing
    with open("writers_contests.csv", mode="w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)  # Use a different name for the CSV writer
        csv_writer.writerow(["Contest Name", "Writers", "Start Time", "Duration"])  # Header row

        # List to store all writers
        all_writers = []

        for row in contest_rows:
            columns = row.find_all('td')

            # Extract relevant data from each column if available
            if len(columns) >= 4:
                contest_name = columns[0].get_text(strip=True)
                writers = columns[1].get_text(strip=True)
                start_time = columns[2].get_text(strip=True)
                duration = columns[3].get_text(strip=True)

                # Check if the contest is Div. 1 or Div. 2
                if "Div. 1" in contest_name or "Div. 2" in contest_name:
                    # Write row data to CSV
                    csv_writer.writerow([contest_name, writers, start_time, duration])  # Use the correct writer
                    print(
                        f"Contest Name: {contest_name}, Writers: {writers}, Start Time: {start_time}, Duration: {duration}")

                    # Add all writers to the list
                    if writers:
                        # Split by comma and strip whitespace to get individual writers
                        all_writers.extend(writer.strip() for writer in writers.split(','))
                else:
                    print(f"Skipped contest: {contest_name} (not Div. 1 or Div. 2)")
            else:
                print("Row does not contain the expected number of columns.")

    # Output all writers
    print(f"Total writers collected: {len(all_writers)}")
    for writer in all_writers:
        print(writer)

# Run the function
get_contest_writers_from_web()

# Close the WebDriver after scraping
driver.quit()
