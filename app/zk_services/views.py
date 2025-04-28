import json
import requests
import urllib.parse

from core import settings
from zk_services.models import ZkToken, ZkRequest


class ZkApiInteraction:

    def __init__(self):
        self.token = self.get_token()
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Token {self.token.token}"
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
                token.token = response["token"]
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

    def refresh_token(self):
        url = f"{settings.BASE_URL_ZK}/base/api/user_notifications/total/"
        params = {"status": 0}
        response = requests.get(url=url, headers=self.headers, params=params)
        if response.ok:
            return
        else:
            self.token = self.login_zk(token=self.token)
            return

    def record_in_db(self, request, user):
        ZkRequest.objects.create(
            user_pk=user,
            request=urllib.parse.unquote(request.url),
            method=request.request.method,
            status_code=request.status_code
        )

    def make_get_request(self, url, params=None, user=None):
        response = requests.get(url=url, headers=self.headers, params=params)
        if user:
            self.record_in_db(request=response, user=user)
        if response.ok:
            return response.json()
        else:
            return {
                "status_code": response.status_code,
                "description": f'{response.reason} Обратитесь к администратору'
            }

    def get_emp(self, user):
        url = f'{settings.BASE_URL_ZK}{settings.get_emp_url}'
        params = {"page_size": 100}
        return self.make_get_request(url, params=params, user=user)

    def get_monthly_status_report(self, params, user):
        url = f'{settings.BASE_URL_ZK}{settings.monthly_status_report_url}'
        return self.make_get_request(url, params=params, user=user)

    def get_monthly_punch_report(self, params, user):
        url = f'{settings.BASE_URL_ZK}{settings.monthly_punch_report_url}'
        return self.make_get_request(url, params=params, user=user)

    def emp_search(self, params, user):
        url = f'{settings.BASE_URL_ZK}{settings.life_search_url}'
        return self.make_get_request(url, params=params, user=user)

    def get_holidays(self, user):
        url = f'{settings.BASE_URL_ZK}{settings.holidays_url}'
        return self.make_get_request(url, user=user)
