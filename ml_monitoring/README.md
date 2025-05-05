# ML Monitoring with FastAPI and Evidently AI

This project demonstrates how to integrate FastAPI with Evidently AI for ML model monitoring.

## Features

- REST API with FastAPI for ML predictions
- ML monitoring dashboard with Evidently AI
- PostgreSQL database for storing model predictions and metrics
- Docker support for containerized deployment
- Model performance monitoring
- Data drift detection

## Project Structure

```
ml_monitoring/
├── app/                # Main application package
│   ├── api/            # API related code
│   │   ├── routes/     # API route handlers
│   ├── core/           # Core functionality
│   │   ├── config.py   # Application settings
│   ├── db/             # Database related code
│   ├── models/         # ML models
│   ├── schemas/        # Pydantic models
│   ├── services/       # Service layer
│   └── templates/      # HTML templates for reports
├── data/               # Data directory
├── main.py             # Main application entry point
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## ML Monitoring Flow

```
┌──────────────┐       ┌───────────┐       ┌───────────────┐       
│              │       │           │       │               │       
│    Client    │──────▶│  FastAPI  │──────▶│  ML Model     │       
│              │       │    App    │       │  Predictions  │       
│              │◀──────│           │◀──────│               │       
└──────────────┘       └─────┬─────┘       └───────┬───────┘       
                             │                     │                
                             │                     │                
                             ▼                     ▼                
                      ┌────────────┐        ┌─────────────┐        
                      │            │        │             │        
                      │  Evidently │◀───────│  Database   │        
                      │  Reports   │        │  Storage    │        
                      │            │        │             │        
                      └────────────┘        └─────────────┘        
```

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd FAstAPI-Example-Project/ml_monitoring
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Access the API documentation at http://localhost:8000/docs

## Key Endpoints

- `POST /predict`: Generate model predictions
- `GET /monitor-model`: Generate model performance monitoring report
- `GET /monitor-target`: Generate target drift monitoring report

## Requirements

- Python 3.9+
- FastAPI
- Evidently AI
- PostgreSQL
- SQLAlchemy
- Pandas
- Scikit-learn
- Docker (optional)