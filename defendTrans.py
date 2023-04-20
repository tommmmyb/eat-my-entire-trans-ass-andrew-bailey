import requests
import json
import sys
import time
from faker import Faker

import address
import phone


DEBUG = False
URL = "https://ago.mo.gov/file-a-complaint/transgender-center-concerns?sf_cntrl_id=ctl00$MainContent$C001"

fake = Faker()

while True:
    addy = address.Address.generate_address()
    phone_str = phone.Phone.generate_phone(addy).randomize_format()

    data = {"TextFieldController_4": fake.first_name(),
            "TextFieldController_5": fake.last_name(),
            "TextFieldController_1": addy.street_address,
            "TextFieldController_2": addy.city,
            "DropdownListFieldController": "MO",
            "TextFieldController_6": addy.postcode,
            "TextFieldController_0": fake.free_email(),
            "TextFieldController_3": phone_str,
            "ParagraphTextFieldController": fake.paragraph(10)}

    if DEBUG: print(f"Attempting to submit {list(data.values())[:-1]}...")

    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json",
               "User-Agent": fake.user_agent(),
               "X-Forwarded-For": fake.ipv4(),
               "Cookie": ""}

    response = requests.post(URL, data=data_json, headers=headers)
    if not response.ok:
        print(f"Endpoint failed {response.status_code}")
        sys.exit(1)
    elif "already submitted" in response.text:
        print("Form already submitted, workaround required")
        sys.exit(1)

    print(f"Response submitted for {data['TextFieldController_5']}, {data['TextFieldController_4']}")

    time.sleep(1)
