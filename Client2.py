import socket

UDP_HOST = 'X.X.X.X'  # Adresa serverului
UDP_PORT = 12346            # Portul serverului UDP

# Creează socket pentru clientul UDP
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Trimite un mesaj inițial către server
udp_client.sendto(b'Clientul UDP s-a conectat!', (UDP_HOST, UDP_PORT))
print("Te-ai conectat ca Client 2. Incepem jocul...")

while True:
    # Așteaptă mesajul de la server
    msg, _ = udp_client.recvfrom(1024)
    decoded_msg = msg.decode().strip()

    # Verifică dacă mesajul conține informații despre sfârșitul jocului

    # Afișează mesajul de la server pentru alegere
    if "castigat" in decoded_msg.lower() or "remiza" in decoded_msg.lower():
        print(decoded_msg)
        msg, _ = udp_client.recvfrom(1024)
        decoded_msg = msg.decode().strip()

    if "Final:" in decoded_msg:
         print(decoded_msg)
         break

    print(decoded_msg)

    # Introdu alegerea și trimite-o la server
    choice = input().strip()
    udp_client.sendto(choice.encode(), (UDP_HOST, UDP_PORT))

    # Așteaptă rezultatul rundei de la server
    result_msg, _ = udp_client.recvfrom(1024)
    print(result_msg.decode().strip())

# Închide socket-ul
udp_client.close()
