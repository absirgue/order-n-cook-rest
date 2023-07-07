from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from dotenv import load_dotenv
import os

def send_order_email(client_email,fournisseur_order_email,order_number,fournisseur_name,client_restaurant_name,client_name,attachment,extra_email_note):
    subject = f"Commande de {client_restaurant_name} pour {fournisseur_name}"
    message = f"Bonjour, \n\n Veuillez trouver ci-joint votre commande {order_number}.\n\n" 
    if extra_email_note:
        message += extra_email_note + "\n\n"
    message += f"Bonne journée,\n\n{client_name}\n\n\nCe mail est envoyé avec le support Order n' Cook"
    attachment_name = f"[Commande]{client_restaurant_name}-{order_number}.pdf"
    recipient_list = [fournisseur_order_email, ]  
    send_email_with_attachment(message, subject, recipient_list,client_restaurant_name,attachment,client_email,attachment_name)

def send_avoir_email(client_email,fournisseur_email,order_number,client_restaurant_name,client_name,attachment):
    subject = f"Demande d'avoir pour la commande {order_number}"
    message = f"Bonjour, \n\n Veuillez trouver ci-joint une demande d'avoir pour votre commande {order_number}.\n\nBonne journée,\n\n{client_name}\n\n\nCe mail est envoyé avec le support Order n' Cook"
    attachment_name = f"[Avoir]{client_restaurant_name}-Commande {order_number}.pdf"
    send_email_with_attachment(message, subject, fournisseur_email,client_restaurant_name,attachment,client_email,attachment_name)
            

def send_email_with_attachment(message, subject, recipient_list,client_restaurant_name,attachment,client_email,attachment_name):
    with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
            email_from = f"{client_restaurant_name.replace('(','').replace(')','')}  <asirgue.dev@gmail.com>"
            headers = {'Reply-To': client_email}
            msg = EmailMessage(subject, message, email_from, recipient_list, connection=connection,headers=headers)
            attachment.seek(0)
            msg.attach(attachment_name, attachment.read(), 'application/pdf')
            msg.send()