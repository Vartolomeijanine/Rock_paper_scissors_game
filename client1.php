<?php
$host = 'X.X.X.X'; // Adauga adresa IP
$port = 12345;

// Creaza un socket TCP
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if (!$socket) {
    die("Eroare la crearea socket-ului: " . socket_strerror(socket_last_error()) . "\n");
}

// Conecteaza la server
if (!socket_connect($socket, $host, $port)) {
    die("Eroare la conectare: " . socket_strerror(socket_last_error()) . "\n");
}

echo "Te-ai conectat ca Client 1. Asteptam conectarea clientului UDP...\n";

// Citeste mesajul de la server
while ($msg = socket_read($socket, 2048, PHP_NORMAL_READ)) {
    echo $msg;

    // Daca se cere alegerea
    if (strpos($msg, 'Introdu alegerea ta') !== false) {
        $choice = readline();
        socket_write($socket, $choice, strlen($choice));
    }

    // Verifică dacă jocul s-a încheiat
    if (strpos($msg, 'Final:') !== false) {
        break;
    }
}

// Inchide socket-ul
socket_close($socket);
?>
