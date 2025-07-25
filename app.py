from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "status": "healthy",
        "service": "Telegram News Bot",
        "version": "1.0.0"
    }

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 