from scapy.all import IP, TCP, sr1
import logging

# Source officielle Python sur le logging : https://docs.python.org/3/library/logging.html
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

port_cible = 5550
print(f"Recherche du vrai serveur sur le port {port_cible} avec Scapy...")

for i in range(1, 255):
    ip_cible = f"192.168.1.{i}"
    
    paquet_syn = IP(dst=ip_cible)/TCP(dport=port_cible, flags="S")
    
    reponse = sr1(paquet_syn, timeout=0.2, verbose=0)
    
    if reponse and reponse.haslayer(TCP):
        if reponse.getlayer(TCP).flags == 0x12:
            print(f"Vrai serveur trouvé à l'adresse IP : {ip_cible}")
            break