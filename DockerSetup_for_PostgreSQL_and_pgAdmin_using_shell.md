## 1. **Pull the PostgreSQL Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull postgres:latest
   ```

## 2. **Create a Docker Volume**
   Create a Docker volume to persist PostgreSQL data:

   ```bash
   docker volume create postgres_data
   ```

   This volume will ensure data persistence, even if the container is removed.

## 3. **Run the PostgreSQL Container**
   Start the PostgreSQL container using the following command:

   ```bash
   docker run -d --name my_postgres -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=db5785 -p 5432:5432 -v postgres_data:/var/lib/postgresql/data postgres
   ```

   Replace `your_password` with a secure password for the PostgreSQL superuser (`postgres`).

   - The `-v postgres_data:/var/lib/postgresql/data` flag mounts the `postgres_data` volume to the container's data directory, ensuring data persistence.

## 4. **Verify the Container**
   To confirm the container is running, use:

   ```bash
   docker ps
   ```

   You should see the `postgres` container listed.

---

# Setting Up pgAdmin with Docker

## 1. **Pull the pgAdmin Docker Image**
   Download the official PostgreSQL Docker image with the following command:

   ```bash
   docker pull dpage/pgadmin4:latest
   ```

## 2. **Run the pgAdmin Container**
   Start the pgAdmin container using the following command:

   ```bash
   docker run -d --name pgadmin -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin123
   ```

   Replace `5050` with your desired port, and `admin@example.com` and `admin123` with your preferred email and password for pgAdmin.

   - The `-p 5050:80` flag maps port `5050` on your host machine to port `80` inside the container (where pgAdmin runs).


## 3. **Access pgAdmin**
   Open your browser and go to:

   ```
   http://localhost:5050
   ```

   Log in using the email and password you set.

---

# Accessing PostgreSQL via pgAdmin

finding Host address: 
  ```bash
  docker inspect --format='{{.NetworkSettings.IPAddress}}' postgres
  ```

## 1. **Connect to the PostgreSQL Database**
   - After logging into pgAdmin, click on **Add New Server**.
   - In the **General** tab, provide a name for your server (e.g., `PostgreSQL Docker`).
   - In the **Connection** tab, enter the following details:
     - **Host name/address**: `postgres` (or the name of your PostgreSQL container). [usually  172.17.0.2 on windows]
     - **Port**: `5432` (default PostgreSQL port).
     - **Maintenance database**: `postgres` (default database).
     - **Username**: `postgres` (default superuser).
     - **Password**: The password you set for the PostgreSQL container (e.g., `your_password`).
   - Click **Save** to connect.

## 2. **Explore and Manage the Database**
   - Once connected, you can:
     - Create and manage databases.
     - Run SQL queries using the **Query Tool**.
     - View and edit tables, views, and stored procedures.
     - Monitor database activity and performance.

---
