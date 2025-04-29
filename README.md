# ETL-Project-OpenLibrary-Data-Pipeline
📚 Project Overview
This project is a Data Engineering ETL pipeline that automates the process of fetching book data related to Data Engineering from the OpenLibrary API, processes it, and stores it into a PostgreSQL database — orchestrated and scheduled using Apache Airflow.

The project is containerized using Docker, simulating a production-ready cloud-like environment locally with full data orchestration, task dependency management, and database persistence.
Awesome — I'm really happy to see how you drove it to full working setup yourself — that's **real engineer behavior.** 🔥

Now, let’s build you a **full professional GitHub README** for this ETL project.

I'll break it down like a real-world project:

---
# 📄 GitHub README.md

# OpenLibrary Books ETL Pipeline

## 📚 Project Overview

This project is a **Data Engineering ETL pipeline** that automates the process of fetching book data related to **Data Engineering** from the **OpenLibrary API**, processes it, and stores it into a **PostgreSQL** database — orchestrated and scheduled using **Apache Airflow**.

The project is containerized using **Docker**, simulating a production-ready cloud-like environment locally with full data orchestration, task dependency management, and database persistence.

---

## ⚙️ Tech Stack Used

- **Docker** — containerization of the full environment
- **Apache Airflow 3.0** — ETL orchestration and scheduling
- **PostgreSQL** — data storage for books information
- **PgAdmin4** — database management GUI
- **Redis** — message broker for Airflow CeleryExecutor
- **Python** — API fetching, data transformation
- **Command Line Interface (CLI)** — full environment control and troubleshooting

---

## 🏗️ Architecture Overview

```
User
 ↓
Local Machine (Docker Engine)
 ├── Airflow Scheduler (DAGs)
 │     ├── Fetch data from OpenLibrary API
 │     ├── Create Books table if not exists
 │     └── Insert transformed book data into Postgres
 ├── Airflow Webserver (UI at localhost:8080)
 ├── PostgreSQL Database (books table)
 ├── PgAdmin Server (DB GUI at localhost:5050)
 └── Redis Server (for Celery messaging)
```

---
### 🖼️ Architecture Diagram

Here’s a simple flowchart:

```
                +-------------------+
                |   OpenLibrary API  |
                +---------+---------+
                          |
                          v
                +-------------------+
                |    Airflow DAG     |
                |  fetchstore_openlibrary_books |
                +---------+---------+
                          |
             +------------+------------+
             |                         |
+---------------------+      +-----------------------+
|  Create Table Task   |      |   Insert Book Data Task |
+---------------------+      +-----------------------+
             \                         /
              \                       /
               \                     /
                v                   v
              +-------------------------+
              |   PostgreSQL Database    |
              |       (books table)       |
              +-------------------------+
```

---
## 🛠️ How It Works

1. **Airflow DAG** is scheduled to run **once daily** (`schedule=timedelta(days=1)`).
2. On execution:
   - **Task 1**: Fetches top 50 books related to "data engineering" from **OpenLibrary API**.
   - **Task 2**: Creates the `books` table if it does not exist.
   - **Task 3**: Inserts the fetched book records into the Postgres database.
3. **PgAdmin** is used to visually verify and manage the Postgres database.

---

## 🧠 What I Learned

- **Containerization with Docker**  
  Spinning up Airflow, Postgres, Redis, and PgAdmin in isolated containers, managing them with Docker Compose.

- **Airflow DAGs and Operators**  
  Creating ETL workflows with PythonOperator and SQLExecuteQueryOperator, building dependencies between tasks.

- **Local Server Setup**  
  Setting up and configuring local services to mimic cloud deployments using volumes, ports, and environment variables.

- **Command Line Usage**  
  Using Docker CLI, Bash commands, Airflow CLI to control containers, execute tasks, and debug issues.

- **Database Management**  
  Creating tables, inserting records, and troubleshooting connection issues inside PostgreSQL.

- **Troubleshooting and Debugging**  
  Diagnosing issues like container IP conflicts, Airflow DAG disappearances, permission errors, and database connectivity problems.

- **Scheduling and Automation**  
  Setting up repeatable daily automation for data extraction and persistence.

---

## 🚀 Future Improvements

- Add **Data Quality Checks** to validate incoming API data before inserting.
- Implement **Deduplication Logic** to avoid repeated entries.
- Use **AWS S3** or other cloud storage for backup of database dumps.
- Add **Docker Healthchecks** for Airflow containers.
- Expand DAG to include **transformations** like normalizing author names, rating analysis, etc.

---

## 📦 Quick Start

```bash
# Clone the project
git clone https://github.com/yourusername/openlibrary-etl.git
cd openlibrary-etl

# Start all containers
docker-compose up -d

# Access Airflow
localhost:8080 (Username: airflow, Password: airflow)

# Access PgAdmin
localhost:5050 (Email: admin@admin.com, Password: admin)
```

---

# 📢 Final Important Note

> This project is intended for **learning and development purposes**.  
> Not optimized for production usage yet (e.g., security, scaling).

---

---
# 📌 Quick Summary

| Category | Description |
|:---|:---|
| Type | End-to-end ETL pipeline |
| Tech | Docker + Airflow + Postgres + Redis |
| Purpose | Fetch Data Engineering book data, store into SQL database |
| Main Skills Gained | Containerization, Orchestration, Scheduling, Database Management, Automation |

---

# 🚀 End

---
---

