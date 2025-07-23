from flask import Flask, jsonify
import os
import socket

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
    
    # Ocultar el header Server manualmente
    if 'Server' in response.headers:
        del response.headers['Server']
    
    return response

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

@app.route('/')
def home():
    return "DevSecOps Project: ¡Escaneado con OWASP ZAP!"

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname()
    }), 200

if __name__ == "__main__":
    # Configuración de puerto desde variable de entorno
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True  # Habilitar modo multi-hilo
    )
