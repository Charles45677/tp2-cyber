import socket

# Scanner le sous-réseau local sur le port 5550 découvert
port_cible = 5550
print(f"[*] Recherche du vrai serveur sur le port {port_cible}...")

for i in range(1, 255):
    ip = f"192.168.1.{i}"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        result = s.connect_ex((ip, port_cible))
        if result == 0:
            print(f"[+] Vrai serveur trouvé à l'adresse IP : {ip}")
            break
    except Exception:
        pass
    finally:
        s.close()