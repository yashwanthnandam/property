import React from 'react';
import PlacesAutocomplete from 'react-places-autocomplete';

import  {
  geocodeByAddress,
  getLatLng,
} from 'react-places-autocomplete';
import './style.css';

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchTerm: '',
      searchFilters: {
        minPrice: '',
        maxPrice: '',
        noBeds: '',
        noBaths: '',
        propertyType: '',
        mapBounds:'',
        address: '',

      },
      center:{lat:28.704060,lng:77.102490},
      term: '' 
    };

  }
  handleChange = address => {
    this.setState({ address });
  };
  handleSelect = async address => {
    try {
      const results = await geocodeByAddress(address);
      const latLng = await getLatLng(results[0]);
      
      this.setState({
        center: latLng,
      });

      this.props.onSelect(latLng);
      
    } catch (error) {
      console.error('Error', error);
    }
  };
  

  handleInputChange = (event) => {
    const { name, value, type } = event.target;
    if (type === 'checkbox') {
      this.setState(prevState => ({
        searchFilters: {
          ...prevState.searchFilters,
          [name]: !prevState.searchFilters[name]
        }
      }));
      
    } else if (name === 'searchTerm') {
      this.setState(prevState => ({
        searchFilters: {
          ...prevState.searchFilters,
          [name]: value
        }
      }));
    } else {
      this.setState(prevState => ({
        searchFilters: {
          ...prevState.searchFilters,
          [name]: value
        }
      }));
    }
  }
  
  
  

  

  handleFilterChange = (event) => {
    const { name, value } = event.target;
    this.setState(prevState => ({
      searchFilters: {
        ...prevState.searchFilters,
        [name]: value
      }
    }));
  }
  
  

  handleSearch = async() => {
    console.log('search clicked');
    const { searchTerm, searchFilters } = this.state;
    
    try {
      // console.log('api called in search bar')
      // const { minPrice, maxPrice, noBeds, noBaths, propertyType, mapBounds, buy, rent } = searchFilters;
      // let url = `http://127.0.0.1:8003/get_properties/?page_size=50&bedroom_num=${noBeds}&bathroomNum=${noBaths}&property_type=${propertyType}&search=${searchTerm}&buy=${buy}&rent=${rent}`;
  
      // if (minPrice) {
      //   url += `&price_min=${minPrice}`;
      // }
      // if (maxPrice) {
      //   url += `&price_max=${maxPrice}`;
      // }
  
      // if (mapBounds) {
      //   url += `&latitude_min=${mapBounds.getSouthWest().lat()}&latitude_max=${mapBounds.northEast.lat}&longitude_min=${mapBounds.getSouthWest().lng()}&longitude_max=${mapBounds.getNorthEast().lng()}`;
      // }
  
      // if (this.state.rent) {
      //   url += '&rent=true';
      // } else if (this.state.buy) {
      //   url += '&buy=true';
      // }
  
      // const response = await fetch(url);
      // const data = await response.json();
      // const properties = data.properties;
      // this.setState({ properties: properties });
      // console.log(properties)
      this.props.onSearch(searchTerm, searchFilters);

    } catch (error) {
      console.error(error);
    }
  }

  render() {
    console.log('searchbar rendering start');
    return (
      <div className="search-bar">
          <label
          style={{ paddingRight: "1em" ,paddingLeft:"1em", marginRight:"1em", marginLeft: "1em" }}
          >
          Buy:
          <input
            type="checkbox"
            name="buy"
            checked={this.state.searchFilters.buy}
            onChange={this.handleInputChange}
            

          />
        </label>
        <label>
          Rent:
          <input
            type="checkbox"
            name="rent"
            checked={this.state.searchFilters.rent}
            onChange={this.handleInputChange}
            style={{ paddingRight: "1em" ,paddingLeft:"1em", marginRight:"1em", marginLeft: "1em" }}

          />
        </label>
        <div className="search-bar-container" style = {{display:"flex"}}>
  <div className="search-bar-row" >
    <PlacesAutocomplete
      value={this.state.address}
      onChange={this.handleChange}
      onSelect={this.handleSelect}
    >
      {({
        getInputProps,
        suggestions,
        getSuggestionItemProps,
        loading,
      }) => (
        <div className="search-bar-autocomplete" >
          <input
            {...getInputProps({
              placeholder: "Search Places ...",
              className: "location-search-input",
            })}
          />
          <div className="suggestions-container" >
            {loading && <div>Loading...</div>}
            {suggestions.map((suggestion) => {
              const className = suggestion.active
                ? "suggestion-item--active"
                : "suggestion-item";
              const style = suggestion.active
                ? {
                    backgroundColor: "#fafafa",
                    cursor: "pointer",
                  }
                : { backgroundColor: "#ffffff", cursor: "pointer" };
              return (
                <div
                  {...getSuggestionItemProps(suggestion, {
                    className,
                    style: suggestion.active
                ? {
                    backgroundColor: "#fafafa",
                    cursor: "pointer",
                    fontSize: "13px",
                  }
                : {
                    backgroundColor: "#ffffff",
                    cursor: "pointer",
                    fontSize: "13px",
                  },
                  })}
                >
                  {suggestion.description.slice(0, 30)}
                  {suggestion.description.length > 30 ? '...' : ''}
                </div>
              );
            })}
            {suggestions.length > 0 && (
              <div className="suggestions-dropdown" >
                {suggestions.map((suggestion) => (
                  <div
                    {...getSuggestionItemProps(suggestion, {
                      className: "suggestion-dropdown-item",
                    })}
                  >

                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </PlacesAutocomplete>
    </div>

    <div className="search-bar-input-container" >
      <input
        type="number"
        name="minPrice"
        placeholder="Min Price"
        value={this.state.searchFilters.minPrice}
        onChange={this.handleFilterChange}
        className="search-bar-input"
        style={{marginRight:'20px'}}
      />

      <input
        type="number"
        name="maxPrice"
        placeholder="Max Price"
        value={this.state.searchFilters.maxPrice}
        onChange={this.handleFilterChange}
        className="search-bar-input"
        style={{marginRight:'20px'}}

      />

      <input
        type="number"
        name="noBeds"
        placeholder="No of Beds"
        value={this.state.searchFilters.noBeds}
        onChange={this.handleFilterChange}
        className="search-bar-input"
        style={{marginRight:'20px'}}

      />

      <input
        type="number"
        name="noBaths"
        placeholder="No of Baths"
        value={this.state.searchFilters.noBaths}
        onChange={this.handleFilterChange}
        style={{marginRight:'20px'}}
      />

      <button onClick={this.handleSearch} className="search-bar-button">
        Search
      </button>
    </div>
  
</div>
</div>

          
          
          
          
    );
  }
  
  
  
}

export default SearchBar;