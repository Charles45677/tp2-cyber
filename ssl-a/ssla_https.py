from flask import Flask, request

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print(f"\n[+] Connexion HTTPS interceptée avec succès !")
    print(f"[+] Données reçues (Le Flag se cache ici) :")
    print(request.data.decode('utf-8', errors='ignore'))
    return "OK", 200

if __name__ == "__main__":
    # Le client se connecte sur le port 5550 en HTTPS
    app.run(host="0.0.0.0", port=5550, ssl_context=("fullchain.pem", "privkey.pem"))