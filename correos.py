from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv

load_dotenv()

def olvide_password(destinatario):
    fernet = Fernet(environ.get('FERNET_KEY'))
    token = fernet.encrypt(bytes(destinatario,'utf-8'))

    email = environ.get('EMAIL_EMISOR')
    password = environ.get('PASSWORD_EMAIL_EMISOR')
    mensaje = MIMEMultipart()
    # titulo del correo
    mensaje['Subject'] = 'Olvidaste tu contraseña'

    mensaje['From'] = email
    mensaje['To'] = destinatario
    cuerpo = "Hola, parece que has olvidado tu correo. Has click en el siguiente link: http://localhost:5000/resetear-password?token={}".format(token.decode('utf-8'))
    text = MIMEText(cuerpo, 'plain')

    mensaje.attach(text)

    #                   SERVIDOR      | PUERTO
    # outlook > outlook.office365.com | 587
    # hotmail > smtp.live.com         | 587
    # gmail >   smtp.gmail.com        | 587
    # icloud >  smtp.mail.me.com      | 587
    # yahoo >   smtp.mail.yahoo.com   | 587
    emisor = SMTP('smtp.gmail.com', 587)

    emisor.starttls()

    emisor.login(email, password)

    emisor.sendmail(from_addr=email, to_addrs=destinatario, msg= mensaje.as_string())

    emisor.quit()
    print("se envio el correo exitosamente")

# olvide_password("tecsup_centro_doc02@tecsup.edu.pe")