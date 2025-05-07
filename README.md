# Cura

Cura is a Flask-based web application for managing patient medication and mentorships.

## Project Structure

- `app/`: Contains the main Flask application code including:
  - `app.py`: Application factory and extension setup.
  - `config.py`: Configuration settings.
  - `models.py`: Database models.
  - `routes.py`: Application routes.
  - `run.py`: Entry point to run the app.
- `static/`: Static files such as CSS, JavaScript, images.
- `templates/`: HTML templates for rendering views.
- `.venv/`: Python virtual environment (should be ignored by git).
- `.gitignore`: Git ignore rules.
- `requirements.txt`: Python dependencies.

## Prerequisites

- Python 3.7 or higher
- SQLite (default database)
- Git

## Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd Cura
```

2. **Create and activate a virtual environment**

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables**

Create a `.env` file in the app directory and add:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./CuraDB.db
```

Replace `your_secret_key_here` with a secure secret key.

5. **Initialize the database**

Use Flask-Migrate commands to set up the database schema:

```bash
cd app
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

6. **Run the application**

```bash
python app/run.py
```

The app will be accessible at `http://127.0.0.1:5000/`.

## Notes

- The `.gitignore` file excludes the virtual environment directory `.venv/`, environment files `.env`, and the SQLite database file `MediMateDB.db`.
- Static files are served from the `/static` URL path.
- Templates are located in the `templates/` folder.
- Routes are currently defined in `app/routes.py` without Blueprints for simplicity.
- Use the Flask-Migrate commands to manage database migrations.


