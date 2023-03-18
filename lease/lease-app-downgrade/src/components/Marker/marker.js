import React from 'react';
import {Marker} from 'google-maps-react';

const CustomMarker = (props) => {
    const {id} = props;

    const onMarkerClick = (evt) => {
        console.log(id);
    };


    return (
        <Marker
            onClick={onMarkerClick}
            {...props}
        />
    );
};

export default CustomMarker;