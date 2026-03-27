<div align="center">
  <h1>- Conveyor Counter Pro -</h1>

  <img src="banner-repo-py-product-counter.png" alt="Project Banner" width="100%">
  <br><br>
</div>

<h2>📖 Deskripsi Proyek</h2>
<p>
  Proyek ini adalah sistem otomasi berbasis <strong>Computer Vision (Visi Komputer)</strong> yang dirancang untuk menghitung jumlah produk yang bergerak di atas <em>conveyor belt</em> secara otomatis. 
</p>
<p>
  Sistem ini menggunakan algoritma pemrosesan gambar untuk mengenali produk berdasarkan bentuk dan kombinasi warnanya secara utuh (wadah putih dan tutup oranye). Dengan melacak titik tengah presisi dari tutup produk (menggunakan <em>Image Moments</em>), program ini akan menambah hitungan secara otomatis ketika produk melewati garis batas imajiner yang telah ditentukan di layar. Proyek ini sangat cocok diimplementasikan untuk simulasi otomasi industri dan kontrol kualitas.
</p>

<hr>

<h2>✨ Fitur Utama</h2>
<ul>
  <li><strong>Deteksi Objek Kompleks:</strong> Menggabungkan masker warna <em>(Color Masking)</em> untuk mendeteksi keseluruhan badan produk (putih) beserta penutupnya (oranye) sebagai satu kesatuan <em>bounding box</em>.</li>
  <li><strong>Pelacakan Titik Tengah Presisi:</strong> Menggunakan perhitungan pusat massa (Centroid) khusus pada area tutup oranye untuk memastikan titik hitung selalu akurat di atas produk.</li>
  <li><strong>Penghitungan Garis Batas (Line Crossing):</strong> Algoritma penghitungan dinamis yang aktif saat koordinat Y produk melewati garis batas horizontal di bagian bawah <em>conveyor</em>.</li>
  <li><strong>User Interface (UI) Interaktif:</strong> Dilengkapi dengan tombol <code>EXIT</code> buatan pada layar video yang dapat diklik menggunakan <em>mouse</em>.</li>
  <li><strong>Mode Debugging:</strong> Menampilkan koordinat (X, Y) secara <em>real-time</em> di sebelah objek untuk memudahkan penyesuaian posisi dan jarak.</li>
</ul>

<hr>

<h2>🛠️ Teknologi yang Digunakan</h2>
<ul>
  <li><strong>Python 3:</strong> Bahasa pemrograman utama yang digunakan karena fleksibilitasnya.</li>
  <li><strong>OpenCV (cv2):</strong> Pustaka utama untuk pemrosesan video, deteksi warna (HSV), pembuatan <em>masking</em>, pencarian kontur, dan manipulasi gambar.</li>
  <li><strong>NumPy:</strong> Digunakan untuk operasi array matematis yang cepat, terutama saat mendefinisikan rentang warna HSV.</li>
</ul>

<hr>

<h2>🚀 Cara Menjalankan</h2>
<ol>
  <li>Pastikan Anda telah menginstal Python di sistem Anda.</li>
  <li>Instal dependensi yang dibutuhkan dengan menjalankan perintah:
    <br><code>pip install opencv-python numpy</code>
  </li>
  <li>Pastikan file video <code>0326.mp4</code> berada di dalam folder yang sama dengan <em>script</em> Python.</li>
  <li>Jalankan program melalui terminal:
    <br><code>python conveyor_counter.py</code>
  </li>
</ol>

<hr>

<h2>▶️ Preview Project</h2>
<video width="800" height="450" src="https://github.com/user-attachments/assets/7ec3485a-be51-487b-a729-1552b2dd2332"></video>
<hr>

<h2>🔜 Progress </h2>
<ol>
  <li>Installing Dependencies</li>
  <li>Baca CAM atau Video dari sumber yang tersedia</li>
  <li>Implementasi Image Processing</li>
  <li>Build Count Logic</li>
  <li>Adjust UI for user Friendly</li>
  <li>Save and store data to database (coming soon)</li>
</ol>

<hr>

<p align="center">
  <i>Dibuat untuk keperluan otomatisasi penghitungan produk pada lini produksi.</i>
</p>
