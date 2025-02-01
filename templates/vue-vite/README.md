# {{ project_name }}
Template for a django project that uses vite and vue

## Requirements
- Python 3.9+
- NPM 7.0+
- Docker 20.10+

## Installation
1. Clone the repository
2. In an IDE of your choice, open the project folder
3. Create a virtual environment. There are many ways to do this, but here is one way:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the Python dependencies
    ```bash
   cd src 
   pip install -r requirements.txt
    ```
5. Run migrations
    ```bash
    python manage.py migrate
    ```
6. Run the backend server
    ```bash
    python manage.py runserver
    ```
7. In a new terminal, navigate to the assets folder and install the NPM dependencies
    ```bash
    cd src/assets
    npm install
    ```
8. Run the frontend server
    ```bash
    npm run dev
    ```

