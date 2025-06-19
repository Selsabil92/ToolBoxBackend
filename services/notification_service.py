# Gestion des notifications (email, Slack, Discord, etc.)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fonction pour envoyer un email de notification
def send_notification(email, subject, message):
    """
    Envoie une notification par email à l'utilisateur.
    :param email: L'email de l'utilisateur à notifier.
    :param subject: Le sujet du message.
    :param message: Le contenu du message.
    """
    try:
        # Paramètres de connexion
        sender_email = "your_email@example.com"
        sender_password = "your_password"
        smtp_server = "smtp.example.com"
        smtp_port = 587

        # Création du message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject

        # Attacher le corps du message
        msg.attach(MIMEText(message, "plain"))

        # Connexion et envoi de l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        
        return {"status": "success", "message": "Notification sent successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
