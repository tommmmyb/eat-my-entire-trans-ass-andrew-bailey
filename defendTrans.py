import requests
import json
import sys
import time
from faker import Faker

import address

fake = Faker()
URL = "https://ago.mo.gov/file-a-complaint/transgender-center-concerns?sf_cntrl_id=ctl00$MainContent$C001"
count = 0
while True:
    count += 1
    missouri = address.Address.generate_MO_address()

    data = {"TextFieldController_4": fake.first_name(),
            "TextFieldController_5": fake.last_name(),
            "TextFieldController_1": missouri.street_address,
            "TextFieldController_2": missouri.city,
            "DropdownListFieldController": "MO",
            "TextFieldController_6": missouri.postcode,
            "TextFieldController_0": fake.free_email(),
            "TextFieldController_3": fake.phone_number(),
            "ParagraphTextFieldController": fake.paragraph(10)}

    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json",
               "User-Agent": fake.user_agent(),
               "X-Forwarded-For": fake.ipv4(),
               "Cookie": ""}
    try:
        response = requests.post(URL, data=data_json, headers=headers)
        if not response.ok:
            print(f"Endpoint failed {response.status_code} (Trying again in 10 seconds)...")
            sys.exit(1)
        elif "already submitted" in response.text:
            print("Form already submitted, workaround required? (Trying again in 10 seconds)...")
            time.sleep(10)
        else:
            print(f"Response {count} submitted for {data['TextFieldController_5']}, {data['TextFieldController_4']}")
            time.sleep(1)
    except:
        print("An error occurred. Trying again in 10 seconds...")
        time.sleep(10)
