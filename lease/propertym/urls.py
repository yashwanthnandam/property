from django.urls import path
from .views import PropertyListAPIView, PropertyCreateAPIView, save_property_data_view

urlpatterns = [
    path("get_properties/", view=PropertyListAPIView.as_view(),name="properties"),
    path("create_property/", view=PropertyCreateAPIView.as_view(), name="createproperty"),
    path('save_property_data/', save_property_data_view, name='save_property_data'),

]
