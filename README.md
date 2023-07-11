# Ağ Performansı Metrikleri Aracı

Bu araç, bir istemci ile bir sunucu arasındaki bant genişliği, gecikme süresi ve paket kaybı gibi ağ performansı ölçümlerini ölçer. İki betikten oluşur: bant genişliği_client_gui.py (client) ve bant genişliği sunucusu.py (server).

###  :electric_plug: Önkoşullar

- Python 3.x
- Gerekli Python paketleri: matplotlib, tkinter

## :zap: Kullanım

# Server

1. Bir terminal veya komut istemi açın.
2. Komut dosyasını içeren dizine gidin bandwidthserver.py.
3. Sunucuyu başlatmak için aşağıdaki komutu çalıştırın:

- python bandwidthserver.py

1. İstendiğinde, sunucunun dinlemesi gereken bağlantı noktası numarasını ve kullanılacak protokolü (TCP veya UDP) girin.

# Client

1. Bir terminal veya komut istemi açın.
2. Komut dosyasını içeren dizine gidin bandwidth_client_gui.py.
3. İstemciyi başlatmak için aşağıdaki komutu çalıştırın:

python bandwidth_client_gui.py ( --ip <server_ip> --port <server_port> --protocol <protocol> --packet-size <packet_size> --duration <duration> --iterations <iterations> )


* <server_ip>
* <server_port>
* <protocol>
* <packet_size>
* <duration>
* <iterations>,  
uygun değerlerle değiştirin:


-- server_ip: Sunucunun IP adresi.
-- server_port: Sunucunun çalıştığı port numarası.
-- protocol: Kullanılacak protokol (TCP veya UDP).
-- packet_size: Bayt cinsinden her paketin boyutu (varsayılan: 1024).
-- duration: Testin saniye cinsinden süresi (varsayılan: 10.0).
-- iterations: Test yineleme sayısı (varsayılan: 1000).

* Gerçek zamanlı ölçümleri görüntüleyen Ağ Performansı Metrikleri GUI penceresi açılacaktır.

###  :package: Metrikler
Ağ Performansı Metrikleri Aracı, aşağıdaki ölçümleri ölçer:

- Süre: Test için harcanan toplam süre.
- Bant Genişliği: Saniyede kilobit (Kb/sn) cinsinden ortalama bant genişliği.
- Gecikme: Saniye cinsinden ortalama gecikme süresi (gidiş-dönüş süresi).
- Paket Kaybı: Yüzde olarak paket kaybı oranı.

## Logs

- İstemci komut dosyası günlükleri client.log.
- Sunucu komut dosyası günlükleri server.log.

## Lisans

Bu proje [MIT Lisansı](LİSANS) kapsamında lisanslanmıştır. Daha fazla ayrıntı için LİSANS dosyasına bakın .