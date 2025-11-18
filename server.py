#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8080

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Permitir CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

Handler = MyHTTPRequestHandler

print(f"🚀 Servidor iniciado en http://localhost:{PORT}")
print(f"📁 Sirviendo archivos desde: {os.getcwd()}")
print(f"🌐 Abre http://localhost:{PORT} en tu navegador")
print(f"⏹️  Presiona Ctrl+C para detener el servidor\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
