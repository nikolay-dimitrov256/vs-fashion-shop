import requests
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from fashionShop.common.globals import SPEEDY_API_URL
from fashionShop.settings import SPEEDY_USERNAME, SPEEDY_PASSWORD


class SpeedyTownsView(APIView):
    authentication_classes = []

    def post(self, request):
        query = request.data.get('name', '')

        url = f'{SPEEDY_API_URL}/location/site'
        headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        }
        params = {
            'userName': SPEEDY_USERNAME,
            'password': SPEEDY_PASSWORD,
            'language': 'BG',
            'countryId': '100',  # Bulgaria
            'name': query,
        }

        response = requests.post(
            url=url,
            headers=headers,
            json=params,
        )

        data = response.json()

        return Response(data=data, status=HTTP_200_OK)


class SpeedyOfficeView(APIView):
    authentication_classes = []

    def post(self, request):
        query = request.data.get('siteId', '')

        url = f'{SPEEDY_API_URL}/location/office'
        headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        }
        params = {
            'userName': SPEEDY_USERNAME,
            'password': SPEEDY_PASSWORD,
            'language': 'BG',
            'countryId': '100',  # Bulgaria
            'siteId': query,
        }

        response = requests.post(
            url=url,
            headers=headers,
            json=params,
        )

        data = response.json()

        return Response(data=data, status=HTTP_200_OK)
