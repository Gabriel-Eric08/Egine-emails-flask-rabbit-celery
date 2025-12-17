from flask import Flask, request, jsonify
from tasks import send_assync_email

app = Flask(__name__)

# Não precisamos mais configurar MAIL_SERVER, pois usaremos API
@app.route('/send', methods=['POST'])
def trigger_email():
    data = request.get_json()
    
    # Envia para o Celery
    task = send_assync_email.delay(data)

    return jsonify({
        "message": "Tarefa enviada para a fila da API!",
        "task_id": str(task.id),
        "success": True
    }), 202

if __name__ == "__main__":
    app.run(port=5050, debug=True)