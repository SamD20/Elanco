from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Endpoints
RESTCOUNTRIES_API = "https://restcountries.com/v3.1/all"
CITYPOPULATION_API = "https://countriesnow.space/api/v0.1/countries/population/cities"
COUNTRY_FLAGS_API = "https://countriesnow.space/api/v0.1/countries/flag/images"

# Fetching data from the APIs
populationDataContent = requests.get(CITYPOPULATION_API).json()
countryFlagsDataContent = requests.get(COUNTRY_FLAGS_API).json()
restcountry = requests.get(RESTCOUNTRIES_API).json()

# Function to change official country names to common names
def changeCountryNames(rawCountryData):
    officialToCommon = {country['name']['official']: country['name']['common'] for country in restcountry}
    tempCountryList = []
    changesMade = {}

    # Creating a list of unique countries
    for data in rawCountryData:
        if data["country"] not in tempCountryList:
            tempCountryList.append(data["country"])

    tempCountryList = tempCountryList[:-2]  # Removing the last two entries

    # Updating country names with their common name if applicable
    for i, country in enumerate(tempCountryList):
        if country in officialToCommon:
            common_name = officialToCommon[country]
            if country != common_name:
                tempCountryList[i] = common_name
                changesMade[country] = common_name

    return tempCountryList, changesMade

# Function to get a list of city names for a selected country
def getCityNames(rawCountryData, selectedCountry, changesDict):
    tempCityList = []
    
    # If a country name was changed, update the selected country to match the official name
    for old, new in changesDict.items():
        if selectedCountry == new:
            selectedCountry = old

    # Collect cities for the selected country
    for data in rawCountryData:
        if data["city"] not in tempCityList and data["country"] == selectedCountry:
            tempCityList.append(data["city"].title())

    return tempCityList

# Function to get country and city names based on status (city mode or not)
def getCountryCityNames(status, selectedCountry):
    if status:
        changedCountries = changeCountryNames(populationDataContent["data"])
        return changedCountries[0], changedCountries[1], getCityNames(populationDataContent["data"], selectedCountry, changedCountries[1])
    else:
        return sorted([country['name']['common'] for country in restcountry]), [], []

# Function to retrieve selected country and city from the request
def getSelections(status):
    selectedCountry = request.args.get("country", None)
    selectedCity = request.args.get("city", None)
    return selectedCountry, selectedCity

# Function to retrieve the flag image URL for the selected country
def getFlag(selectedCountry):
    if selectedCountry:
        for country in restcountry:
            if country['name']['common'].lower() == selectedCountry.lower() or country['name']['official'].lower() == selectedCountry.lower():
                return country['flags']['png']
    return None

# Function to fetch population data for the selected country and city
def getPopulationData(status, selectedCountry, selectedCity):
    try:
        years = []
        populations = []
        
        # If a country is selected
        if selectedCountry is not None:
            if status and selectedCity is not None:  # City mode enabled
                for city in populationDataContent["data"]:
                    if city["city"].lower() == selectedCity.lower():
                        for record in city['populationCounts']:
                            years.append(record['year'])
                            populations.append(record['value'])
            elif not status:  # No city mode, fetching total population for a country
                countryCode = next((country['cca3'] for country in restcountry if country['name']['common'] == selectedCountry or country['name']['official'] == selectedCountry), None)
                populationInfoUrl = f"https://api.worldbank.org/v2/country/{countryCode}/indicator/SP.POP.TOTL?format=json&rows=1000&os=0"
                populationInfoData = requests.get(populationInfoUrl).json()
                years = [entry['date'] for entry in populationInfoData[1]]
                populations = [entry['value'] for entry in populationInfoData[1]]

        return years, populations
    except:
        return [], []  # Return empty lists if there's an error

@app.route("/", methods=["GET", "POST"])
def index():
    # Default state (cityCountryButtonState=False means no city mode initially)
    cityCountryButtonState = False
    selectedCountry, selectedCity = getSelections(cityCountryButtonState)
    myCountries, _, cityList = getCountryCityNames(cityCountryButtonState, selectedCountry)

    # Initialize variables for population data and flag URL
    populationData = []
    flagUrl = None

    return render_template(
        "index.html",
        state=cityCountryButtonState,
        countryList=myCountries,
        selectedCountry=selectedCountry,
        selectedCity=selectedCity,
        cityList=cityList,
        flagUrl=flagUrl,
        populationData=populationData,
    )

@app.route("/update_data", methods=["GET", "POST"])
def update_data():
    # Retrieve the status of city mode from the request
    city_mode = request.args.get("city_mode", "false").lower() == "true"
    selectedCountry, selectedCity = getSelections(city_mode)

    # Get country and city names based on city mode status
    myCountries, _, cityList = getCountryCityNames(city_mode, selectedCountry)
    flagUrl = getFlag(selectedCountry)

    # Fetch population data based on selected country and city
    years, populations = getPopulationData(city_mode, selectedCountry, selectedCity)

    return jsonify({
        'countries': myCountries, 
        'cities': cityList, 
        'flagUrl': flagUrl, 
        'years': years, 
        'populations': populations
    })

if __name__ == "__main__":
    app.run(debug=True)
