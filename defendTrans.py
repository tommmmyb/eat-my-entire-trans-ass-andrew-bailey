import requests
import json
import time
from faker import Faker
import address

RequestTimeoutLength = 1  # Seconds to wait between successful requests
retryTimeoutLength = 10  # Seconds to wait after an error before retrying

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
    except ConnectionError:
        print("A connection error occurred. ")
        print("This could be a normal network error or the connection could have been blocked by the host.")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except requests.HTTPError:
        print("An HTTP error occurred.")
        print("This means the program received an invalid HTTP response from the server.")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except TimeoutError:
        print("A timeout error occurred.")
        print("This means the server waited too long to send a response.")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except requests.exceptions.RequestException:
        print("A request error occurred.")
        print("This means there was an ambiguous exception that occurred while handling the request.")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except:
        print("An unknown error occurred.")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    else:  # if there were no errors
        if not response.ok:
            print(f"Endpoint failed {response.status_code}.")
            print("Trying again in 10 seconds...")
            time.sleep(retryTimeoutLength)
        elif "already submitted" in response.text:
            print("Got 'Form already submitted' message. New workaround required?")
            print("Trying again in 10 seconds...")
            time.sleep(retryTimeoutLength)
        else:
            print(f"Response {count} submitted for {data['TextFieldController_5']}, {data['TextFieldController_4']}")
            time.sleep(RequestTimeoutLength)
