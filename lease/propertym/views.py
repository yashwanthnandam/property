import time

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, generics
from rest_framework.response import Response
from django.db.models.aggregates import Count, Avg, Sum
from django.db.models import F, Q
from .models import Propertym
from .serializers import PropertyCreateSerializer, PropertyListSerializer
import requests
from rest_framework.exceptions import ValidationError

from .pagination import PropertyLimitOffsetPagination


from rest_framework.pagination import PageNumberPagination

class PropertyListAPIView(generics.ListAPIView):
    model = Propertym
    serializer_class = PropertyListSerializer
    queryset = Propertym.objects.all()
    pagination_class = PageNumberPagination
    page_size = 100

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by min_price if provided
        min_price = self.request.query_params.get('price_min')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        # Filter by max_price if provided
        max_price = self.request.query_params.get('price_max')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        latitude_min = self.request.query_params.get('latitude_min')
        if latitude_min:
            queryset = queryset.filter(pmtLat__gte=latitude_min)

        # Filter by min_price if provided
        bedroom_num = self.request.query_params.get('bedroom_num')
        if bedroom_num:
            queryset = queryset.filter(bedroomD__iexact=bedroom_num)

        # Filter by max_price if provided
        bathroomNum = self.request.query_params.get('bathroomNum')
        if bathroomNum:
            queryset = queryset.filter(bathD__iexact=bathroomNum)




        # Filter by transaction type
        buy = self.request.query_params.get('buy')
        rent = self.request.query_params.get('rent')
        if buy== 'true' and rent =='true':
            queryset = queryset.filter(Q(transType='Sale') | Q(transType='Rent'))
        elif buy=='true':
            queryset = queryset.filter(transType='Sale')
        elif rent=='true':
            queryset = queryset.filter(transType='Rent')


        # Filter by max_price if provided
        latitude_max = self.request.query_params.get('latitude_max')
        if latitude_max:
            queryset = queryset.filter(pmtLat__lte=latitude_max)
        longitude_min = self.request.query_params.get('longitude_min')
        if longitude_min:
            queryset = queryset.filter(pmtLong__gte=longitude_min)

        # Filter by max_price if provided
        longitude_max = self.request.query_params.get('longitude_max')
        if latitude_max:
            queryset = queryset.filter(pmtLong__lte=longitude_max)

        # Limit queryset to 100 objects
        queryset = queryset[:100]

        return queryset

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'detail': exc.detail}, status=400)
        return super().handle_exception(exc)


    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({'detail': exc.detail}, status=400)
        return super().handle_exception(exc)





class PropertyCreateAPIView(generics.CreateAPIView):

    model = Propertym
    serializer_class = PropertyListSerializer

    def get_queryset(self):
        return self.model.objects.all()

def save_property_data_view(request):
    createresponse = None
    property_type = [10002,10003,10021,10022,10020,10001,10017,10007,10018,10008,10009,10006,10012,10011,10013,10014]
    for city in range(4443, 5000):
        for type in property_type:
            for page in range(0, 100):
                url = f"https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=R&city={city}&sortBy=premiumRecent&isNRI=N&showPrimePropsinFixedSlotsSEO=N&multiLang=en&propertyType={type}&page={page}"
                response = requests.get(url)
                json_file = response.json()
                print(str(city))
                if json_file.get('resultList'):
                    for property in json_file.get('resultList'):
                        try:
                            createresponse = save_property_data_with_transaction(property)
                            if createresponse:
                                print('property with id' + str(property['encId'])+" created with status code"+ str(createresponse.status_code) )
                            else:
                                print("response is none")
                                break
                        except:
                            continue

                print(str(city)+" "+str(page))
                time.sleep(1)
                if response.status_code == 404 or (createresponse == None and page == 20) :
                    print(response.json())
                    break
                if json_file.get('resultList') == []:
                    break
            if response.status_code == 404:
                print(response.json())
                break
            if json_file.get('resultList') == []:
                break

        continue

    return HttpResponse("Property data saved successfully")

def save_property_data_with_transaction(property):
    with transaction.atomic():
        if not Propertym.objects.filter(encId=property.get('encId')):
            url = f"http://127.0.0.1:8003/m/create_property/"
            response = requests.post(url, data = property)
            if response.status_code == 400:
                print(response.json())
            return response




