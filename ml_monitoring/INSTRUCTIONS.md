# ML Monitoring Project Setup Instructions

This document provides step-by-step instructions for setting up and running the ML Monitoring project based on the Evidently AI tutorials for batch monitoring architecture with Prefect and Grafana.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (recommended for containerized deployment)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FAstAPI-Example-Project/ml_monitoring
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Synthetic Data

```bash
python generate_data.py
```

This script will:
- Generate synthetic data for training and testing
- Train a simple linear regression model
- Save the model and data to the `data/` directory

### 5. Run the Application

#### Option 1: Using Python directly

This will start the FastAPI application and embedded Prefect server:

```bash
python main.py
```

#### Option 2: Using Docker Compose (Recommended)

This will start the entire monitoring stack including FastAPI, PostgreSQL, Prefect, and Grafana:

```bash
docker-compose up --build
```

### 6. Access the Applications

- FastAPI Web Dashboard: http://localhost:8000/
- API Documentation: http://localhost:8000/docs
- Prefect UI: http://localhost:4200
- Grafana Dashboard: http://localhost:3000 (admin/admin)

## Using Prefect for Scheduled Monitoring

The application automatically sets up scheduled Prefect workflows:

1. **Batch Prediction Pipeline**: Runs every 6 hours
   - Processes new data and generates predictions
   
2. **Data Monitoring Pipeline**: Runs every 12 hours
   - Checks for data quality issues and data drift
   
3. **Model Monitoring Pipeline**: Runs daily
   - Evaluates model performance metrics
   
4. **Full Monitoring Pipeline**: Runs weekly
   - Comprehensive monitoring that includes all of the above

You can manually trigger these pipelines from the web dashboard or Prefect UI.

## Using Grafana Dashboards

Two pre-configured Grafana dashboards are included:

1. **Model Performance Dashboard**:
   - Tracks RMSE, MAE, and R² scores over time
   - Displays current model performance metrics

2. **Data Drift Dashboard**:
   - Monitors feature drift over time
   - Shows feature distribution changes
   - Alerts on detected drift

Default Grafana credentials: `admin`/`admin`

## Testing the API

You can test the API using the provided test script:

```bash
python test_api.py
```

This script will:
- Make predictions using the API
- Update actual values for some predictions
- Generate model performance and data drift reports
- Test the Prefect integration

## Project Structure

```
ml_monitoring/
├── app/                # Main application package
│   ├── api/            # API related code
│   │   ├── routes/     # API route handlers
│   ├── core/           # Core functionality
│   ├── db/             # Database related code
│   ├── models/         # ML models
│   ├── schemas/        # Pydantic models
│   ├── services/       # Service layer
│   ├── templates/      # HTML templates for reports
│   └── workflows/      # Prefect workflow definitions
│       └── tasks/      # Prefect task definitions
├── data/               # Data directory
├── grafana/            # Grafana configuration
│   ├── dashboards/     # Pre-configured dashboards
│   └── provisioning/   # Datasources and dashboard provisioning
├── main.py             # Main application entry point
├── generate_data.py    # Script to generate synthetic data
├── test_api.py         # Script to test the API
├── run_prefect_server.py # Script to run Prefect server
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker configuration
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Key API Endpoints

- `POST /api/v1/predictions/predict`: Generate model predictions
- `POST /api/v1/predictions/update-actual-value`: Update actual values for past predictions
- `GET /api/v1/predictions/predictions`: Get historical predictions
- `GET /api/v1/monitoring/monitor-model`: Generate model performance monitoring report
- `GET /api/v1/monitoring/monitor-target`: Generate target drift monitoring report
- `GET /api/v1/monitoring/metrics`: Get model performance metrics
- `GET /api/v1/monitoring/run-batch-predictions`: Trigger batch prediction pipeline
- `GET /api/v1/monitoring/run-all-pipelines`: Trigger all monitoring pipelines
- `GET /api/v1/monitoring/prefect-status`: Check Prefect server status

## Scaling the Project

To scale this project for production:

1. **Scaling with Prefect**:
   - Move Prefect to a dedicated server or cloud deployment
   - Use work queues for distributed execution
   - Implement deployment-specific settings

2. **Database Scaling**:
   - Set up PostgreSQL replication
   - Implement database sharding for metrics storage
   - Use connection pooling

3. **Application Scaling**:
   - Deploy multiple FastAPI instances behind a load balancer
   - Use Redis for caching and job queues
   - Implement horizontal scaling with Kubernetes

## Next Steps

1. Replace the synthetic data with your real dataset
2. Implement more sophisticated ML models
3. Add authentication for the API
4. Set up alerts in Grafana for critical metrics
5. Extend Prefect workflows for more advanced monitoring scenarios
6. Set up email notifications for monitoring alerts

## Troubleshooting

- If Prefect server doesn't start automatically, run it manually: `prefect server start`
- If Grafana dashboards aren't loading, check that PostgreSQL is properly initialized
- For Docker-related issues, check the Docker logs with `docker-compose logs`
- If metrics aren't showing in Grafana, check the database connection and ensure data is being collected