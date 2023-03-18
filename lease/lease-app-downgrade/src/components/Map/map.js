import {GoogleMap, useLoadScript, Marker} from "@react-google-maps/api";
import { useMemo } from "react";

export default function Home(){
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: 'AIzaSyCqCO4OFri0-do9lW15udLNC_Bh-KbkW0I'
  });
  if (!isLoaded) return <div>Loading ...</div>;
  return <Map/>
}
function Map(){
  const center = useMemo(()=> ({lat:28.704060,lng:77.102490}), []);
  return (
    <GoogleMap zoom={10} center={center} mapContainerClassName="map-container">
      <Marker position={center}/>
    </GoogleMap>
  )
}