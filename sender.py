import smtplib, ssl

def send_email(port, smtp_server, sender_email, password, receiver_email, message):
    context = ssl._create_unverified_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode("utf-8"))
