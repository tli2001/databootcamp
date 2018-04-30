// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $dateTimeInput = document.querySelector("#datetime");
var $stateInput = document.querySelector("#state");
var $cityInput = document.querySelector("#city");
var $countryInput = document.querySelector("#country");
var $shapeInput = document.querySelector("#shape");

var $searchBtn = document.querySelector("#search");

// Add an event listener to the searchButton, call handleSearchButtonClick when clicked
$searchBtn.addEventListener("click", handleSearchButtonClick);

// Set filteredSightings and dataSetFiltered to dataSet initially
var filteredSightings = dataSet;
var dataSetFiltered = dataSet;

// renderTable renders the filteredSightings to the tbody
function renderTable() {
  $tbody.innerHTML = "";
  console.log("renderTable - FS length: ", filteredSightings.length)
  for (var i = 0; i < filteredSightings.length; i++) {
    // Get get the current sighting object and its fields
    var sighting = filteredSightings[i];
    var fields = Object.keys(sighting);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the sighting object, create a new cell at set its inner text to be the current value at the current address's field
      // var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = sighting[fields[j]];
    }
  }
}

function filterFunction(data, filter) {
  var filterDateTime = $dateTimeInput.value.trim(); // do not need to lower case date
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCity = $cityInput.value.trim().toLowerCase();
  var filterCountry = $countryInput.value.trim().toLowerCase();
  var filterShape = $shapeInput.value.trim().toLowerCase();

  dataSetFiltered = filteredSightings.filter(function(sighting) {
    var sightingDate = sighting.datetime;
    var sightingState = sighting.state.toLowerCase();
    var sightingCity = sighting.city.toLowerCase();
    var sightingCountry = sighting.country.toLowerCase();
    var sightingShape = sighting.shape.toLowerCase();
    
    // filter sightings depending on which filter parameter was passed through the function
    if (filter == "datetime") {
      // console.log("filter matched datetime")
      return sightingDate === filterDateTime;
    }
    else if (filter == "state") {
      // console.log("filter matched state")
      return sightingState === filterState;
    }
    else if (filter == "city") {
      // console.log("filter matched city")
      return sightingCity === filterCity;
    }
    else if (filter == "country") {
      // console.log("filter matched country")
      return sightingCountry === filterCountry;
    }
    else if (filter == "shape") {
      // console.log("filter matched shape")
      return sightingShape === filterShape;
    }
    else {
      console.log("filter did not match")
      return true;
    }
  })
  console.log("filter: ", filter, "dataSet: ", dataSet.length, " filteredSightings: ", filteredSightings.length, " dataSetFiltered: ", dataSetFiltered.length)
  return dataSetFiltered;
}

function handleSearchButtonClick() {
  // check search parameter inputs
  var filterDateTime = $dateTimeInput.value.trim(); // do not need to lower case date
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCity = $cityInput.value.trim().toLowerCase();
  var filterCountry = $countryInput.value.trim().toLowerCase();
  var filterShape = $shapeInput.value.trim().toLowerCase();

  // for each search parameter input that is not blank, filter the sightings by the parameter
  if (filterDateTime.length > 0) {
    filteredSightings = filterFunction(filteredSightings, "datetime");
    console.log("FS after filtering by date: ", filteredSightings.length);
  }
  if (filterState.length > 0) {
    filteredSightings = filterFunction(filteredSightings, "state");
    console.log("FS after filtering by state: ", filteredSightings.length);
  }
  if (filterCity.length > 0) {
    filteredSightings = filterFunction(filteredSightings, "city");
    console.log("FS after filtering by city: ", filteredSightings.length);
  }
  if (filterCountry.length > 0) {
    filteredSightings = filterFunction(filteredSightings, "country");
    console.log("FS after filtering by country: ", filteredSightings.length);
  }
  if (filterShape.length > 0) {
    filteredSightings = filterFunction(filteredSightings, "shape");
    console.log("FS after filtering by shape: ", filteredSightings.length);
  }
  // renders filtered results after filtering
  renderTable();
  // reset filteredSightings back to full dataset
  filteredSightings = dataSet;
}

// Render the table for the first time on page load
renderTable();
