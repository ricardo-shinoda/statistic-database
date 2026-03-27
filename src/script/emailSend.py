import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

gmail_pass = config('GMAIL_PASSWORD')
g_drive_link = config('G_DRIVE_LINK')


def to_send_email(email_to, drive_link):
    # email configuration
    email_from = "ricardoshinoda@gmail.com"
    password = gmail_pass

    # Configuring smtp server (using gmail)
    smtp_host = "smtp.gmail.com"
    smtp_port = 587

    # create a message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = "Seu link para o Google Drive"

    # this is the email body
    body = f"""
    Esse é um teste para envio do email com o link de controle financeiro

    Clique <a href="{drive_link}">aqui</a> para acessar o arquivo

    Ricardo Shinoda
    """

    # attach body to the email
    msg.attach(MIMEText(body, 'html'))

    try:
        # connect server to smtp
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # start a secure connection
        server.login(email_from, password)  # login with username and password

        # send the email
        server.sendmail(email_from, email_to, msg.as_string())
        print(f'Email enviado para {email_to} com sucesso')

    except Exception as e:
        print(f'Erro ao envair o email: {e}')

    finally:
        server.quit()


to_send_email('ricardoshinoda@gmail.com', g_drive_link)
