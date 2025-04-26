import requests
from decouple import config
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from fashionShop.api.utils import get_econt_cities_data


class EcontTownsView(APIView):
    authentication_classes = []

    def get(self, request):
        query = request.GET.get('name', '')

        data = get_econt_cities_data()

        cities = [
            {
                'id': city['id'],
                'postCode': city['postCode'],
                'name': city['name'],
                'regionName': city['regionName'],
                # 'servingOffices': {of["officeCode"] for of in city['servingOffices']},
            }
            for city in data['cities']
            if city.get('name', '').lower().startswith(query.lower())
            or city.get('nameEn', '').lower().startswith(query.lower())
        ]

        return Response(data=cities, status=HTTP_200_OK)


class EcontOfficeView(APIView):
    authentication_classes = []

    def post(self, request):
        query = request.data.get('cityID', '')
        url = 'http://ee.econt.com/services/Nomenclatures/NomenclaturesService.getOffices.json'

        headers = {
            'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'ee.econt.com',
            'Upgrade-Insecure-Requests': '1',
            'username': config('ECONT_USERNAME'),
            'password': config('ECONT_PASSWORD')
        }

        params = {
            'cityID': query
        }

        response = requests.post(url, json=params)
        data = response.json()

        return Response(data=data, status=HTTP_200_OK)
