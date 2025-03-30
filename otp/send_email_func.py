import smtplib
from email.mime.text import MIMEText

from otp.settings_otp import config


def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["From"] = config["EMAIL_USER"]
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP(config["EMAIL_HOST"], config["EMAIL_PORT"])
        server.starttls()  # Segurança extra
        server.login(config["EMAIL_USER"], config["EMAIL_PASS"])
        server.sendmail(config["EMAIL_USER"], to_email, msg.as_string())
        server.quit()
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
