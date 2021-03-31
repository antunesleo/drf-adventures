from thoughtsapi.celery import app


@app.task
def send_confirmation_email(user_email):
    print(f'SENT EMAIL TO {user_email}')
