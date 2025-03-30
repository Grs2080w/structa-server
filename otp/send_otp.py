from otp.send_email_func import send_email
from otp.settings_otp import config


def send_code_otp(email, code):
    subject = "Verification Code"
    message = f"""
Hello, 👋

You're receiving this email because you requested a verification code to access your {config["APP_NAME"]} account. 🔐 To complete the verification, use the code below:

Verification Code: {code}

For security reasons: ⚠️

- Don't share this code with anyone.
- This code expires in 5 minutes. After this period, you'll need to request a new code. 🔄
- If you didn't make this request, ignore this email. 🙈

Best regards,

The {config["APP_NAME"]} Team 🌟"""
    send_email(email, subject, message)


# send_code_otp("c5V0o@example.com", "123456")
