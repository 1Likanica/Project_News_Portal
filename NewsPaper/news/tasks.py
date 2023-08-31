from celery import shared_task
import time
from .models import *
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.contrib.auth.models import User
from django.template.loader import render_to_string




@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def my_job():
    one_week_ago = datetime.today() - timedelta(days=7)
    postnewsweekly = Post.objects.filter(dateCreation__gte=one_week_ago)
    print(postnewsweekly)
    categoriesall = Category.objects.all()
    print(categoriesall)
    for cat_here in categoriesall:
        print('  --- SCHEDULER ---', cat_here)
        postnewsweeklycats = Post.objects.filter(dateCreation__gte=one_week_ago, postCategory=cat_here)
        text4email = ''
        html4email = ''
        for p in postnewsweeklycats:
            text4email += (f'Заголовок: {p.title}\n' \
                           f'Ссылка на статью: http://127.0.0.1:8000{p.get_absolute_url()}\n')
            html4email += (f'Заголовок: {p.title}<br>'
                           f'<a href="http://127.0.0.1:8000{p.get_absolute_url()}">'
                           f'Ссылка на статью</a><br>')
        print(text4email)
        print(html4email)

        emails = User.objects.filter(
            subscriptions__category=cat_here
        ).values_list('email', flat=True)

        subject = f'Все новости за неделю в категории {cat_here}'

        for email in emails:
            msg = EmailMultiAlternatives(subject, text4email, None, [email])
            msg.attach_alternative(html4email, "text/html")
            msg.send()


@shared_task
def mail_notification_post_create(link, appointment_title, appointment_message, appointment_message1, appointment_subject, recipient_list, client_username):
    # получаем наш html
    html_content = render_to_string(
        'post_create_notification.html',
        {
            'link' : link,
            'post_title': appointment_title,
            'text': appointment_message,
            'text1': appointment_message1,
            'appointment_subject': appointment_subject,
        }
    )


    msg = EmailMultiAlternatives(
        # тема
        subject=appointment_subject,
        # сообщение с кратким описанием
        body=appointment_message,
        # почта, с которой будете отправлять
        from_email='Kornyushin.Vladislav@yandex.ru',
        # список получателей
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


    # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
    mail_admins(
         subject=f'Клиенту {client_username} отправлено письмо: {appointment_subject}',
        message=appointment_message,
    )