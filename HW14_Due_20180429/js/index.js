// Get references to the tbody element, input field and button
var $tbody = document.querySelector("tbody");
var $stateInput = document.querySelector("#state");
var $cityInput = document.querySelector("#city");

var $searchBtn = document.querySelector("#search");

// Add an event listener to the searchButton, call handleSearchButtonClick when clicked
$searchBtn.addEventListener("click", handleSearchButtonClick);

// Set filteredSightings to dataSet initially
var filteredSightings = dataSet;

// renderTable renders the filteredSightings to the tbody
function renderTable() {
  $tbody.innerHTML = "";
  for (var i = 0; i < filteredSightings.length; i++) {
    // Get get the current address object and its fields
    var address = filteredSightings[i];
    var fields = Object.keys(address);
    // Create a new row in the tbody, set the index to be i + startingIndex
    var $row = $tbody.insertRow(i);
    for (var j = 0; j < fields.length; j++) {
      // For every field in the address object, create a new cell at set its inner text to be the current value at the current address's field
      // var field = fields[j];
      var $cell = $row.insertCell(j);
      $cell.innerText = address[fields[j]];
    }
  }
}

function handleSearchButtonClick() {
  // Format the user's search by removing leading and trailing whitespace, lowercase the string
  var filterState = $stateInput.value.trim().toLowerCase();
  var filterCity = $cityInput.value.trim().toLowerCase();
  // Set filteredSightings to an array of all addresses whose "state" matches the filter
  filteredSightings = dataSet.filter(function(address) {
    var addressState = address.state.toLowerCase();
    var addressCity = address.city.toLowerCase();
    // If true, add the address to the filteredSightings, otherwise don't add it to filteredAddresses
    // If state input length > 0 and city input length > 0
    if (filterState.length > 0 && filterCity.length > 0) {
      return addressState === filterState && addressCity === filterCity;
    }
    // If state input is 0, filter by city
    else if (filterState.length == 0) {
      return addressCity === filterCity;
    }
    // If city input is 0, filter by state
    else if (filterCity.length == 0) {
      return addressState === filterState;
    }

  });
  renderTable();
}

// Render the table for the first time on page load
renderTable();
