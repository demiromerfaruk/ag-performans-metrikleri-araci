import sys
import time
import logging
from socket import *
import threading

BUFSIZE = 1024000

def handle_client(conn, host, remoteport, protocol):
    try:
        data_received = 0
        if protocol == "TCP":
            while True:
                data = conn.recv(BUFSIZE)
                if not data:
                    break
                data_received += len(data)
                conn.send(data)  # Alınan veriyi müşteriye geri gönder
        elif protocol == "UDP":
            while True:
                data, addr = conn.recvfrom(BUFSIZE)
                if not data:
                    break
                data_received += len(data)
                conn.sendto(data, addr)  # Alınan veriyi müşteriye geri gönder
        else:
            raise ValueError("Geçersiz protokol. Desteklenen protokoller: TCP, UDP")
        packet_loss_rate = 0 if data_received == 0 else (1 - data_received / (BUFSIZE * COUNT)) * 100
        logging.info("Paket Kaybı - Müşteri %s Port %s: %.2f%%", host, remoteport, packet_loss_rate)
    except Exception as e:
        logging.error("Bir hata oluştu - Müşteri %s Port %s: %s", host, remoteport, str(e))
    finally:
        conn.close()
        logging.info("Müşteri %s Port %s işlemi tamamlandı", host, remoteport)

def server(port, protocol):
    s = socket(AF_INET, SOCK_STREAM) if protocol == "TCP" else socket(AF_INET, SOCK_DGRAM)
    s.bind(('', int(port)))
    s.listen(1)
    logging.info("Sunucu hazır...")
    try:
        while True:
            conn, (host, remoteport) = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, host, remoteport, protocol))
            client_thread.start()
    except Exception as e:
        logging.error("Bir hata oluştu: %s", str(e))
    finally:
        s.close()

def main():
    port = input("Port: ")
    protocol = input("Protokol (TCP veya UDP): ").upper()
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    server(port, protocol)

if __name__ == "__main__":
    main()
