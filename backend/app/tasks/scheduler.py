from app.core.celery_app import celery_app

@celery_app.task
def test_task():
    return {"status": "ok", "message": "Celery execution successful"}

@celery_app.task(queue="high_priority")
def fetch_critical_market_data():
    # Placeholder for high priority market data fetch
    pass
