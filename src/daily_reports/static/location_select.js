let map, marker, autocomplete;

async function initMap() {
  const markerElement = document.getElementById("markerData");
  const defaultLocation = { lat: parseFloat(markerElement.dataset.lat), lng: parseFloat(markerElement.dataset.lng) };
  
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Initialize map
  map = new Map(document.getElementById("map"), {
    center: defaultLocation,
    zoom: 4,
    mapId: "DEMO_MAP_ID",
  });

  // Initialize marker
  marker = new AdvancedMarkerElement({
    position: defaultLocation,
    map: map,
    gmpDraggable: true,
    title: "Drag me!",
  });

  // Update location fields on marker drag
  marker.addListener("dragend", () => {
    const position = marker.position;
    markerElement.dataset.lat = position.lat;
    markerElement.dataset.lng = position.lng;
    reverseGeocode(position);
  });

  // Click to move marker
  map.addListener("click", (event) => {
    const clickedLocation = event.latLng;
    marker.position = clickedLocation;
    const position = marker.position;
    map.panTo(clickedLocation);
    markerElement.dataset.lat = position.lat;
    markerElement.dataset.lng = position.lng;
    reverseGeocode(clickedLocation);
  });

  // Initialize autocomplete
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("location"),
    {
      fields: ["geometry", "formatted_address"],
      types: ["geocode"], // Only geocodable results
    }
  );

  // On place selection from autocomplete
  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();

    if (place.geometry) {

      // Update map and marker position
      map.setCenter(place.geometry.location);
      map.setZoom(15);
      marker.position = place.geometry.location;

      const position = marker.position;

      // Update hidden fields
      
      markerElement.dataset.lat = position.lat;
      markerElement.dataset.lng = position.lng;
    } else {
      alert("No geometry found for the selected place.");
    }
  });  
}

async function reverseGeocode(location) {
  const geocoder = new google.maps.Geocoder();
  const response = await geocoder.geocode({ location });

  if (response.results[0]) {
    document.getElementById("location").value = response.results[0].formatted_address;
  } else {
    document.getElementById("location").value = "";
  }
}