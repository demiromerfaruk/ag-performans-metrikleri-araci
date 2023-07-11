import sys
import time
import logging
from socket import *
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
import argparse

BUFSIZE = 1024000
metrics = {
    'time': [],
    'bandwidth': [],
    'latency': [],
    'packet_loss': []
}

class BandwidthGUI:
    def __init__(self, ip, port, protocol, packet_size, duration, iterations):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.packet_size = packet_size
        self.duration = duration
        self.iterations = iterations

        self.root = tk.Tk()
        self.root.title("Ağ Performansı Metrikleri")
        self.root.geometry("600x400")

        # ... GUI başlatma kodunun geri kalanı ...

    def start_test(self):
        threading.Thread(target=self.client).start()

    def client(self):
        testdata = 'x' * (self.packet_size - 1) + '\n'
        try:
            start_time = time.time()
            if self.protocol == "TCP":
                s = socket(AF_INET, SOCK_STREAM)
            elif self.protocol == "UDP":
                s = socket(AF_INET, SOCK_DGRAM)
            else:
                raise ValueError("Geçersiz protokol. Desteklenen protokoller: TCP, UDP")
            s.connect((self.ip, int(self.port)))
            connection_setup_time = time.time()
            data_sent = self.packet_size * self.iterations
            packets_sent = 0
            packets_received = 0
            test_duration = 0
            while test_duration < self.duration:
                packets_sent += 1
                if self.protocol == "TCP":
                    s.send(bytearray(testdata, "utf-8"))
                    data = s.recv(self.packet_size)
                elif self.protocol == "UDP":
                    s.sendto(bytearray(testdata, "utf-8"), (self.ip, int(self.port)))
                    data, _ = s.recvfrom(self.packet_size)
                if data:
                    packets_received += 1
                update_metrics(time.time() - start_time, (data_sent * 0.001) / (time.time() - connection_setup_time), (connection_setup_time - start_time) + (time.time() - connection_setup_time) / 2, (packets_sent - packets_received) / packets_sent * 100)
                test_duration = time.time() - start_time
            s.shutdown(1)
            end_time = time.time()
            data = s.recv(self.packet_size)
            self.close()
            logging.info("Alınan veri: %s", data.decode())
            logging.info("Ping: %s", (connection_setup_time - start_time) + (end_time - connection_setup_time) / 2)
            logging.info("Zaman: %s", end_time - connection_setup_time)
            logging.info("Bant genişliği: %s Kb/sn.", round((data_sent * 0.001) / (end_time - connection_setup_time), 3))
            packet_loss_rate = 0 if packets_sent == 0 else (packets_sent - packets_received) / packets_sent * 100
            logging.info("Paket Kaybı: %.2f%%", packet_loss_rate)
        except ConnectionRefusedError:
            logging.error("Bağlantı reddedildi. Sunucunun çalıştığından ve IP adresi ile portun doğru olduğundan emin olun.")
            messagebox.showerror("Hata", "Bağlantı reddedildi. Lütfen sunucu erişilebilirliğini ve bağlantı ayarlarını kontrol edin.")
        except TimeoutError:
            logging.error("Bağlantı zaman aşımına uğradı. Ağ bağlantınızı kontrol edin ve tekrar deneyin.")
            messagebox.showerror("Hata", "Bağlantı zaman aşımına uğradı. Lütfen ağ bağlantınızı kontrol edin.")
        except Exception as e:
            logging.error("Bir hata oluştu: %s", str(e))
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        finally:
            s.close()

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Ağ Performansı Metrikleri Aracı")
    parser.add_argument("--ip", required=True, help="Sunucunun IP adresi")
    parser.add_argument("--port", required=True, help="Sunucunun port numarası")
    parser.add_argument("--protocol", choices=["TCP", "UDP"], required=True, help="Kullanılacak protokol (TCP veya UDP)")
    parser.add_argument("--packet-size", type=int, default=1024, help="Paket boyutu (byte cinsinden)")
    parser.add_argument("--duration", type=float, default=10.0, help="Test süresi (saniye cinsinden)")
    parser.add_argument("--iterations", type=int, default=1000, help="Test tekrar sayısı")
    args = parser.parse_args()

    logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    gui = BandwidthGUI(args.ip, args.port, args.protocol, args.packet_size, args.duration, args.iterations)
    ani = FuncAnimation(plt.gcf(), animate_graphs, interval=1000)
    plt.tight_layout()
    plt.show()
    gui.run()

if __name__ == "__main__":
    main()
