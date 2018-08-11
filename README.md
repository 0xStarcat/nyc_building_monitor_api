# NYC Building Monitor

- This is the repo for the Backend API and database manager.
- For the frontend client, visit [https://github.com/0xStarcat/nyc_building_monitor_client](https://github.com/0xStarcat/nyc_building_monitor_client)

## Description

The NYC Building monitor is a tool that NYC tenants can use to help them make informed housing decisions and fight for housing justice.

## Setup

1.  Clone this repo and the [frontend repo](https://github.com/0xStarcat/nyc_building_monitor_client) into separate directories.
2.  Install dependencies for both repos with `npm install`
3.  Start the backend server with `yarn nodemon`
4.  Start the frontend client with `yarn dev`
5.  Visit `localhost:3000`

## Database Management

1.  The database can be seeded with `python3 python_scripts/seed_db.py`
2.  Migrations are run with `python3 python_scripts/migrate.py`
3.  Database updates are `python3 python_scripts/update.py`
4.  Tests are run with `pytest`

## API

1.  Server can started for development with `yarn nodemon`, for production with `yarn start` in a production environment with PM2 installed.
2.  Tests run with `yarn test`
