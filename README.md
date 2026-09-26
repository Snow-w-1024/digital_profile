# Digital Profile

A lightweight personal profile website built with FastAPI, MongoDB, and static HTML pages. It lets you display a public profile on the home page and update the content from a protected admin login page.

## Features

- Public profile page at `/`
- Admin login form at `/login.html`
- JWT-based authentication for protected profile updates
- MongoDB storage for profile content
- Docker Compose setup for quick local development

## Tech Stack

- Python 3
- FastAPI
- MongoDB
- PyMongo
- JWT / bcrypt
- Docker and Docker Compose

## Project Structure

```text
.
├── main.py                 # FastAPI app and API endpoints
├── static/
│   ├── index.html          # Public profile page
│   └── login.html          # Admin login and edit form
├── tool/
│   └── passwd.py           # Hashes the admin password
├── Dockerfile              # Container image definition
├── entrypoint.sh           # Generates ADMIN_HASH from ADMIN_PASSWORD
├── docker-compose.yml      # Local multi-container setup
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables
└── README.md               # Project documentation
```

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose
- Optional: Python 3.10+ for local non-Docker development

## Environment Variables

Create a `.env` file in the project root with values like:

```dotenv
MONGO_URI=mongodb://mongo:27017/profile_db
SECRET_KEY="your-long-random-secret-key"
ADMIN_PASSWORD=change-this-password
```

Notes:

- `MONGO_URI` points to the MongoDB container in Docker Compose.
- `SECRET_KEY` is used to sign the JWT used by the admin login flow.
- `ADMIN_PASSWORD` is the password that will be checked during login.
- `ADMIN_HASH` is generated automatically from `ADMIN_PASSWORD` by the startup script, so you normally do not set it manually.

## Running with Docker Compose

1. Make sure your `.env` file exists and contains the required values.
2. Start the application:

```bash
docker compose up --build
```

3. Open the app in a browser:

- Public profile: http://localhost:5000/
- Admin page: http://localhost:5000/login.html

The app runs on port `5000`.

## Local Development

If you want to run without Docker:

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start MongoDB locally or update `MONGO_URI` to a reachable database.
4. Run the app:

```bash
python main.py
```

## Application Behavior

### Public profile

`GET /api/profile` returns the stored profile data as JSON. The page at `/` renders the profile content on the website.

### Admin login

`POST /api/login` accepts:

```json
{
  "password": "your-admin-password"
}
```

If the password matches, the server returns a JWT token. The browser stores that token and uses it for protected updates.

### Updating the profile

`PUT /api/profile` updates the stored profile document. It requires a valid `Authorization: Bearer <token>` header.

## Default Profile Seed

On first startup, if the database is empty, the app creates a sample profile with:

- name: `.w.`
- message: `Hello, World!`
- bio: `this is a test text`
- skills: `do this, do that`

## Useful Commands

Start the stack:

```bash
docker compose up --build
```

Stop the stack:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

## Notes

- This project is intended as a simple personal profile/portfolio site.
- The admin page is intentionally minimal and can be expanded with a richer UI.
- The stored admin password is hashed at runtime from `ADMIN_PASSWORD` through the helper script.

## License

This project is provided as-is for personal or educational use.
