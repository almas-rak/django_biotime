import json
import requests

from core import settings
from zk_services.models import ZkToken, ZkRequest


class ZkApiInteraction:

    def __init__(self):
        self.token = self.get_token()
        self.headers = {"Content-Type": "application/json",
                        "Authorization": self.token
                        }

    def get_token(self):
        token = ZkToken.objects.get_or_none()
        if token:
            return token
        else:
            return self.login_zk()

    def login_zk(self, token=None):
        login_url = f'{settings.BASE_URL_ZK}{settings.login_url}'
        headers = {"Content-Type": "application/json", }
        body = {
            "username": settings.USER_NAME_ZK,
            "password": settings.USER_PASS_ZK
        }
        response = requests.post(url=login_url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            response = response.json()
            if token:
                token.token = response.token
                token.save()
                return token
            else:
                token = ZkToken.objects.create(
                    token=response["token"]
                )
                return token
        else:
            return {
                "status_code": response.status_code,
                "description": f'{response.reason} Обратитесь к администратору'
            }

    def get_emp(self, user_pk: int):
        get_emp_url = f'{settings.BASE_URL_ZK}{settings.get_emp_url}'
        if self.token:
            params = {"page_size": 100}
            response = requests.get(url=get_emp_url, headers=self.headers, params=params)

            if response.ok:
                response = response.json()
                ZkRequest.objects.create(
                    user_pk=user_pk,
                    request=f"GET {get_emp_url}"
                    )
                return response
            else:
                self.login_zk()

    def get_report(self, ids, user):
        headers = {"Content-Type": "application/json",
                   "Authorization": ""
                   }
