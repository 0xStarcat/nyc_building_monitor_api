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
** Requires Python > 3.5 and Sqlite3 with FST5
** I'm working on bundling everything into the virtualenv pattern
** And moving the seeding & migrations over to Alchemy rather than manual

1.  The database can be seeded with `python3 python_scripts/seed_db.py`
2.  Migrations are run with `python3 python_scripts/migrate.py`
3.  Database updates are `python3 python_scripts/update.py`
4.  Tests are run with `pytest`

## API

1.  Server can started for development with `npm run-script nodemon`, for production with `npm start` in a production environment with PM2 installed.
2.  Tests run with `npm test`
