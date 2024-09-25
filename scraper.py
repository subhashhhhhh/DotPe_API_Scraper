import requests
import json
import csv
import time
import random

base_url = "https://api.dotpe.in/api/merchant/external/store/"
service_subtype = "?serviceSubtype=fine"
start_id = 1  # Adjust if needed

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    # ... add more User-Agent strings
]

# If you have proxies, uncomment and configure the following lines
# proxies = {
#     'http': 'http://your_proxy_server:port',
#     'https': 'https://your_proxy_server:port'
# }

with open('restaurants1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Store ID', 'Restaurant Name', 'Description', 'Address', 'City', 'State'] 
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for store_id in range(start_id, 9999):
        url = base_url + str(store_id) + service_subtype

        headers = {
            'User-Agent': random.choice(user_agents)
        }

        try:
            # If using proxies, uncomment the following line
            # response = requests.get(url, headers=headers, proxies=proxies)
            response = requests.get(url, headers=headers)  # Without proxies
            response.raise_for_status()

            data = json.loads(response.text)

            if data['status'] and 'store' in data:
                store_data = data['store']

                try:
                    restaurant_name = store_data['storeName']
                    description = store_data['description']

                    # Handle potential missing address fields
                    address1 = store_data.get('address1', '') 
                    address2 = store_data.get('address2', '')
                    address = address1 + ", " + address2 if address2 else address1

                    city = store_data['city']
                    state = store_data['state']

                    writer.writerow({
                        'Store ID': store_id, 
                        'Restaurant Name': restaurant_name, 
                        'Description': description,
                        'Address': address,
                        'City': city,
                        'State': state
                    })

                except KeyError as e:
                    print(f"Missing key in store data for ID {store_id}: {e}")
            else:
                print(f"No store data found for ID {store_id}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for store ID {store_id}: {e}")

        # Introduce a random delay
        time.sleep(random.uniform(0.5, 2))
