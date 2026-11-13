import os
import smtplib
import ssl
from email.message import EmailMessage
class NotificationManager:
    def __init__(self,price,departure_airport_iata_code,
                 arrival_airport_iata_code,outbound_date,inbound_date):
        self.price = price
        self.departure_airport = departure_airport_iata_code
        self.arrival_airport = arrival_airport_iata_code
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
    def send_message(self):
        # Coleta credenciais das variáveis de ambiente de forma segura
        my_email = os.environ.get("MY_EMAIL")
        password = os.environ.get("MY_APP_PASSWORD")
        to_email = os.environ.get("TO_EMAIL")
        # Monta o e-mail de forma protegida contra Injeção de Cabeçalho (CRLF)
        msg = EmailMessage()
        msg.set_content(f"Only {self.price}R$ to Fly From {self.departure_airport} "
                        f"to {self.arrival_airport}, on {self.outbound_date}. ")
        msg["Subject"] = "Low Price Alert!"
        msg["From"] = my_email
        msg["To"] = to_email
        # Cria um contexto SSL seguro forçando validação moderna (RFC 8997)
        context = ssl.create_default_context()
        # Especifica explicitamente a porta 587 (STARTTLS)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls(context=context)  # Aplica o contexto seguro
            connection.login(user=my_email, password=password)
            connection.send_message(msg)
