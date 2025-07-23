from flask import Flask, jsonify
import os
import socket
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración de seguridad mejorada
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600
)

@app.after_request
def add_security_headers(response):
    security_headers = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "default-src 'self'; script-src 'self'",
        'Permissions-Policy': "geolocation=(), microphone=(), camera=()",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Resource-Policy': 'same-origin',
        'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
    }
    for header, value in security_headers.items():
        response.headers[header] = value
    
    # Ocultar headers sensibles
    for header in ['Server', 'X-Powered-By']:
        if header in response.headers:
            del response.headers[header]
    
    return response

@app.route('/')
def home():
    logger.info("Acceso a la ruta principal")
    return "DevSecOps Project: ¡Escaneado con OWASP ZAP!"

@app.route('/health')
def health_check():
    logger.info("Health check solicitado")
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "environment": os.environ.get("ENV", "development")
    }), 200

if __name__ == "__main__":
    # Configuración optimizada para escaneos
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Iniciando aplicación en puerto {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False  # Importante para evitar dobles instancias
    )