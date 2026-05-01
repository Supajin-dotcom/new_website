import http.server
import socketserver
import ssl
import webbrowser
import os

PORT = 8000
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Page par défaut
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    # Désactiver les logs pour garder la console propre
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    # Servir les fichiers depuis le dossier du script
    os.chdir(CURRENT_DIR)

    # Configuration du serveur HTTP de base
    httpd = socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler)

    # --- NOUVELLE MÉTHODE HTTPS (Compatible Python 3.12+) ---
    # On crée un contexte SSL pour configurer la sécurité
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    try:
        # On charge le certificat et la clé privée
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        
        # On applique le contexte au socket du serveur
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        print("Serveur HTTPS lancé avec succès :")
        print(f"→ https://localhost:{PORT}")
        print(f"→ https://127.0.0.1:{PORT}")

        # Ouvrir le navigateur automatiquement
        webbrowser.open(f"https://localhost:{PORT}")

        # Lancer le serveur
        httpd.serve_forever()

    except FileNotFoundError:
        print("Erreur : Les fichiers 'cert.pem' ou 'key.pem' sont introuvables.")
        print("Assurez-vous de les avoir générés dans le même dossier que ce script.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
