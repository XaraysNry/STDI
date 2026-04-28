## <center> <b> Modul 5 Fault Tolerance </b> </center>
<center> Nama: Aditya Wisnu Naraya
<br>Nim: 235410069
<br>Kelas: Informatika-2
</center>


4.1 Load Balancing Aplikasi  
---------------
Materi ini merupakan materi Praktikum SIstem Terdistribusi dan Terdesentralisasi
untuk pembahasan tentang Fault Tolerance. Pembahasan tentang load balancing diperlukan
agar high-availability dari suatu aplikasi bisa tercapai dengan melakukan proses scaling
aplikasi menjadi lebih dari satu dan mengkonfigurasi proxy load balancer.

1. Persiapan  
    Pada materi ini, aplikasi merupakan aplikasi ASGI Python yang dibuat dengan
    menggunakan framework Blacksheep (https://www.neoteroi.dev/blacksheep/). Aplikasi
    dibuat hanya merupakan aplikasi default - tutorial dan hanya digunakan untuk keperluan
    pemahaman load balancing sehingga pembaca perlu melihat pada dokumentasi dari
    Blacksheep jika ingin mendalami pengembangan aplikasi menggunakan framework
    tersebut.
    Software yang diperlukan untuk mengikuti permbahasan ini adalah Docker (jika
    menggunakan Windows, install Docker Desktop
    (https://docs.docker.com/desktop/setup/install/windows-install/). Jika menggunakan Linux,
    install Docker dan Docker Compose menggunakan package manager masing-masing distro.
    Sebagai contoh, berikut ini instalasi pada distro Artix Linux:
    ![z1](images/a2.png)  
    Perhatikan, karena aplikasi akan dibuat menggunakan Python, sebaiknya menggunakan env
    manager seperti Micromamba
    (https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), uv
    (https://docs.astral.sh/uv/), atau Miniconda
    (https://www.anaconda.com/docs/getting-started/miniconda/install). Silakan dipelajari terlebih
    dahulu dan buat env khusus untuk pembahasan ini. Khusus jika menggunakan uv, gunakan
    panduan berikut: https://github.com/NEO-X-School/notes/blob/main/uv/00.md
    ![z2](images/a3.png)
    ![z3](images/a3in1.png)  
    <br>Untuk membuat aplikasi web menggunakan Blacksheep, install blacksheep dan
    blacksheep-cli terlebih dahulu:
    ![z4](images/a4.png) 
    sebelumnya sudah di install jadi tampilannya berbeda  

02. Pembuatan Aplikasi Web  
    Setelah itu, buat aplikasi menggunakan cli
    <pre> blacksheep create </pre>
    hasil nya ketika di cek  
    ![z5](images/a5.png)  
    <br>install paket yang diperlukan:  
    ![z6](images/a6.png)  
    ketika sudah di intall akan seperti itu tampilannya  
    <br> Pada shell tempat kita mengaktifkan server, muncul:
    ![a3](images/10.png)  
    <br> Pada titik ini, kita sudah berhasil membuat aplikasi menggunakan Blacksheep. Perhatikan,
    dalam direktori blacksheep_lb sudah ada Dockerfile yang bisa kita gunakan.
    ![a4](images/11.png)  
    Dockerfile ini bisa digunakan dan secara default akan membuka port 80, bukan 44777.
    Ini penting untuk diperhatikan karena akses ke port akan diperlukan saat menggunakan
    Docker Compose.



03. Siapkan Dockerfile dan docker-compose.yml
Ada 2 komponen utama pada materi ini:
    1. Aplikasi yang dibangun menggunakan Blacksheep. Aplikasi ini akan di-scale menjadi
    2 instances.
    2. Proxy untuk load balancing menggunakan nginx.
    Dengan demikian, diperlukan pengaturan sebagai berikut:
    1. Aplikasi diletakkan pada direktori tertentu (blacksheep_lb)
    2. Direktori nginx untuk mengelola load balancer menggunakan nginx
    3. File docker-compose.yml untuk mengelola Docker Compose.
    4. Opsional: env.sh untuk alias - mempermudah pengetikan perintah melalui cli (hanya
    untuk Linux - Bash).
    Aplikasi sudah harus mempunyai Dockerfile, demikian juga nginx.  
    ![p1](images/1.png)  
    <br>blacksheep_lb/Dockerfile
    ![p2](images/2.png)  
    Dockerfile di blacksheep_lb ini merupakan bawaan dari Blacksheep. Sila mengedit tetapi
    pastikan bahwa anda memahami cara kerja Docker dan sistem operasi yang akan menjadi
    dasar dari container tersebut. Untuk Dockerfile di atas, perubahan hanya dilakukan untuk
    versi Python yang digunakan yaitu versi 3.13.1-slim.  
    <br>nginx/Dockerfile
    ![p3](images/3.png)  
    <br>nginx/nginx.conf  
    Kita juga perlu menyiapkan konfigurasi nginx sebagai load balancer.
    ![p4](images/4.png)  
    <br>docker-compose.yml
    ![p5](images/5.png)  
    <br>env.sh  
    ![p6](images/6.png)  
    <br>Sebelum menjalankan Docker, jalankan dulu service dockerd. Pada sistem yang menggunakan dinit:  
    ![p7](images/7.png)   
    Jika menggunakan Linux lainnya, khususnya Linux dengan Systemd, gunakan  
    *sudo systemctl start dockerd*  
<br>  

4. Jalankan Docker Compose  

    ![a1](images/8in1.png)  
    ![a1in](images/8in2.png)  
    <br>Untuk memeriksa, kita bisa melihat hasil di browser:
    ![a2](images/9.png)  
    <br>Perhatikan: port yang digunakan sekarang port 8081 (jika tidak menyebutkan port seperti
    tamilan di atas - hanya localhost, maka defaultnya 8081), bukan 44777 lagi.  
    <br>Hasil dari docker ps menunjukkan nama aplikasi yang sedang berjalan. Pada bagian ini
    kita bisa melihat ada 2 instances dari aplikasi bs_app yaitu: load-balancing-bs_app-1
    dan load-balancing-bs_app-2 (nama di depan - load-balancing… merupakan hasil
    dari nama direktori).  
    ![a3](images/12.png)  
    <br>Bagaimana mengetahui bahwa load balancing sudah berjalan? Akses ke aplikasi akan
    di-route melalui load balancer (nginx) ke salah satu instance. Lihat potongan log berikut:  
    ![a4](images/13.png)  
    Perhatikan: log untuk load-balancing-bs_app-1 mendapatkan 2 akses di bagian
    paling bawah, sementara load-balancing-bs_app-2 tmendapatkan 1 akses di bagian
    paling bawah. Ini berarti pada saat terdapat request, nginx me-route permintaaan / request
    tersebut ke load-balancing-bs_app-1.  
    <br>Jika sudah selesai, matikan semua container:  
    ![a5](images/14.png) 

4. Failure Detection   
    <br>Failure Detection adalah proses untuk menentukan apakah suatu komponen telah gagal.  
    Heartbeat  
    <br> Protokol heartbeat adalah protokol untuk memantau aktivitas suatu komponen. Jika
    suatu komponen pemantauan tidak menerima heartbeat dari komponen lain dalam jangka
    waktu tertentu, komponen tersebut diasumsikan telah gagal dan tidak responsif.  
    <br> heartbeat/check-server.py  
    <br> Cobalah script pada kondisi tidak ada aplikasi blacksheep di port 44777 yang aktif. Setelah
    itu, aktifkan port 44777 untuk aplikasi blacksheep. Jalankan script pada 2 kondisi tersebut
    dan catat serta jelaskan perbedaannya.
    ![a6](images/15.png)  
    ![a7](images/c1.png)  
    <br> failure-detection/
    Library tenacity (https://github.com/jd/tenacity) bisa digunakan untuk mengelola
    proses yang memerlukan keterkaitan dengan komponen di luar aplikasi. Hal ini diperlukan.
    karena selalu ada kemungkinan kegagalan untuk koneksi dengan komponen di luar aplikasi.
    Gunakan file check-retry.py pada 2 kondisi: aplikasi blacksheep aktif dan non-aktif kemudian
    jelaskan.
    ![a8](images/c2.png)  
    <br>Pola circuit breaker merupakan pola desain yang digunakan dalam microservices
    untuk mencegah kegagalan berantai dengan memblokir sementara panggilan ke layanan
    yang gagal. Pola ini bertindak seperti state machine dengan tiga status: "closed", "open",
    dan "half-open".
    Dalam status closed, permintaan diijinkan dan dipantau untuk kegagalan. Jika
    ambang batas kegagalan terpenuhi, circuit breaker beralih ke status open, segera menolak
    permintaan selanjutnya dan memberi layanan waktu untuk pulih. Setelah batas waktu, circuit
    breaker memasuki status half-open, memungkinkan sejumlah permintaan terbatas untuk
    menguji apakah layanan telah pulih. Jika permintaan pengujian berhasil, sirkuit kembali ke
    status "closed"; jika gagal, pemutus sirkuit kembali ke status "topen"  
    <br>Coba script check-circuit-breaker.py pada 2 kondisi: aplikasi blacksheep aktif dan non-aktif
    setelah itu jelaskan cara kerja dari check-circuit-breaker.py.
    ![a9](images/c3.png) 
