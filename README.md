# NYC Building Monitor

- This is the repo for the Backend API and database manager.
- For the frontend client, visit [https://github.com/0xStarcat/nyc_building_monitor_client](https://github.com/0xStarcat/nyc_building_monitor_client)

## Description

The NYC Building monitor is a tool that NYC tenants can use to help them make informed housing decisions and fight for housing justice.

## Setup

1.  Clone this repo and the [frontend repo](https://github.com/0xStarcat/nyc_building_monitor_client) into separate directories.
2.  Install dependencies for both repos with `npm install`
3.  Start the backend server with `npm run-script nodemon`
4.  Start the frontend client with `npm run-script dev`
5.  Visit `localhost:3000`

## Database Management
** Requires Python > 3.5 and Sqlite3 with FST5 and virtual environment
** And moving the seeding & migrations over to Alchemy rather than manual

1. Setup virtual environemnt in `python_scripts` directory
  - `python3 virtualenv venv`
  - activate it with `source venv/bin/activate`
  - install packages with `pip3 install requirements.txt`

2.  The database can be seeded with `python3 python_scripts/seed_db.py`
  - This can take about an hour
3.  Migrations are run with `python3 python_scripts/migrate.py`
4.  Database updates are `python3 python_scripts/update.py`
  - This is required to seed Violations and Service calls too
  - This could take a couple hours the first time.
  - I will find a way to host the sqlite file for download in the future.
5.  Tests are run with `python -m pytest`

## API

1.  Server can started for development with `npm run-script nodemon`, for production with `npm start` in a production environment with PM2 installed.
2.  Tests run with `npm test`


## Sources
Boroughs (clipped to shoreline)
http://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/nybb/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=geojson

Neighborhoods
http://data.beta.nyc/dataset/pediacities-nyc-neighborhoods/resource/35dd04fb-81b3-479b-a074-a27a37888ce7

Census tracts 2010 (clipped to shoreline)
https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/nyct2010/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=geojson

Income
http://app.coredata.nyc/?mlb=false&ntii=hh_inc_med_adj&ntr=Census%20Tract&mz=14&vtl=https%3A%2F%2Fthefurmancenter.carto.com%2Fu%2Fnyufc%2Fapi%2Fv2%2Fviz%2F691a2b7c-94d7-46ac-ac4d-9a589cb2c6ed%2Fviz.json&mln=true&mlp=true&mlat=40.718&ptsb=&nty=2012-2016&mb=roadmap&pf=%7B%22subsidies%22%3Atrue%7D&md=table&mlv=false&mlng=-73.996&btl=Borough&atp=neighborhoods

Rent
http://app.coredata.nyc/?mlb=false&ntii=rent_gross_med_adj&ntr=Census%20Tract&mz=14&vtl=https%3A%2F%2Fthefurmancenter.carto.com%2Fu%2Fnyufc%2Fapi%2Fv2%2Fviz%2F691a2b7c-94d7-46ac-ac4d-9a589cb2c6ed%2Fviz.json&mln=true&mlp=true&mlat=40.718&ptsb=&nty=2012-2016&mb=roadmap&pf=%7B%22subsidies%22%3Atrue%7D&md=table&mlv=false&mlng=-73.996&btl=Borough&atp=neighborhoods

Race
https://www1.nyc.gov/site/planning/data-maps/nyc-population/census-2010.page
