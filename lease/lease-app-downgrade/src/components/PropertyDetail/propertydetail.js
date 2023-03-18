import React from 'react';
import './style.css';

const PropertyDetail = ({ properties, onPropertyHover }) => {
  return (
    <div className="property-detail-container">
      {properties && properties.slice(0, 10).map(property => (
        <div className="property-card" key={property.id}
          onMouseEnter={() => onPropertyHover(property.id)}
          onMouseLeave={() => onPropertyHover(null)}
        >
          <div className="card-image">
            <img src={property.image} alt={property.title} />
          </div>
          <div className="card-details">
            <h4>{property.propertyTitle}</h4>
            <p>Price: {property.price}</p>
            <p>Bedrooms: {property.bedroom_num}</p>
            <p>Bathrooms: {property.bathroomNum}</p>
            <p>Area: {property.area}</p>
            <p>Description: {property.description}</p>
            <p>Location: {property.catAdd1}</p>
            <p>Floor: {property.floorD}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PropertyDetail;
