# Scholars Novara

Scholars Novara is a social networking platform designed for students, staff, and alumni of an academic institution. It provides a space for community engagement, project collaboration, and sharing creative work.

## Features

The platform currently includes the following features:

*   **User Authentication:** Secure user signup, login, and logout.
*   **Home Feed:** A central feed displaying posts from all users.
*   **Posts with Media:** Users can create posts with text and upload images or videos.
*   **Comments:** Users can comment on posts.
*   **Likes:** Users can like posts.
*   **Saved Posts:** Users can save or bookmark posts for later.
*   **Communities:** Users can join and post within specific communities.
*   **Innovation Hub:** A section for users to pitch and support projects.
*   **Stories:** Users can post stories that are visible for 24 hours.

## Local Development Setup

To set up and run this project on your local machine, follow these steps.

### 1. Prerequisites

*   Python 3.8+
*   `pip` for package management
*   `virtualenv` (recommended)

### 2. Installation

Clone the repository to your local machine:
```bash
git clone <repository-url>
cd <repository-directory>
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Setup

The project uses Flask-Migrate to manage database schemas. To initialize your database for the first time, run the following command:
```bash
export FLASK_APP=app.py
flask db upgrade
```
This will create a `app.db` file in the `instance` folder and apply all existing migrations.

### 4. Running the Application

To start the Flask development server, run:
```bash
flask run
```
The application will be available at `http://127.0.0.1:5000`.

## Running Tests

A simple test script is provided to verify the authentication (signup and login) functionality. To run it:

1.  Make sure the application server is running in a separate terminal.
2.  In a new terminal, run the test script:
    ```bash
    python test_auth.py
    ```
You should see output indicating the success or failure of the signup and login tests.
