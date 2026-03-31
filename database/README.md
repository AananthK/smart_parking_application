# Smart Parking System – Database Setup
## Prerequisites
Before setting up the database, ensure you have:

PostgreSQL installed
OR any PostgreSQL-compatible database (e.g., Supabase, Neon)
A database management tool (e.g., pgAdmin, DBeaver, or psql)

## Setup Instructions
### 1. Create a Database

Create a new database in PostgreSQL.

Example using psql:

    CREATE DATABASE smart_parking;
### 2. Open Query Tool

Open your preferred database tool (e.g., pgAdmin Query Tool Workspace) and connect to the newly created database.

### 3. Run SQL Scripts

Execute the following SQL scripts in order to initialize the database:

    create_tables.sql
    insert_lots.sql
    insert_parking_spots.sql
    insert_vehicles.sql

⚠️ Run the scripts in this exact order to avoid foreign key constraint errors.

## Notes
The database schema is designed for a simulation-based smart parking system
Parking spots are pre-generated for each lot
Test vehicles are included to simulate occupancy
Ticket creation and occupancy updates are handled in the application logic