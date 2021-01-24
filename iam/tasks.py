from celery import shared_task


@shared_task
def send_confirmation_email(user_email):
    print(f'SENT EMAIL TO {user_email}')
