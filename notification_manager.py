import os
import smtplib
import ssl
from email.message import EmailMessage
import re

class NotificationManager:
    PADRAO = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
    def __init__(self, price, origin_airport,
                     destination_airport, outbound_date,
                     inbound_date,number_of_stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.number_of_stops = number_of_stops
    def check_email(self,email):
        striped_email = email.strip().lower()
        return bool(self.PADRAO.match(striped_email))

    def send_email(self, user_email):
        # Coleta credenciais das variáveis de ambiente de forma segura
        my_email = os.environ.get("MY_EMAIL")
        password = os.environ.get("MY_APP_PASSWORD")
        # Monta o e-mail de forma protegida contra Injeção de Cabeçalho (CRLF)
        msg = EmailMessage()
        msg.set_content(f"Alerta de preço baixo! Apenas R$ {self.price} para voar "
                         f"de {self.origin_airport} para {self.destination_airport},"
                            f" com {self.number_of_stops} parada(s)"
                         f"em {self.outbound_date} até {self.inbound_date}.")
        msg["Subject"] = "Low Price Alert!"
        msg["From"] = my_email
        if self.check_email(user_email):
            msg["To"] = user_email
        else:
            raise ValueError(f'E-mail inválido: {user_email!r}')

        if not all([my_email, password, user_email]):
            raise Exception("Email not sent!, Some Values Were Wrong!")
        # Cria um contexto SSL seguro forçando validação moderna (RFC 8997)
        context = ssl.create_default_context()
        # Especifica explicitamente a porta 587 (STARTTLS)
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.ehlo()
            connection.starttls(context=context)
            connection.ehlo()

            connection.login(str(my_email), str(password))
            connection.send_message(msg)

        print(f"Email successfully sent to {user_email}!")