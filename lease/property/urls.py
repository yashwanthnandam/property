from django.urls import path
from .views import save_property_data_view, get_map_view, get_properties

urlpatterns = [
    path('save_property_data/', save_property_data_view, name='save_property_data'),
    path('get_map_view/', get_map_view, name='get_map_view'),
    path('get_properties/', get_properties, name='get_property'),

]
