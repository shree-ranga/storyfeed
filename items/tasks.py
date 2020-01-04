from storyboard.celery import celery_app as app


@app.task(bind=True)
def add_task(x, y):
    return x + y
