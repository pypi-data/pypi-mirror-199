import json
import os
import requests


class ApifonicaClient:
    def __init__(self, apifonica_account_sid, apifonica_auth_token, apifonica_number_from):
        self.apifonica_base_url = "https://api.apifonica.com/v2/"
        self.apifonica_account_sid = apifonica_account_sid
        self.apifonica_auth_token = apifonica_auth_token
        self.apifonica_number_from = apifonica_number_from
        self.headers = {
            "content-type": "application/json; charset=iso-8859-15",
        }

    @classmethod
    def send_sms(cls, tel, text):
        if tel.strip() == "" or tel is None:
            return False

        data = {
            "from": cls.apifonica_number_from,
            "to": tel,
            "text": text,
        }
        auth = (cls.apifonica_account_sid, cls.apifonica_auth_token)

        try:
            response = requests.post(
                os.url.join(cls.apifonica_base_url, f"accounts/{cls.apifonica_account_sid}/messages"),
                data=json.dumps(data), headers=cls.headers, auth=auth
            )
        except Exception as e:
            print("Exception sending sms with data %s: %s" % (data, e))
            return False

        if not response.ok:
            print("sms api error %s for data %s" % (response.status_code, data))
            return False

        return True


    # @classmethod
    # def get_message_history(cls):
    #     https: // api.apifonica.com / v2 / accounts / {account_sid} / messages
