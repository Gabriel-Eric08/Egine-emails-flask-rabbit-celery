import eventlet
eventlet.monkey_patch() # Crucial para não travar no Windows

import requests
from celery import Celery

# Configura o Celery para usar o seu Redis local
celery = Celery('tasks', broker='redis://localhost:6379/0')

# Seus dados extraídos da URL e mensagens anteriores
API_TOKEN = "dd47f6c153a61931172b6944b2827bb2"
INBOX_ID = "4263096"

@celery.task
def send_assync_email(email_data):
    # Endpoint correto para a sua Sandbox específica
    url = f"https://sandbox.api.mailtrap.io/api/send/{INBOX_ID}"
    
    # O Mailtrap Sandbox aceita o Token no cabeçalho 'Api-Token'
    headers = {
        "Api-Token": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": {"email": "sistema@exemplo.com", "name": "Meu App Flask"},
        "to": [{"email": email_data['to']}],
        "subject": email_data['subject'],
        "text": email_data['body']
    }

    print(f"Tentando enviar para Inbox {INBOX_ID}...")
    
    try:
        # Usamos HTTPS (Porta 443) para passar pelo firewall do seu trabalho
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ SUCESSO: O e-mail apareceu no seu Mailtrap!")
        else:
            print(f"❌ FALHA: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️ ERRO DE CONEXÃO: {e}")