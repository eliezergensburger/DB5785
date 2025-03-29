# Docker Compose Setup for PostgreSQL, pgAdmin, and Python

This project sets up a development environment using Docker Compose to run PostgreSQL, pgAdmin, and a Python service. The Python service includes `psycopg2-binary` for interacting with the PostgreSQL database.

## Prerequisites

- Docker Desktop installed on your machine.
- Basic knowledge of Docker and Docker Compose.

## Project Structure
├── docker-compose.yml ├── Dockerfile ├── requirements.txt └── your-python-scripts/ └── your_script.py


## Services

### PostgreSQL

- **Image**: `postgres:15`
- **Environment Variables**:
  - `POSTGRES_USER`: Database username.
  - `POSTGRES_PASSWORD`: Database password.
  - `POSTGRES_DB`: Default database name.
- **Ports**: Exposes port `5432`.
- **Volumes**: Persists data using `postgres_data` volume.

### pgAdmin

- **Image**: `dpage/pgadmin4:6.21`
- **Environment Variables**:
  - `PGADMIN_DEFAULT_EMAIL`: Email for pgAdmin login.
  - `PGADMIN_DEFAULT_PASSWORD`: Password for pgAdmin login.
- **Ports**: Exposes port `5050`.
- **Depends On**: Starts after the PostgreSQL service.

### Python

- **Image**: Built from the provided `Dockerfile`.
- **Dependencies**: Installs `psycopg2-binary` and other Python packages from `requirements.txt`.
- **Volumes**: Mounts `your-python-scripts` directory to `/app`.
- **Command**: Runs `your_script.py`.

## Setup Instructions

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Create `requirements.txt`**: Ensure `requirements.txt` includes `psycopg2-binary`:

    ```
    psycopg2-binary
    ```

3. **Create `Dockerfile`**: Use the following Dockerfile:

    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["python", "your_script.py"]
    ```

4. **Modify `docker-compose.yml`**: Ensure your `docker-compose.yml` is set up as follows:

```yaml
   services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: db5785
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - pgnetwork

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: username@domain.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - pgnetwork

  python:
    image: python:latest
    volumes:
      - ./your-python-scripts:/app
    working_dir: /app
  #  command: python activities.py
    networks:
      - pgnetwork
    depends_on:
      - db

volumes:
  postgres_data:
    external: false

networks:
  pgnetwork:
```

5. **Run the Setup**: Navigate to the directory containing your `docker-compose.yml` file and run:

    ```bash
    docker-compose up --build
    ```

6. **Access pgAdmin**: Open your browser and go to `http://localhost:5050`. Log in using the email and password specified in the environment variables.

7. **Connect to PostgreSQL**: In pgAdmin, add a new server using the following details:
   - **Host**: `db`
   - **Port**: `5432`
   - **Username**: `yourusername`
   - **Password**: `mysecretpassword`

## Notes

- Ensure your Python script (`your_script.py`) is set up to interact with the PostgreSQL database.
- Adjust the `employee_id` range and sample data in your script as needed.
- an example of such a script: [activities.py](code/python/activities.py) to be modified as needed.

This setup provides a robust environment for developing applications that require a PostgreSQL database and a Python backend.

