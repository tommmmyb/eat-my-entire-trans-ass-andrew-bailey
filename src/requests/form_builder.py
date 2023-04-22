import requests
import random
from faker import Faker
from requests_toolbelt.multipart.encoder import MultipartEncoder

from src.captcha import fuck_missouri
from src.generators import address, phone


class Form:
    def __init__(self):
        self.url = None
        self.params = None
        self.multipart_data = None
        self.parsed_form_data = None
        self.headers = None
        self.form_data = None
        self.faker = Faker()

    def send_request(self):
        self._build_form()
        self._solve_captcha()
        self._build_headers()
        return requests.post(url=self.url,
                             params=self.params,
                             headers=self.headers,
                             data=self.parsed_form_data
                             )
    
    def _solve_captcha(self):
        captcha_resp = fuck_missouri.generate_captcha_token()
        self.form_data.update(captcha_resp)
        self.multipart_data = MultipartEncoder(fields=self.form_data)
        self.parsed_form_data = self.multipart_data.to_string().decode()
        return self

    def _build_headers(self):
        self.headers = {
            'Content-Type': self.multipart_data.content_type,
            'User-Agent': self.faker.user_agent(),
            'X-Forwarded-For': self.faker.ipv4()
        }


class TransForm(Form):
    def __init__(self, url, params):
        super().__init__()
        self.has_captcha = True
        self.url = url
        self.params = params

    def _build_form(self):
        addy = address.Address.generate_address()
        phone_number = phone.Phone.generate_phone(addy).randomize_format()
        self.form_data = {"TextFieldController_4": self.faker.first_name(),
                          "TextFieldController_5": self.faker.last_name(),
                          "TextFieldController_1": addy.street_address,
                          "TextFieldController_2": addy.city,
                          "DropdownListFieldController": "MO",
                          "TextFieldController_6": addy.postcode,
                          "TextFieldController_0": self.faker.free_email(),
                          "TextFieldController_3": phone_number,
                          "ParagraphTextFieldController": self.faker.paragraph(10)}
        return self


class UndocWorkerForm(Form):
    def __init__(self, url, params):
        super().__init__()
        self.has_captcha = False
        self.url = url
        self.params = params

    def _build_form(self):
        addy = address.Address.generate_address()
        business_addy = address.Address.generate_address()
        phone_number = phone.Phone.generate_phone(addy).randomize_format()
        business_phone = phone.Phone.generate_phone(business_addy).randomize_format()
        self.form_data = {"TextFieldController_4": self.faker.first_name(),
                          "TextFieldController_5": self.faker.last_name(),
                          "TextFieldController_20": addy.street_address,
                          "TextFieldController_9": addy.city,
                        #   "TextFieldController_8": "MO",   # Form Auto-Fills "MO" for state
                          "TextFieldController_11": addy.postcode,
                          "TextFieldController_14": self.faker.free_email(),
                          "TextFieldController_21": phone_number,
                          "MultipleChoiceFieldController": "I am a state resident.",
                          "TextFieldController_18": self.faker.company(),
                          "TextFieldController_15": business_addy.street_address,
                          "TextFieldController_13": business_addy.city,
                          "TextFieldController_7": business_addy.postcode,
                          "TextFieldController_19": business_phone,
                          "TextFieldController_16": self.faker.name(),
                          "ParagraphTextFieldController": self.faker.paragraph(10),
                          "TextFieldController": f"{self.faker.month_name()} {random.randint(2010, 2023)}"}
        return self