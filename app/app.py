from flask import Flask

app = Flask(__name__)

# Middleware para headers de seguridad
@app.after_request
def add_security_headers(response):
    # Headers para resolver las vulnerabilidades detectadas
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Permissions-Policy'] = "geolocation=(self)"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Server'] = 'SecureServer'  # Ocultar versión del servidor
    return response

@app.route('/')
def home():
    return "DevSecOps Project: ¡Escaneado con OWASP ZAP!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
