# Scholars Novara Application

This is a Flask-based web application for the Scholars Novara Institute.

## Prerequisites

- Python 3.10 or higher
- pip

## Project Setup

These instructions are for setting up the project on a Windows machine.

### 1. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with system-wide packages.

Open your command prompt in the project's root directory and run the following commands:

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
.\\venv\\Scripts\\activate
```

You will know the virtual environment is active when you see `(venv)` at the beginning of your command prompt line.

### 2. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Database Management

This project uses Flask-Migrate to handle database schema changes. The following commands use a robust method that avoids environment issues.

### First-Time Setup / Applying Migrations

If you are setting up the database for the first time, or if there are new migrations to apply, run the `upgrade` command. This will create the database and apply all migrations.

```bash
python -m flask --app app:create_app db upgrade
```

### Creating New Migrations (for developers)

When you make changes to the database models in `models.py`, you need to generate a new migration script.

```bash
python -m flask --app app:create_app db migrate -m "A short message describing the changes"
```
After generating a migration, run the `upgrade` command above to apply it.

## Running the Application

To start the Flask development server, run the following command:

```bash
python -m flask --app app:create_app run
```

The application will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the automated tests for the application, use this command:

```bash
python -m unittest test_app_auth.py
```
