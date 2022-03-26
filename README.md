# HDB Resale data (Dash)board

Simple dashboard made from Dash to visualize some aspect of Singapore HDB resale data.

## Getting the data

The data can be downloaded from, https://data.gov.sg/dataset/resale-flat-prices using requests library.

    import requests
    r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=42ff9cfe-abe5-4b54-beda-c88f9bb438ee")
    r.json()
    
## Demo

The dashboard is currently hosted on Heroku at, https://damp-stream-44319.herokuapp.com/

![Screenshots](/Screenshots/Screenshots.png?raw=true "Dashboard")