import React, { useState,useMemo, useEffect } from 'react';
import { Map, InfoWindow, GoogleApiWrapper } from 'google-maps-react';
import CustomMarker from '../../components/Marker/marker';
import blueMarkerIcon from '../../assets/images/comment-square-256.png';
import SearchBar from '../../components/SearchBar/searchbar';
import icon from '../../assets/images/marker_icon.png';
import PropertyDetail from '../../components/PropertyDetail/propertydetail';
import { debounce } from 'lodash';
import memoize from 'memoize-one';
const MapContainer = (props) => {
  const [properties, setProperties] = useState([]);
  const [activeMarker, setActiveMarker] = useState(null);
  const [showingInfoWindow, setShowingInfoWindow] = useState(false);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [selectedPropertyId, setSelectedPropertyId] = useState(null);
  const [center, setCenter] = useState({lat:28.704060,lng:77.102490})
  const [mapBounds, setMapBounds] = useState({
    getSouthWest: () => ({ lat: null, lng: null }),
    getNorthEast: () => ({ lat: null, lng: null })
  });
  
  const [searchTerm, setSearchTerm] = useState('');
  const [searchFilters, setSearchFilters] = useState({
    minPrice: '',
    maxPrice: '',
    noBeds: '',
    noBaths: '',
    propertyType: '',
    mapBounds:''
  });
  const [isSearchTriggered, setIsSearchTriggered] = useState(false);



  useEffect(() => {
    if (isSearchTriggered) {
      const fetchProperties = async () => {
        try {
          
          const response = await fetch(`http://13.50.14.134:8003/property/get_properties/?page_size=50&latitude_min=${mapBounds.southWest.lat}&latitude_max=${mapBounds.northEast.lat}&longitude_min=${mapBounds.southWest.lng}&longitude_max=${mapBounds.northEast.lng}&search=${searchTerm}&price_min=${searchFilters.minPrice}&price_max=${searchFilters.maxPrice}&bedroom_num=${searchFilters.noBeds}&bathroomNum=${searchFilters.noBaths}&property_type=${searchFilters.propertyType}&buy=${searchFilters.buy}&rent=${searchFilters.rent}`);
          const data = await response.json();
          console.log(mapBounds)
          const properties = data.properties;
          console.log(properties)
          setProperties(properties);
          setIsSearchTriggered(false);
        } catch (error) {
          console.error(error);
        }
      };
      fetchProperties();
    }
  }, [isSearchTriggered, mapBounds, searchTerm, searchFilters]);
  

  const onMarkerClick = (property, marker, e) => {
    setSelectedProperty(property);
    setShowingInfoWindow(true);
    setActiveMarker(marker);
    console.log(marker,property)
  };
  const handlePropertyHover = (propertyId) => {
    setSelectedPropertyId(propertyId);
    console.log(propertyId)
  }


  const handleSearch = (term, filters, properties) => {
    setSearchTerm(term);
    setSearchFilters(filters);
    setProperties(properties);
    setIsSearchTriggered(true);
  };
  const handleSelect = ( properties, center) => {
    setProperties(properties);
    setIsSearchTriggered(true);
    setCenter(center);
    console.log(center)
  };
  
  const onClose = () => {
    if (activeMarker !== null) {
      setActiveMarker(null);
    }
    setSelectedProperty(null);
    setShowingInfoWindow(false);
  };

  const debouncedOnMapBoundsChanged = useMemo(
    () => debounce((mapProps, map) => {
      const bounds = map.getBounds();
      setMapBounds({
        southWest: { lat: bounds.getSouthWest().lat(), lng: bounds.getSouthWest().lng() },
        northEast: { lat: bounds.getNorthEast().lat(), lng: bounds.getNorthEast().lng() },
      });
    }, 500),
    []
  );
  

  const memoizedPropertiesMap = memoize((properties, selectedPropertyId, onMarkerClick, blueMarkerIcon, icon, googleMapsSize) => {
    return properties.map(property => {
      const isSelected = selectedPropertyId === property.id;
      const markerIcon = isSelected ? blueMarkerIcon : icon;
  
      return (
        <CustomMarker
          key={property.id}
          position={{ lat: property.latitude, lng: property.longitude }}
          onClick={(marker, e) => onMarkerClick(property, marker, e)}
              
          icon={{
            url: markerIcon,
            scaledSize: new googleMapsSize(30, 30),
          }}
          label={{
            text: `${property.price}`,
            color: 'white',
            fontSize: '8px',
          }}
        />
      );
    });
  });
  
  // Usage
  const propertiesMap = memoizedPropertiesMap(properties, selectedPropertyId, onMarkerClick, blueMarkerIcon, icon, props.google.maps.Size);
  
  return (
    <div style={{ position: "relative", height: "100vh", backgroundColor: "white" }}>
  <div style={{ position: "relative", top: 0, left: 0, right: 0, backgroundColor: "white", padding: "1rem" }}>
    <SearchBar onSearch={(term, filters) => handleSearch(term, filters, properties)} 
               onSelect={(center) => handleSelect( properties, center)}
    />
  </div>
  <div style={{ position: "absolute", top: "4rem", left: 0, bottom: 0, width: "69%" }}>

    <Map
      google={props.google}
      zoom={15}
      initialCenter = {center}
      center={center}
      onBoundsChanged={debouncedOnMapBoundsChanged}
      setSelectedPropertyId={setSelectedPropertyId}
    >

    {propertiesMap}
      

      {selectedProperty && showingInfoWindow && activeMarker && (
        <InfoWindow
          visible={selectedProperty !== null && showingInfoWindow}
          marker={activeMarker}
          onClose={onClose}
          pixelOffset={new props.google.maps.Size(0, -30)}
          position={{ lat: activeMarker.position.lat, lng: activeMarker.position.lng }}
          onMouseover={() => setShowingInfoWindow(true)}
          onMouseout={() => setShowingInfoWindow(false)}
        >
          <div>
            <p>Price: {selectedProperty.price}</p>
            <p>Bedrooms: {selectedProperty.bedroom_num}</p>
            <p>Bathrooms: {selectedProperty.bathroomNum}</p>
            <p>Area: {selectedProperty.area}</p>
          </div>
        </InfoWindow>
      )}
    </Map>
  </div>
  <div style={{ position: "absolute", top: "4rem", right: 0, bottom: 0, width: "30%", backgroundColor: "white", padding: "1rem", overflow: "scroll" }}>
  <PropertyDetail properties={properties} onPropertyHover={handlePropertyHover} />



  </div>
</div>

    
  );
};


export default GoogleApiWrapper({
  apiKey: 'AIzaSyCqCO4OFri0-do9lW15udLNC_Bh-KbkW0I'
})(MapContainer);

