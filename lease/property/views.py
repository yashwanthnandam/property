from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render
from rest_framework import status

# Create your views here.
from requests import Response

from .functions import Map
from .models import \
    (
    MapDetails, FSLData,\
    Property, Profile,
    MetaData, Location,
    SuperProfile,
    Formatted, FormattedLandmarkDetails

)
from django.http import HttpResponse, HttpRequest
import time
import requests

from django.shortcuts import render
from django.http import JsonResponse
from .models import Property

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Property, MapDetails

from django.http import JsonResponse

from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator



def get_properties(request):
    properties = Property.objects.all()
    maps = MapDetails.objects.all()
    formatted = Formatted.objects.all()
    id = request.GET.get('id')
    city = request.GET.get('city')
    latitude_min = request.GET.get('latitude_min')
    latitude_max = request.GET.get('latitude_max')
    longitude_min = request.GET.get('longitude_min')
    longitude_max = request.GET.get('longitude_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    bedroom_num = request.GET.get('bedroom_num')
    property_type = request.GET.get('property_type')
    locality = request.GET.get('locality')
    furnish = request.GET.get('furnish')
    area = request.GET.get('area')
    page_size = request.GET.get('page_size')
    page_number = request.GET.get('page_number')
    bathroomNum = request.GET.get('bathroomNum')

    if city:
        properties = properties.filter(city__iexact=city)
    if latitude_min and latitude_max and latitude_max!='false' and latitude_max != 'false':
        maps = maps.filter(latitude__range=(latitude_min, latitude_max))
    if longitude_min and longitude_max  and longitude_min!='false' and longitude_max!='false':
        maps = maps.filter(longitude__range=(longitude_min, longitude_max))
    if price_min:
        formatted = formatted.filter(avg_price__gte=price_min)
    if price_max:
        formatted = formatted.filter(avg_price__lte=price_max)
    if bedroom_num:
        properties = properties.filter(bedroomNum__iexact=bedroom_num)
    if property_type:
        properties = properties.filter(propertyType__iexact=property_type)
    if locality:
        properties = properties.filter(locality__iexact=locality)
    if furnish:
        properties = properties.filter(furnish__iexact=furnish)
    if area:
        properties = properties.filter(area__iexact=area)
    if id:
        properties = properties.filter(id__iexact=id)
    if bathroomNum:
        properties = properties.filter(bathroomNum__iexact=bathroomNum)

    properties = properties.filter(mapDetails__in=maps, formatted__in=formatted)
    properties = properties.distinct()

    paginator = Paginator(properties, 10 if not page_size else page_size)
    page = request.GET.get('page_number')
    properties = paginator.get_page(page if page else 1)

    data = [
        {
        'id': property.id,
        'price': 0 if property.price =='Price on Request' else property.price,
        'bedroomNum': property.bedroomNum,
        'bathroomNum':property.bathroomNum,
        'propertyType': property.propertyType,
        'locality': property.locality,
        'furnish': property.furnish,
        'area': property.area,
        'city': property.city,
        'latitude': property.mapDetails.latitude,
        'longitude': property.mapDetails.longitude

        } for property in properties]
    print('api called')
    return JsonResponse({'properties': data,"no_of_properties":len(properties)})


def get_properties(request):
    price_min = request.GET.get('price_min','')
    price_max = request.GET.get('price_max','')
    page_size = request.GET.get('page_size')
    latitude_min =  request.GET.get('latitude_min','')  # Add code to define the latitude_min variable
    latitude_max =  request.GET.get('latitude_max','')  # Add code to define the latitude_max variable
    longitude_min =  request.GET.get('longitude_min','')  # Add code to define the longitude_min variable
    longitude_max =  request.GET.get('longitude_max','')
    buy = request.GET.get('buy', '')  # Add code to define the longitude_min variable
    rent = request.GET.get('rent', '')
    bathroomNum = request.GET.get('bathroomNum')
    bedroom_num = request.GET.get('bedroom_num')
    # Add code to define the longitude_max variable
    city = 1
    furnish = None  # Add code to define the furnish variable
    # endpoint = f"http://127.0.0.1:8003/get_properties/?price_min={price_min}&price_max={price_max}&page_size={page_size}&latitude_min={latitude_min}&latitude_max={latitude_max}&longitude_min={longitude_min}&longitude_max={longitude_max}&furnish={furnish}&cityId={city}"
    endpointm = f"http://127.0.0.1:8003/m/get_properties/?price_min={price_min}&price_max={price_max}&page_size={page_size}&latitude_min={latitude_min}&latitude_max={latitude_max}&longitude_min={longitude_min}&longitude_max={longitude_max}&furnish={furnish}&cityId={city}&buy={buy}&rent={rent}&bedroom_num={bedroom_num}&bathroomNum={bathroomNum}"

    # properties = requests.get(endpoint)
    propertiesm = requests.get(endpointm)
    # properties = properties['properties']+propertiesm['properties']


    # properties = Property.objects.select_related('mapDetails').values_list('mapDetails__latitude',

    return JsonResponse({"properties":propertiesm.json()})



def get_map_view(request):

    key = "AIzaSyCqCO4OFri0-do9lW15udLNC_Bh-KbkW0I"
    properties = get_properties(request)
    # Initialize a dictionary to store the properties data
    properties_data = []

    # Loop through the properties and store the data in the dictionary
    for index, property in enumerate(properties.json()['results']):
        map = Map()
        # boundaries = map.get_polygon(property['map_details']['latitude'],property['map_details']['longitude'])
        if not property['bedroomNum'] :
            property['bedroomNum'] = 0
        properties_data.append({
            'lat': property['latitude'],
            'lng': property['longitude'],
            'price': property['price'],
            'id': property['id'],
            'bathroomNum':property['bathroomNum'],
            'bedroomNum':property['bedroomNum'],
            'area':property['area'],
            'city':property.get('city',''),
            'locality':property.get('locality',''),
            'furnish':property['furnish'],
            'property_type':property.get('propertyType',''),
            # 'boundaries': boundaries,
        })

    return render(request, "real_estate_map.html",
                  {'properties': properties_data, "key": key})



def save_property_data_view(request):
    for city in range(200, 300):
        url = f"https://www.99acres.com/api-aggregator/discovery/srp/search?area_unit=1&platform=DESKTOP&moduleName=GRAILS_SRP&workflow=GRAILS_SRP&page_size=25000&page=1&city={city}&preference=S&res_com=R&seoUrlType=DEFAULT&recomGroupType=VSP&pageName=SRP&groupByConfigurations=true"
        response = requests.get(url)
        json_file = response.json()
        print(str(city))
        if json_file.get('properties'):
            for property in json_file.get('properties'):
                try:
                    save_property_data_with_transaction(property)
                except:
                    continue
        time.sleep(1)
    return HttpResponse("Property data saved successfully")



def save_property_data_with_transaction(property):
    with transaction.atomic():
        save_property_data(property)


# def save_property_data_view(request):
#     file_path = "response.json"
#     def read_json_file(file_path):
#         with open(file_path, 'r') as file:
#             return json.load(file)
#     json_file = read_json_file(file_path)
#     for property in json_file.get('properties'):
#         try:
#             save_property_data_with_transaction(property)
#         except:
#             continue
#     return HttpResponse("Property data saved successfully")

def save_property_data(prop_data):

    # Creating metadata object
    meta_data = prop_data.get('meta_data', {})
    metadata = MetaData.objects.create(
        prop_photo_count=meta_data.get('PROP_PHOTO_COUNT', None),
        prop_video_count=meta_data.get('PROP_VIDEO_COUNT', None)
    )

    # Creating location object
    location = Location.objects.create(
        city=prop_data.get('CITY_ID', None),
        cityName=prop_data.get('CONTACT_CITY_NAME', ''),
        buildingId=prop_data.get('BUILDING_ID', None),
        buildingName=prop_data.get('BUILDING_NAME', ''),
        societyName=prop_data.get('SOCIETY_NAME', ''),
        localityId=prop_data.get('LOCALITY_ID', None),
        localityName=prop_data.get('LOCALITY_WO_CITY', ''),
        address=prop_data.get('ADDRESS', ''),
    )
    super_profile_data = prop_data.get('profile',{}).get('super')
    super_profile = SuperProfile.objects.create(
        contact_company_name=super_profile_data.get('CONTACT_COMPANY_NAME', ''),
        photo_url=super_profile_data.get('DEALER_PHOTO_URL', ''),
        since=super_profile_data.get('SINCE', ''),
        total_eoi=super_profile_data.get('TOTAL_EOI', 0),
    )
    # Creating profile object
    profile_data = prop_data.get('profile', {})
    profile = Profile.objects.create(
        contact_name=profile_data.get('CONTACT_NAME', None),
        contact_company_name=profile_data.get('CONTACT_COMPANY_NAME', None),
        class_label=profile_data.get('CLASS_LABEL', None),
        contact_city=profile_data.get('CONTACT_CITY', None),
        assigned_to_profileid=profile_data.get('ASSIGNED_TO_PROFILEID', None),
        url=profile_data.get('URL', None),
        photo_url=profile_data.get('PHOTO_URL', None),
        dealer_seo_url=profile_data.get('DEALER_SEO_URL', None),
        super_profile = super_profile
    )

    # Creating map_details object
    map_data = prop_data.get('MAP_DETAILS',{})
    map_details = MapDetails.objects.create(
        zoomLevel=map_data.get('ZOOM_LEVEL', None),
        mapAccuracy=map_data.get('MAP_ACCURACY', None),
        mapped=map_data.get('MAPPED', None),
        latitude=map_data.get('LATITUDE', None),
        source=map_data.get('SOURCE', None),
        longitude=map_data.get('LONGITUDE', None),
    )

    fsl = prop_data.get('FSL_Data',{})
    # Creating fsl_data object
    fsl_data = FSLData.objects.create(
        localityId=fsl.get('LOCALITY_ID', None),
        type=fsl.get('TYPE', None),
    )
    formatted_data = prop_data.get('FORMATTED',{})
    formatted = Formatted.objects.create(
        availability=formatted_data.get('AVAILABILITY', 0),
        sub_availability=formatted_data.get('SUB_AVAILABILITY', 0),
        availability_date=formatted_data.get('AVAILABILITY_DATE', None),
        avg_price=formatted_data.get('AVG_PRICE', 0),
        price_sqft=formatted_data.get('PRICE_SQFT', 0),
        logo=formatted_data.get('LOGO', ''),
        floor_number=formatted_data.get('FLOOR_NUMBER', 0),
        tenant_preferences=formatted_data.get('TENANT_PREFERENCES', ''),
        prop_type_label=formatted_data.get('PROP_TYPE_LABEL', ''),
        furnish_label=formatted_data.get('FURNISH_LABEL', ''),
        furnishing_attributes=formatted_data.get('FURNISHING_ATTRIBUTES', ''),
        rera_type=formatted_data.get('RERA_TYPE', ''),
        price_in_words=formatted_data.get('PRICE_IN_WORDS', ''),
        description=formatted_data.get('DESCRIPTION', ''),
        havephoto=formatted_data.get('HAVEPHOTO', ''),
        amenities=formatted_data.get('AMENITIES', ''),
        alt_tag=formatted_data.get('ALT_TAG', ''),
        )
    formatted_landmark_data = prop_data.get('FORMATTED_LANDMARK_DATA', {})
    formatted_landmark = FormattedLandmarkDetails.objects.create(
        category=formatted_landmark_data.get('category', ''),
        text=formatted_landmark_data.get('text', ''),
        className=formatted_landmark_data.get('className', ''),
        icon=formatted_landmark_data.get('icon', ''),
    )
    separator = " "
    project_highlights = separator.join(prop_data.get('PROJECT_HIGHLIGHTS',""))
    topUsps = separator.join(prop_data.get('TOP_USPS', ''))
    property_data = Property(
        propId=prop_data.get('PROP_ID'),
        photoUrl=prop_data.get('PHOTO_URL'),
        mediumPhotoUrl=prop_data.get('mediumPhotoUrl'),
        preference=prop_data.get('PREFERENCE'),
        description=prop_data.get('DESCRIPTION', ''),
        propertyType=prop_data.get('PROPERTY_TYPE', ''),
        city=prop_data.get('CITY', ''),
        locality=prop_data.get('LOCALITY', ''),
        builtupArea=prop_data.get('BUILTUP_AREA', 0.0),
        areaUnit=prop_data.get('AREA_UNIT', ''),
        builtupSqft=prop_data.get('BUILTUP_SQFT', 0.0),
        transactType=prop_data.get('TRANSACT_TYPE', ''),
        ownType=prop_data.get('OWNTYPE', None),
        bedroomNum=prop_data.get('BEDROOM_NUM', None),
        bathroomNum=prop_data.get('BATHROOM_NUM', None),
        bathroomAttached=prop_data.get('BATHROOM_ATTACHED', ''),
        balconyAttached=prop_data.get('BALCONY_ATTACHED', ''),
        balconyNum=prop_data.get('BALCONY_NUM', None),
        pricePerUnitArea=prop_data.get('PRICE_PER_UNIT_AREA', 0.0),
        bookingAmount=prop_data.get('BOOKING_AMOUNT', None),
        availability=prop_data.get('AVAILABILITY', ''),
        furnish=prop_data.get('FURNISH', None),
        facing=prop_data.get('FACING', None),
        age=prop_data.get('AGE', None),
        floorNum=prop_data.get('FLOOR_NUM', None),
        totalFloor=prop_data.get('TOTAL_FLOOR', None),
        postingDate=prop_data.get('POSTING_DATE', None),
        updateDate=prop_data.get('UPDATE_DATE', None),
        classs=prop_data.get('CLASS', ''),
        resCom=prop_data.get('RES_COM', ''),
        propName=prop_data['PROP_NAME'],
        propertyNumber=prop_data['PROPERTY_NUMBER'],
        minPrice=prop_data.get('MIN_PRICE', None),
        maxPrice=prop_data.get('MAX_PRICE', None),
        priceSqft=prop_data.get('PRICE_SQFT', 0.0),
        listing=prop_data.get('Listing', None),
        carpetArea=prop_data.get('CARPET_AREA', 0.0),
        carpetAreaUnit = prop_data.get('CARPETAREA_UNIT', 0.0),
        carpetSqft = prop_data.get('CARPET_SQFT', 0.0),
        verified = prop_data.get('VERIFIED', 0.0),
        superBuiltUpArea = prop_data.get('SUPERBUILTUP_AREA', 0.0),
        superBuiltUpAreaUnit = prop_data.get('SUPERBUILTUPAREA_UNIT', 0.0),
        superBuiltUpSqft = prop_data.get('SUPERBUILTUP_SQFT', 0.0),
        maskContact = prop_data.get('MASK_CONTACT', 0.0),
        confId = prop_data.get('CONF_ID', 0.0),
        brokerage = prop_data.get('BROKERAGE', 0.0),
        deposit = prop_data.get('DEPOSIT', 0.0),
        depositType = prop_data.get('DEPOSIT_TYPE', 0.0),
        cornerProperty = prop_data.get('CORNER_PROPERTY', 0.0),
        reservedParking = prop_data.get('RESERVED_PARKING', 0.0),
        mapDetails = map_details,
        fslData = fsl_data,
        minAreaSqft = prop_data.get('MIN_AREA_SQFT', 0.0),
        maxAreaSqft = prop_data.get('MAX_AREA_SQFT', 0.0),
        showBsp = prop_data.get('SHOW_BSP', 0.0),
        isNewLaunch = prop_data.get('IS_NEW_LAUNCH', 0.0),
        isPosterReraRegistered = prop_data.get('IS_POSTER_RERA_REGISTERED', 0.0),
        isDealerReraRegistered = prop_data.get('IS_DEALER_RERA_REGISTERED', 0.0),
        formatted = formatted,
        havephoto = prop_data.get('HAVEPHOTO', 0.0),
        altTag = prop_data.get('ALT_TAG', 0.0),
        isPreLeased = prop_data.get('IS_PRE_LEASED', 0.0),
        preLeasedCurrentRent = prop_data.get('PRE_LEASED_CURRENT_RENT', 0.0),
        productType = prop_data.get('PRODUCT_TYPE', 0.0),
        topUsps = topUsps,
        selfVerified=prop_data.get('SELF_VERIFIED', 0.0),
        expiryDate = prop_data.get('EXPIRY_DATE', 0.0),
        gated = prop_data.get('GATED', 0.0),
        groupName = prop_data.get('GROUP_NAME', 0.0),
        groupMeta = prop_data.get('GROUP_META', 0.0),
        propertyTypeU = prop_data.get('PROPERTY_TYPE__U', 0.0),
        areaUnitU = prop_data.get('AREA_UNIT__U', 0.0),
        postingDateU = prop_data.get('POSTING_DATE__U', 0.0),
        updateDateU = prop_data.get('UPDATE_DATE__U', 0.0),
        carpetAreaUnitU = prop_data.get('CARPETAREA_UNIT__U', 0.0),
        superBuiltupAreaUnitU = prop_data.get('SUPERBUILTUPAREA_UNIT__U', 0.0),
        expiryDateU = prop_data.get('EXPIRY_DATE__U', 0.0),
        area = prop_data.get('AREA', 0.0),
        secondaryArea = prop_data.get('SECONDARY_AREA', 0.0),
        price = prop_data.get('PRICE', 0.0),
        propHeading = prop_data.get('PROP_HEADING', 0.0),
        propDetailsUrl = prop_data.get('PROP_DETAILS_URL', 0.0),
        valueLabel =prop_data.get('VALUE_LABEL', 0.0),
        classHeading = prop_data.get('CLASS_HEADING', 0.0),
        page = prop_data.get('PAGE', 0.0),
        classLabel = prop_data.get('CLASS_LABEL', 0.0),
        isFSL = prop_data.get('IS_FSL', 0.0),
        isFresh = prop_data.get('IS_FRESH', 0.0),
        shortlisted = prop_data.get('SHORTLISTED', 0.0),
        reported = prop_data.get('REPORTED', 0.0),
        registerDate = prop_data.get('REGISTER_DATE__U', 0),
        postedOnColored = prop_data.get('POSTED_ON_COLORED', 0.0),
        totalLandmarkCount = prop_data.get('TOTAL_LANDMARK_COUNT', 0.0),
        formattedLandmarkDetails = formatted_landmark,
        contactCityName = prop_data.get('CONTACT_CITY_NAME', 0.0),
        contactName = prop_data.get('CONTACT_NAME', 0.0),
        contactCompanyName = prop_data.get('CONTACT_COMPANY_NAME', 0.0),
        dealerPhotoUrl = prop_data.get('DEALER_PHOTO_URL', 0.0),
        isDefaultDealerImage = prop_data.get('IS_DEFAULT_DEALER_IMAGE', 0.0),
        assignedToProfileid = prop_data.get('ASSIGNED_TO_PROFILEID', 0.0),
        societyName = prop_data.get('SOCIETY_NAME', 0.0),
        buildingName = prop_data.get('BUILDING_NAME', 0.0),
        cityId = prop_data.get('CITY_ID', 0.0),
        localityWoCity = prop_data.get('LOCALITY_WO_CITY', 0.0),
        profile = profile,
        registrationStatus = prop_data.get('REGISTRATION_STATUS', 0.0),
        projectHighlights = project_highlights,
        projectRating = prop_data.get('PROJECT_RATING', 0.0),
        metadata = metadata,
        location = location,
    )
    property_data.save()
    print("property with id"+ str(property_data)+" has been saved." )
    return str(property_data)
