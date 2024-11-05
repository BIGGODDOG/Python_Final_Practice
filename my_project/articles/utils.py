from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(user_email, article_title, comment_content):
    subject = f'Новый комментарий к статье: {article_title}'
    message = f'Ваш комментарий:\n\n{comment_content}\n\nПосмотрите на статью!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
