from django.shortcuts import render
from django.core.mail import EmailMessage,send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
def index(request):
    return render(request,'myapp/index.html')

def homepage(request):
    subject='this is test mail'
    name='User'
    html_message=render_to_string('myapp/email.html',{'name':name})
    plain_message=strip_tags(html_message)
    from_email='ajdjango3@gmail.com'
    to_email=['ishmeetsinghsodhi14@gmail.com']
    file_path=f'{settings.BASE_DIR}/requirements.txt'
    email=EmailMultiAlternatives(subject=subject,body=plain_message,from_email=from_email,to=to_email,)
    email.attach_file(file_path)
    # email=EmailMessage(subject=subject,body=html_message,from_email=from_email,to=to_email)
    email.content_subtype='html'
    email.send()
    return HttpResponse('test mail sent successfully')