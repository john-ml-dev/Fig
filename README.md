## Project Overview

![architecture_pipeline](https://github.com/john-ml-dev/Flightradar24/assets/78201996/3dbaca14-6421-4822-b8c8-f9287ffac707)

### Data Gathering

- **Source**: Data is gathered from [flightradar24.com](https://www.flightradar24.com) using Scrapy.
- **Reason for Choosing Scrapy**: Scrapy was chosen for its simplicity and effective handling of cookies.

### Scheduling

- **Tool**: Airflow is used to schedule the scraping process.
- Apache Airflow is used for orchestrating the workflow, managing task dependencies, scheduling, and monitoring the data pipeline.
- Airflow handles the execution of each step in the pipeline, ensuring tasks are run in the correct order and handling retries and failures.
- **Frequency**: The project is scheduled to run daily.

### Containerization

- **Tool**: Docker is used to containerize the project.
- **Reason for Choosing Docker**: Docker simplifies the setup and ensures replicability of the project across different operating systems.
-------------

This document outlines the setup and usage instructions for the **Flight** project. Follow the steps below to clone the repository, set up the environment, and run the project.

## Directory Structure

```plaintext
FLIGHT/
├── Airflow/
│   ├── dags/
│   ├── logs/
│   ├── pg-init-scripts/
│   ├── plugins/
│   ├── scripts/
│   └── sql/
├── Flight/
├── test/
├── .env
├── docker-compose.yml
├── dockerfile
├── requirements.txt
└── .gitignore

```

# Setup Instructions

## 1. Clone the Repository
Clone the repository to your local machine using the following command:
```sh
git clone https://github.com/john-ml-dev/Flightradar24
```
## 2. Change Directory to Airflow
Navigate to the Airflow directory:
```sh
cd Airflow
```
## 3. Build the Docker Image
Build the Docker image with the tag `scrapy_airflow:latest`:
```sh
docker compose build --tag scrapy_airflow:latest
```
## 4. Update `.env` with S3 Credentials
Update the `.env` file with your AWS S3 credentials. This file should contain the necessary environment variables for accessing your S3 bucket.

## 5. Start the Docker Containers
Whiles your docker desktop is running in the background, start the Docker containers in detached mode:
```sh
docker compose up -d
```
## 6. Access the Airflow UI
Open your web browser and go to http://localhost:8080 to access the Airflow UI.

## 7. Update the PostgreSQL Connection
In the Airflow UI, navigate to Admin > Connections and update the postgres_default connection with the following details:

Port: 5433
User: `airflow`
Password: `airflow`
Database: `airflow`
Save the changes.

## 8. Connect to PostgreSQL
Use a SQL tool such as DBeaver or Valentina Studio to connect to the PostgreSQL database. Enter the connection details as specified above.

## 9. Verify S3 Upload


