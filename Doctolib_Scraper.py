import requests
import json
import csv
from time import sleep

def fetch_doctors(max_pages=2):  
    all_doctors = []
    
    for page in range(1, max_pages + 1):
        url = f"https://www.doctolib.fr/medecin-generaliste/france-30837580-593b-424c-b9c9-3aa621a66b55?page={page}"
        headers = # Paste the headers for the URL here        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response content (first 500 characters): {response.text[:500]}")
            
            data = response.json()
            doctors = data.get('data', {}).get('doctors', [])
            
            if not doctors:
                print(f"No doctors found on page {page}. Stopping.")
                break
            
            all_doctors.extend(doctors)
            print(f"Fetched {len(doctors)} doctors from page {page}")
            
            if len(all_doctors) >= 21000:
                print(f"Reached 21,000 doctors. Stopping.")
                break
            
            sleep(1)  # Add a delay to avoid overwhelming the server
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching page {page}: {e}")
        except ValueError as e:
            print(f"Failed to parse JSON from page {page}: {e}")
    
    return all_doctors

# Fetch doctors
doctors_list = fetch_doctors()

# Export to CSV
csv_filename = 'doctors_list.csv'
csv_fields = ['name', 'speciality', 'address', 'city', 'zipcode', 'phone']

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
    writer.writeheader()
    for doctor in doctors_list:
        writer.writerow({
            'name': doctor.get('name_with_title', ''),
            'speciality': doctor.get('speciality', ''),  # Changed this line
            'address': doctor.get('address', ''),
            'city': doctor.get('city', ''),
            'zipcode': doctor.get('zipcode', ''),
            'phone': doctor.get('phone_number', '')
        })

print(f"\nTotal doctors fetched: {len(doctors_list)}")
print(f"Doctors' details exported to {csv_filename}")