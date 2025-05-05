from prefect import flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
import datetime
import logging

from app.workflows.prediction_pipeline import batch_prediction_pipeline
from app.workflows.monitoring_pipeline import data_monitoring_pipeline, model_monitoring_pipeline, full_monitoring_pipeline

logger = logging.getLogger(__name__)

@flow(name="Create Scheduled Pipelines")
def create_scheduled_pipelines():
    """Create and deploy scheduled pipelines."""
    logger.info("Creating scheduled pipelines")
    
    # Create batch prediction deployment with schedule
    prediction_deployment = Deployment.build_from_flow(
        flow=batch_prediction_pipeline,
        name="scheduled-batch-predictions",
        schedule=CronSchedule(cron="0 */6 * * *"),  # Every 6 hours
        tags=["ml", "predictions"]
    )
    prediction_url = prediction_deployment.apply()
    logger.info(f"Deployed batch prediction pipeline: {prediction_url}")
    
    # Create data monitoring deployment with schedule
    data_monitoring_deployment = Deployment.build_from_flow(
        flow=data_monitoring_pipeline,
        name="scheduled-data-monitoring",
        schedule=CronSchedule(cron="0 */12 * * *"),  # Every 12 hours
        tags=["ml", "monitoring", "data"]
    )
    data_monitoring_url = data_monitoring_deployment.apply()
    logger.info(f"Deployed data monitoring pipeline: {data_monitoring_url}")
    
    # Create model monitoring deployment with schedule
    model_monitoring_deployment = Deployment.build_from_flow(
        flow=model_monitoring_pipeline,
        name="scheduled-model-monitoring",
        schedule=CronSchedule(cron="0 0 * * *"),  # Daily at midnight
        tags=["ml", "monitoring", "model"]
    )
    model_monitoring_url = model_monitoring_deployment.apply()
    logger.info(f"Deployed model monitoring pipeline: {model_monitoring_url}")
    
    # Create full monitoring deployment with schedule
    full_monitoring_deployment = Deployment.build_from_flow(
        flow=full_monitoring_pipeline,
        name="scheduled-full-monitoring",
        schedule=CronSchedule(cron="0 0 * * 1"),  # Weekly on Monday
        tags=["ml", "monitoring", "full"]
    )
    full_monitoring_url = full_monitoring_deployment.apply()
    logger.info(f"Deployed full monitoring pipeline: {full_monitoring_url}")
    
    return {
        "prediction_url": prediction_url,
        "data_monitoring_url": data_monitoring_url,
        "model_monitoring_url": model_monitoring_url,
        "full_monitoring_url": full_monitoring_url
    }

@flow(name="Manual Run All Pipelines")
def run_all_pipelines():
    """Manually run all pipelines in sequence."""
    logger.info("Running all pipelines")
    
    # Run batch prediction pipeline
    prediction_result = batch_prediction_pipeline()
    logger.info(f"Batch prediction pipeline completed: {prediction_result}")
    
    # Run full monitoring pipeline
    monitoring_result = full_monitoring_pipeline()
    logger.info(f"Full monitoring pipeline completed")
    
    return {
        "prediction_result": prediction_result,
        "monitoring_result": monitoring_result
    }

if __name__ == "__main__":
    # Create scheduled pipelines
    create_scheduled_pipelines()