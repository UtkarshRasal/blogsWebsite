from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

class Convert(APIView):
    def get(self, request):
        try:
            query = {'amount': request.GET.get('amount'), 'from':request.GET.get('from') , 'to':request.GET.get('to') }
            response = requests.get('http://api.frankfurter.app/latest', params=query)
            data = response.json()  

            if query['amount'] is not None:

                return Response(data={
                    'status': True,
                    'message':'Currency Converted Successfully',
                    'data':data['rates']
                }, status=status.HTTP_200_OK)
            
            return Response(data={
                    'status': True,
                    'message':'List of currency changes',
                    'data':data
                }, status=status.HTTP_200_OK)


        except:
            return Response(data={
                'status': False,
                'message':'Enter correct currency to convert',
                'data':{}
            }, status=status.HTTP_400_BAD_REQUEST)