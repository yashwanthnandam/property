from rest_framework import serializers

from .models import Propertym

from django_filters import FilterSet, AllValuesFilter, CharFilter
from django_filters import DateTimeFilter, NumberFilter

class PropertyCreateSerializer(serializers.ModelSerializer):
    lastAccessDate = serializers.CharField()
    lCtDate = serializers.CharField()

    class Meta:
        model = Propertym
        fields = "__all__"

    def create(self, validated_data):
        landmark_details = ""
        validated_data['lastAccessDate'] = str(validated_data.get('lastAccessDate'))
        validated_data['lCtDate'] = str(validated_data.get('lCtDate'))
        for detail  in validated_data['landmarkDetails']:
            landmark_details= landmark_details+","+str(detail)
        validated_data['landmarkDetails'] = landmark_details
        return super().create(validated_data)


class PropertyListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField( required=False)
    price = serializers.SerializerMethodField(required=False)
    bedroom_num = serializers.CharField(source='bedroomD', required=False)
    bathroomNum = serializers.CharField(source='bathD', required=False)
    propertyType = serializers.CharField( required=False)
    locality = serializers.CharField( required=False)
    furnish = serializers.CharField(source='furnishedD', required=False)
    area = serializers.CharField(source='coveredArea', required=False)
    city = serializers.CharField(required=False)
    latitude = serializers.FloatField(source='pmtLat', required=False)
    longitude = serializers.FloatField(source='pmtLong', required=False)
    description = serializers.CharField(source='seoDesc', required=False)
    class Meta:
        model = Propertym
        fields = (
        'id', 'latitude', 'longitude', 'price', 'bedroom_num', 'bathroomNum', 'propertyType', 'locality', 'furnish',
        'area', 'city','transType','description','propertyTitle','floorD','catAdd1')

    def get_id(self, obj):
        return obj.id

    def get_price(self, obj):
        return 0 if obj.price == 'Price on Request' else obj.price




