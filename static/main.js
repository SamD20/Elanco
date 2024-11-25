// Toggle the visibility of the city dropdown and fetch updated data
function toggleDropdown() {
    const checkbox = document.getElementById("showCity");
    const dropdown = document.getElementById("cityDropdown");
    const citySelect = document.getElementById("city");

    const isChecked = checkbox.checked;
    dropdown.classList.toggle("show", isChecked);  // Show or hide dropdown
    citySelect.disabled = !isChecked;  // Enable/Disable city dropdown based on checkbox state

    fetchUpdatedDropdownData();  // Fetch updated data from the server
}

// Fetch and update country and city dropdowns based on the checkbox state
function fetchUpdatedDropdownData() {
    const checkbox = document.getElementById("showCity");
    const cityMode = checkbox.checked ? "true" : "false"; // Get checkbox state

    fetch(`/update_data?city_mode=${cityMode}`)
        .then(response => response.json())
        .then(data => {
            updateDropdowns(data);
            updateChartAndFlag(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Update the country and city dropdowns with new data
function updateDropdowns(data) {
    const countrySelect = document.getElementById("country");
    const citySelect = document.getElementById("city");

    countrySelect.innerHTML = '<option value="">Choose a country</option>';
    data.countries.forEach(country => {
        const option = document.createElement("option");
        option.value = country;
        option.textContent = country;
        countrySelect.appendChild(option);
    });

    if (document.getElementById("showCity").checked) {
        citySelect.innerHTML = '<option value="">Choose a city</option>';
        data.cities.forEach(city => {
            const option = document.createElement("option");
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    }
}

// Update the chart and flag image
function updateChartAndFlag(data) {
    updateChart(data.years, data.populations); // Update the chart with new data
    updateFlagImage(data.flagUrl);  // Update the flag image
}

// Update city dropdown based on selected country
function updateCityDropdown() {
    const selectedCountry = document.getElementById("country").value;
    const cityMode = document.getElementById("showCity").checked ? "true" : "false";

    fetch(`/update_data?city_mode=${cityMode}&country=${selectedCountry}`)
        .then(response => response.json())
        .then(data => {
            const citySelect = document.getElementById("city");
            citySelect.innerHTML = '<option value="">Choose a city</option>';
            data.cities.forEach(city => {
                const option = document.createElement("option");
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });

            updateChartAndFlag(data);  // Update chart and flag after city data
        })
        .catch(error => console.error('Error updating city dropdown:', error));
}

// Update the chart and flag based on selected city
function onCitySelect() {
    const selectedCountry = document.getElementById("country").value;
    const selectedCity = document.getElementById("city").value;
    const cityMode = document.getElementById("showCity").checked ? "true" : "false";

    fetch(`/update_data?city_mode=${cityMode}&country=${selectedCountry}&city=${selectedCity}`)
        .then(response => response.json())
        .then(data => {
            updateChartAndFlag(data);  // Update chart and flag after selecting a city
        })
        .catch(error => console.error('Error fetching city data:', error));
}

// Update the flag image
function updateFlagImage(flagUrl) {
    document.getElementById("flag").src = flagUrl;  // Set flag image URL
}

// Initialize event listeners and set initial state
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("showCity").addEventListener("change", toggleDropdown);
    document.getElementById("country").addEventListener("change", updateCityDropdown);
    document.getElementById("city").addEventListener("change", onCitySelect);

    toggleDropdown(); // Initialize dropdown state on page load
});
