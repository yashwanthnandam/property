export const getProperties = async (params) => {
    const urlSearchParams = new URLSearchParams(params);
    const response = await fetch(`http://127.0.0.1:8003/get_properties/?${urlSearchParams}`);
    const data = await response.json();
    return data.properties;
  };
  