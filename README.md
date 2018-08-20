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

** I'm working on moving the seeding & migrations over to Alembic.

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
