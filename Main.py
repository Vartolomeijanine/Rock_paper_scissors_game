
import socket

TCP_HOST = '0.0.0.0'
TCP_PORT = 12345
UDP_PORT = 12346
ROUNDS = 3
MATCHES = 3

# Creeaza socket pentru serverul TCP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((TCP_HOST, TCP_PORT))
tcp_server.listen(1)

# Creeaza socket pentru serverul UDP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((TCP_HOST, UDP_PORT))

print("Serverul este pornit si asteapta conexiunile clientilor...")

# Accepta conexiunea clientului TCP
tcp_client, addr_tcp = tcp_server.accept()
print("Clientul TCP s-a conectat.")
tcp_client.send("Asteptam conectarea clientului UDP...\n".encode())

# Asteapta conectarea clientului UDP
udp_choice, addr_udp = udp_server.recvfrom(1024)
print("Clientul UDP s-a conectat de la", addr_udp)

# Anunta clientul TCP ca UDP s-a conectat
tcp_client.send("Clientul UDP s-a conectat! Incepem jocul...\n".encode())

# Setup initial scor
tcp_wins, udp_wins = 0, 0

# Start joc cu MATCHES
for match in range(MATCHES):
    tcp_round_wins, udp_round_wins = 0, 0

    for round in range(ROUNDS):
        # Asteapta alegerea clientului TCP
        tcp_client.send("Introdu alegerea ta (Piatra, Hartie, Foarfeca):\n".encode())
        tcp_choice = tcp_client.recv(1024).decode().strip()

        # Anunta clientul UDP sa isi faca alegerea
        udp_server.sendto("Introdu alegerea ta (Piatra, Hartie, Foarfeca):\n".encode(), addr_udp)
        udp_choice, _ = udp_server.recvfrom(1024)
        udp_choice = udp_choice.decode().strip()

# Determina castigatorul rundei
        if tcp_choice.lower() == udp_choice.lower():
            result = "Remiza"
        elif (tcp_choice.lower() == "piatra" and udp_choice.lower() == "foarfeca") or \
                (tcp_choice.lower() == "foarfeca" and udp_choice.lower() == "hartie") or \
                (tcp_choice.lower() == "hartie" and udp_choice.lower() == "piatra"):
            result = "Clientul 1 (TCP) a castigat runda!"
            tcp_round_wins += 1
        else:
            result = "Clientul 2 (UDP) a castigat runda!"
            udp_round_wins += 1

        # Anunta fiecare client despre rezultatul rundei
        tcp_client.send(f"Runda {round + 1}: {result}\n".encode())
        udp_server.sendto(f"Runda {round + 1}: {result}\n".encode(), addr_udp)

        # Verifica daca cineva a castigat meciul dupa doua runde
        if tcp_round_wins == 2 or udp_round_wins == 2:
            break

    # Stabileste castigatorul meciului
    if tcp_round_wins > udp_round_wins:
        match_result = "Clientul 1 (TCP) a castigat meciul!"
        tcp_wins += 1
    elif udp_round_wins > tcp_round_wins:
        match_result = "Clientul 2 (UDP) a castigat meciul!"
        udp_wins += 1
    else:
        match_result = "Meciul s-a terminat cu remiza!"

    # Trimite rezultatul meciului catre fiecare client
    tcp_client.send(f"{match_result}\n".encode())
    udp_server.sendto(f"{match_result}\n".encode(), addr_udp)

    # Verifica daca cineva a castigat jocul
    if tcp_wins == 2 or udp_wins == 2:
        break

# Anunta castigatorul final
if tcp_wins > udp_wins:
    final_result = "Final: Clientul 1 (TCP) a castigat jocul final!"
elif udp_wins > tcp_wins:
    final_result = "Final: Clientul 2 (UDP) a castigat jocul final!"
else:
    final_result = "Final: Jocul s-a terminat cu remiza!"

udp_server.sendto(f"{final_result}\n".encode(), addr_udp)
tcp_client.send(f"{final_result}\n".encode())


# Inchide socket-urile
tcp_client.close()
udp_server.close()
tcp_server.close()