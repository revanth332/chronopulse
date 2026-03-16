# ChronoPulse

ChronoPulse is a distributed log analysis and monitoring backend built with **FastAPI, PostgreSQL, Celery, and Redis**.
It processes uploaded log files asynchronously, computes operational metrics (error rate, latency), and generates alerts when configured thresholds are exceeded.

The system is designed to demonstrate **real-world backend architecture patterns** including background job processing, idempotent task execution, distributed workers, and failure recovery.

---

# Overview

ChronoPulse allows users to:

1. Define monitoring jobs with thresholds.
2. Upload application log files.
3. Create processing executions for uploaded files.
4. Analyze logs asynchronously using worker processes.
5. Generate alerts when error rate or latency thresholds are exceeded.
6. Automatically recover stuck executions using scheduled background checks.

---

# Architecture

ChronoPulse follows a layered backend architecture.

```
FastAPI (API Layer)
       │
       ▼
PostgreSQL (Metadata Storage)
       │
       ▼
Celery Task Queue
       │
       ▼
Redis (Message Broker)
       │
       ▼
Worker Processes
       │
       ▼
Alert Generation
```

### Key Components

- **FastAPI** – REST API for managing jobs, files, and executions
- **PostgreSQL** – stores metadata, executions, and alerts
- **Celery** – distributed task queue for background processing
- **Redis** – message broker for Celery
- **Workers** – process log files asynchronously
- **Celery Beat** – scheduled tasks (stale execution recovery)

---

# Core Features

### Log File Processing

- Supports streaming log parsing
- Handles large files efficiently
- Extracts operational metrics

### Threshold Monitoring

Jobs can define thresholds such as:

- error rate threshold
- latency threshold

Alerts are triggered when metrics exceed these thresholds.

### Asynchronous Processing

Log analysis runs in background workers using Celery.

```
Create Execution
      ↓
Celery Task Published
      ↓
Worker Processes File
      ↓
Alerts Generated
```

### Idempotent Task Execution

Tasks can safely retry without corrupting system state.

Duplicate alerts are prevented using database constraints.

### Automatic Failure Recovery

ChronoPulse detects and recovers stuck executions.

If a worker crashes:

```
Execution RUNNING
      ↓
Timeout exceeded
      ↓
Recovery task resets execution
      ↓
Execution requeued
```

---

# Project Structure

```
chronopulse/
│
├── app/
│   ├── main.py
│   ├── celery_app.py
│
│   ├── api/
│   │   ├── jobs.py
│   │   ├── files.py
│   │   └── executions.py
│
│   ├── models/
│   │   ├── job.py
│   │   ├── file.py
│   │   ├── job_execution.py
│   │   └── alert.py
│
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── db/
│   └── storage/
│
├── uploads/
├── alembic/
├── requirements.txt
└── README.md
```

---

# Database Schema

## Jobs

Stores monitoring configurations.

| Column            | Description            |
| ----------------- | ---------------------- |
| id                | Job identifier         |
| name              | Job name               |
| error_threshold   | Allowed error rate     |
| latency_threshold | Allowed latency        |
| is_active         | Whether job is enabled |

---

## Files

Stores uploaded log metadata.

| Column       | Description        |
| ------------ | ------------------ |
| id           | File identifier    |
| filename     | Original filename  |
| size_bytes   | File size          |
| checksum     | File hash          |
| storage_path | Local storage path |

---

## Job Executions

Represents a processing run.

| Column       | Description                          |
| ------------ | ------------------------------------ |
| id           | Execution identifier                 |
| job_id       | Associated job                       |
| file_id      | Processed file                       |
| status       | PENDING / RUNNING / SUCCESS / FAILED |
| started_at   | Execution start time                 |
| completed_at | Execution completion time            |

---

## Alerts

Generated when thresholds are exceeded.

| Column       | Description       |
| ------------ | ----------------- |
| id           | Alert identifier  |
| execution_id | Related execution |
| alert_type   | Type of alert     |
| message      | Alert description |

---

# Log Format

ChronoPulse currently supports a simple log format:

```
GET /users 200 120ms
GET /orders 500 340ms
GET /login 200 80ms
```

Fields:

```
METHOD PATH STATUS LATENCY
```

Example:

```
GET /orders 500 340ms
```

---

# API Endpoints

## Create Job

```
POST /jobs
```

Example:

```json
{
  "name": "API Monitor",
  "error_threshold": 5,
  "latency_threshold": 200
}
```

---

## Upload File

```
POST /files
```

Uploads log files for analysis.

---

## Create Execution

```
POST /executions
```

Creates a log processing execution.

---

## Get Execution Status

```
GET /executions/{execution_id}
```

Returns execution status and metrics.

---

# Running the Project

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Start Redis

```
redis-server
```

---

## Start FastAPI

```
uvicorn app.main:app --reload
```

---

## Start Celery Worker

```
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
```

---

## Start Celery Beat (Scheduler)

```
celery -A app.celery_app.celery_app beat --loglevel=info
```

---

# Failure Recovery

ChronoPulse automatically recovers executions that remain in `RUNNING` state longer than the configured timeout.

Recovery flow:

```
RUNNING execution
       ↓
timeout exceeded
       ↓
execution reset to PENDING
       ↓
task requeued
```

This ensures the system remains fault tolerant.

---

# Future Improvements

Possible extensions include:

- Email or webhook alert delivery
- Object storage integration (S3 / Azure Blob)
- Docker-based deployment
- Metrics and monitoring dashboards
- File deduplication using checksums
- Execution progress tracking
- Table partitioning for large-scale data

---

# Purpose of the Project

ChronoPulse was built to demonstrate practical backend system design concepts such as:

- asynchronous job processing
- distributed workers
- idempotent task execution
- failure recovery mechanisms
- scalable architecture patterns

It serves as a learning project for building **production-style backend systems**.

---

# License

This project is intended for educational and demonstration purposes.
