# Weather Data API & Visualization
This Flask-based project aims to provide tools for exploring and analyzing historical temperature data sourced from the ECA&D (European Climate Assessment & Dataset). Due to GitHub size limits, the databsae was reduced to 50 stations. The core features include an API and a visualization tool.

## Functionality

### Home Page
Presents a comprehensive table of available weather stations. This table includes essential information like station ID, station name, and country, aiding users in selecting the desired station.


### API Endpoints

>/api/v1/station/date

Retrieves the temperature recorded at a specific station on a given date.

Parameters:
* station: The numerical ID of the weather station.
* date: The date in YYYYMMDD format.


* Response: A JSON object containing:
    
  * station: The station ID.
  * date: The requested date (formatted as YYYY-MM-DD).
  * temperature_in_date: The temperature on the specified date.
  * temperature_mean: The average temperature for the station across the dataset. 
  * temperature_max: The highest recorded temperature for the station. 
  * temperature_min: The lowest recorded temperature for the station.
>/api/v1/station

Returns all available temperature data for a selected station.

Parameters:

* station: The numerical ID of the weather station.

* Response: A JSON array, where each element is a dictionary representing a single temperature record (including date and temperature value).
>/api/v1/annual/station/year

Fetches temperature data for a specific station within a particular year.
Parameters:
* station: The numerical ID of the weather station.
* year: The desired year (e.g., 2023).


* Response: A JSON array of temperature records, filtered by the provided year. 
### Visualization

>/visualization/station/year

Generates a clear and informative line plot visualizing temperature trends for a given station throughout a selected year.
Parameters:
* station: The numerical ID of the weather station.
* year: The desired year for visualization.


* Response: Renders a PNG image of the visualization directly in the browser.
