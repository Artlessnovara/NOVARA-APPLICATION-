# Scholars Novara Institute - Web Application

This is the official web application for the Scholars Novara Institute, a modern, feature-rich platform designed to foster education, innovation, and community among students, staff, and alumni.

## Features

This application is being built in multiple phases, with current and planned features including:
-   User Authentication (Login, Sign Up, Forgot Password)
-   Dynamic Home Feed with posts, comments, likes, and bookmarks
-   User Profiles with Following system and Certificate showcase
-   Community Hubs for collaboration
-   Innovation Hub for projects and startups
-   Creativity Hub for sharing art, music, and writing
-   Advanced Search functionality

## Project Structure

The application is built with Python using the Flask web framework.

-   **Backend:** Flask, SQLAlchemy (for database ORM), Flask-Migrate (for database migrations).
-   **Frontend:** HTML, CSS, JavaScript, Bootstrap.
-   **Database:** SQLite (for development).

## Setup and Installation

To run this application locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    The required Python packages are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    The application uses Flask-Migrate to manage the database schema. To create the database and apply all migrations, run:
    ```bash
    flask db upgrade
    ```
    *Note: If the `flask` command is not found, you can use `python -m flask db upgrade`.*

5.  **Run the Application:**
    You can run the development server with the following command:
    ```bash
    flask run
    ```
    *Or, alternatively: `python -m flask run`*

    The application will be available at `http://127.0.0.1:5000`.
