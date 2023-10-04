import time
import requests
from sofia.settings import env
from requests.auth import HTTPBasicAuth


class KopoKopoHandler():
    app_id = None
    app_secret = None
    auth_url = None
    stk_push_url = None
    my_request_headers = None
    access_token_expiration = None

    def __init__(self):
        """ initializing payment objects """
        self.app_id = env("KOPOKOPO_APP_ID")
        self.app_secret = env("KOPOKOPO_SECRET")
        self.auth_url = env("KOPOKOPO_BASE_URL")
        self.stk_push_url = env("KOPOKOPO_STK_API_URL")

        try:
            self.access_token = self.get_kopokopo_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed")
            else:
                self.access_token_expiration = time.time() + 3599
        except Exception as e:
            # log this errors
            print(str(e))

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(handler, *args, **kwargs):
                if (
                    handler.access_token_expiration
                    and time.time() > handler.access_token_expiration
                ):
                    token = handler.get_kopokopo_access_token()
                    handler.access_token = token
                return decorated(handler, *args, **kwargs)
            return wrapper

    def get_kopokopo_access_token(self):
        """ 
        supply the base_url,
        if all is well receive a token from kopokopo
        """
        try:
            res = requests.post(
                self.auth_url,
                auth=HTTPBasicAuth(self.app_id, self.app_secret),
                headers={"Accept": "application/json"})
            access_token = res.json()['access_token']
            self.my_request_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
        except Exception as e:
            print(str(e), "error from get access token")
            raise e
        return access_token

    @Decorators.refreshToken
    def make_stk_push(self, first_name, last_name, phone_number, email, amount, my_call_back):
        """
        supply the client information and the stk push url
        """
        request_data = {
            "payment_channel": "MPESA STK Push",
            "till_number": "K857521",
            "subscriber": {
                "first_name": f"{first_name}",
                "last_name": f"{last_name}",
                "phone_number": f"{phone_number}",
                "email": f"{email}"
            },
            "amount": {
                "currency": "KES",
                "value": f"{amount}"
            },
            "metadata": {
                "notes": "Pay Journaling",
            },
            "_links": {
                "callback_url": f"{my_call_back}",
            }
        }
        response = requests.post(
            self.stk_push_url, json=request_data, headers=self.my_request_headers)
        return response

    @Decorators.refreshToken
    def query_transaction_status(self, url):
        """ query the status of the transaction."""

        response = requests.get(url, headers=self.my_request_headers)
        response_data = response.json()
        return response_data
