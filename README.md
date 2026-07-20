# End-to-End Football-API Data Warehouse Solution

## Overview
A data pipeline that ingests fixture and match data from Football-API, consolidates it into a Snowflake data warehouse, and transforms it using dbt to support fixture-based analytics for the English Premier League across the 2022–2024 seasons.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Data Pipeline Details](#data-pipeline-details)
- [Scheduling and Orchestration](#scheduling-and-orchestration)
- [Known Limitations](#known-limitations)

## Architecture
Follows the medallion architecture, using AWS S3 Bucket for raw files, and Snowflake for the data warehouse.

```
[Football API] -> [Ingestion via API calls] -> [AWS S3 Bucket (Bronze Layer)] -> [Snowflake (Silver Layer)] -> [Snowflake w/ Star Schema (Gold Layer)]
```

## Data Sources
| Source Name | Type | Format | Frequency | Access Method |
|---|---|---|---|---|
| Football-API /leagues | API | JSON | Yearly | REST API  |
| Football-API /fixtures | API | JSON | Weekly | REST API |
| Football-API /teams | API | JSON | Yearly | REST API |

## Tech Stack
- **Languages:** Python, SQL
- **Orchestration:** Airflow
- **Transformation:**  dbt
- **Storage:** Snowflake, S3
- **Infrastructure:** Docker

## Project Structure
```
project-root/
├── dags/                                         # Orchestration DAGs
├── infra/                                        # Source code for ingestion
│   ├── extract/
│   ├── logger/
├── footballapi_sports_DEProject/                 # dbt scripts
├── scripts/                                      # Runner files for airflow
├── requirements.txt                              # Python dependencies
└── README.md
```

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sebinate/Football-Data-E2E.git
   cd Football-Data-E2E
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   or via conda
   ```bash
   conda create -p venv/ python=3.11 -y
   conda activate venv/
   ```
3. Install dependencies (for development):
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (see `.env.example` for required keys):
   ```bash
   cp .env.example .env
   ```

## Usage
Instructions for running the pipeline manually or triggering specific components.

```bash
docker compose up -d --build
# Go to http://localhost:8080 for Apache Airflow UI and Triggering dags
```

## Data Pipeline Details
- **Ingestion:** Uses the *requests* library of Python to extract certain API calls from [*Football-API*](https://www.api-football.com/)
- **Transformation:** Data Pipeline follows the medallion architecture
    - Bronze Layer: S3 Bucket - Every API call resposne gets stored here
    - Silver Layer: dbt then takes the raw S3 Json responses and converts them into cleaned, tabular versions stored as views in Snowflake
    - Gold Layer: dbt then again takes the cleaned data from the silver layer, and conforms it to the star schema defined in the Gold layer for business analytics
- **Loading:** Data is persisted in Snowflake, under the Gold layer with a star schema design, optimized for fast joins

## Scheduling and Orchestration
Apache Airflow is the choice tool for orchestration for this project. To run, head over to http://localhost:8080 (assuming that ```docker compose up -d --build``` has been ran) and trigger each dag manually first. The ```league_country``` will run Yearly (this dag handles the ingestion, and ), and the ```fixtures``` dag will run weekly.

## Known Limitations
The project is still not fully completed with the missing features:
- Monitoring and Observability
- Consumption layer via Dashboard
- Unit Testing