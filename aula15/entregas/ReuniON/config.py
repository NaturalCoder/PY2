import os

# Configurações básicas
SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-ultra-segura'
SQLALCHEMY_DATABASE_URI = 'sqlite:///reunion.db'

# Configurações de e-mail (exemplo para Mailtrap)
MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'seu-usuario'
MAIL_PASSWORD = 'sua-senha'
MAIL_USE_TLS = True