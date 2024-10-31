import requests
import csv
import urllib.error

def fetch_all_users(limit=2000):
    all_users = []
    count = 100  # Number of users to fetch per request
    from_index = 1  # Starting index for the request

    while len(all_users) < limit:
        url = f"https://codeforces.com/api/user.ratedList?activeOnly=true&from={from_index}&count={count}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            if data['status'] != 'OK':
                print(f"Error fetching data: {data['comment']}")
                break

            users = data['result']
            all_users.extend(users)

            if len(users) < count:  # Break if fewer users are returned than requested
                break

            from_index += count  # Move to the next set of results

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except urllib.error.URLError as url_err:
            print(f"URL error occurred: {url_err}")
            break
        except Exception as err:
            print(f"An error occurred: {err}")
            break

    return all_users[:limit]  # Return only the first 'limit' users

def save_to_csv(users, filename='users.csv'):
    csv_data = []
    header = ['Rank', 'Handle', 'Rating', 'Max Rating', 'Contribution']
    csv_data.append(header)

    for user in users:
        rank = user['rank']
        handle = user['handle']
        rating = user['rating']
        max_rating = user['maxRating']
        contribution = user['contribution']
        csv_data.append([rank, handle, rating, max_rating, contribution])

    # Write to CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"User data saved to {filename}")

# Usage example
if __name__ == "__main__":
    user_limit = 2000  # Number of users to fetch
    all_users = fetch_all_users(user_limit)

    if all_users:
        save_to_csv(all_users)
