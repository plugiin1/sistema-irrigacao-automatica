import socket
import time
import random

# LIMITES
SECO = 30
IDEAL_MAX = 70

# SIMULA SENSOR
def ler_umidade():
   return random.uniform(0, 100)

# CONTROLE
def controlar(umidade):
   if umidade < SECO:
       estado = "Solo seco"
       led = "VERMELHO"
       bomba = "LIGADA"
   elif umidade <= IDEAL_MAX:
       estado = "Umidade ideal"
       led = "VERDE"
       bomba = "DESLIGADA"
   else:
       estado = "Solo muito úmido"
       led = "AZUL"
       bomba = "DESLIGADA"
   return estado, led, bomba

# HTML
def pagina_html(umidade, estado, led, bomba):
   if estado == "Solo seco":
       cor = "#e74c3c"
   elif estado == "Umidade ideal":
       cor = "#2ecc71"
   else:
       cor = "#3498db"
   html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Irrigação Automática</title>
<meta http-equiv="refresh" content="2">
<style>
           body {{
               margin: 0;
               font-family: Arial, sans-serif;
               background: linear-gradient(135deg, #1e3c72, #2a5298);
               color: white;
               text-align: center;
           }}
           .container {{
               display: flex;
               justify-content: center;
               align-items: center;
               height: 100vh;
           }}
           .card {{
               background: rgba(255,255,255,0.1);
               padding: 30px;
               border-radius: 20px;
               width: 300px;
               box-shadow: 0 10px 25px rgba(0,0,0,0.3);
           }}
           h1 {{
               margin-bottom: 10px;
           }}
           .umidade {{
               font-size: 50px;
               font-weight: bold;
           }}
           .estado {{
               font-size: 22px;
               color: {cor};
               margin-bottom: 20px;
           }}
           .barra {{
               width: 100%;
               background: #ddd;
               border-radius: 10px;
               overflow: hidden;
               margin-bottom: 20px;
           }}
           .progresso {{
               height: 20px;
               width: {umidade}%;
               background: {cor};
           }}
           .info {{
               font-size: 18px;
               margin-top: 10px;
           }}
</style>
</head>
<body>
<div class="container">
<div class="card">
<h3>Irrigação 🌱</h3>
<div class="umidade">{umidade:.1f}%</div>
<div class="estado">{estado}</div>
<div class="barra">
<div class="progresso"></div>
</div>
<div class="info">💡 LED: {led}</div>
<div class="info">🚰 Bomba: {bomba}</div>
</div>
</div>
</body>
</html>
   """
   return html

# SERVIDOR
host = "0.0.0.0"
port = 8080
server = socket.socket()
server.bind((host, port))
server.listen(1)
print(f"Servidor rodando em http://localhost:{port}")

# LOOP 
while True:
   umidade = ler_umidade()
   estado, led, bomba = controlar(umidade)
   # SERIAL (terminal)
   print(f"Umidade: {umidade:.2f}% | {estado} | LED: {led} | Bomba: {bomba}")
   conn, addr = server.accept()
   request = conn.recv(1024)
   response = pagina_html(umidade, estado, led, bomba)
   conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())
   conn.send(response.encode())
   conn.close()