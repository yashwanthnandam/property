export const getProperties = async (params) => {
    const urlSearchParams = new URLSearchParams(params);
    const response = await fetch(`https://ghardhuundo.in/get_properties/?${urlSearchParams}`);
    const data = await response.json();
    return data.properties;
  };
  