import cv2
import numpy as np

# --- VARIABEL GLOBAL UNTUK UI ---
exit_program = False

# Fungsi untuk mendeteksi klik mouse pada layar video
def deteksi_klik_mouse(event, x, y, flags, param):
    global exit_program
    # Jika klik kiri mouse ditekan
    if event == cv2.EVENT_LBUTTONDOWN:
        # Cek apakah klik berada di dalam area tombol EXIT (X: 700-790, Y: 10-50)
        if 700 <= x <= 790 and 10 <= y <= 50:
            print("Tombol Exit diklik. Menutup program...")
            exit_program = True

# 1. Buka file video
video_path = '0326.mp4'
cap = cv2.VideoCapture(video_path)

# 2. Buat Jendela dan pasang pendeteksi klik mouse
cv2.namedWindow("CAM Conveyor")
cv2.setMouseCallback("CAM Conveyor", deteksi_klik_mouse)

# Pengaturan Penghitung
batas_garis_start = (210, 353)
batas_garis_end = (698, 316)      # Posisi garis horizontal di bawah (koordinat Y)
offset = 15              # Toleransi area di sekitar garis
jumlah_produk = 0
objek_terhitung = []     # Menyimpan tuple (y, frame_idx) untuk menghindari hitungan ganda dalam jangka pendek
frame_idx = 0

# Performance tuning: process at a lower resolution every N frames,
# then reuse last detections for intermediate frames to keep display smooth.
proc_scale = 0.5
process_every_n_frames = 2
last_detections = []  # list of dicts: {'box':(x,y,w,h), 'center':(cx,cy)}

# Precompute constants and reusable buffers to avoid reallocating every loop
scale_up = 1.0 / proc_scale
kernel = np.ones((3, 3), np.uint8)
# color thresholds (HSV)
lower_orange = np.array([5, 100, 100])
upper_orange = np.array([20, 255, 255])
lower_white = np.array([0, 0, 255])
upper_white = np.array([200, 60, 255])

# Read first frame before loop so we can allocate fixed-size data once
ret, frame = cap.read()
frame_idx = 0
if not ret:
    print("Tidak dapat membaca video atau video kosong")
    cap.release()
    cv2.destroyAllWindows()
    raise SystemExit

frame = cv2.resize(frame, (800, 450))
frame_idx += 1

fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Get frame width and height from the input capture object
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60.0 # Define the desired frames per second

# 3. Initialize the VideoWriter object
out = cv2.VideoWriter('0326_out.mp4', fourcc, fps, (800, 450))

while ret and not exit_program:
    # Draw counting line first (for consistent overlay)
    cv2.line(frame, batas_garis_end, batas_garis_start, (255, 0, 0), 2)

    # Only run the heavier detection pipeline every few frames at lower resolution
    if frame_idx % process_every_n_frames == 0:
        # prepare smaller frame for faster processing
        small = cv2.resize(frame, (0, 0), fx=proc_scale, fy=proc_scale)
        hsv_small = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

        # 3. Filter Warna Oranye (Tutup) on small frame
        mask_orange_small = cv2.inRange(hsv_small, lower_orange, upper_orange)

        # 4. Filter Warna Putih (Wadah) on small frame
        mask_white_small = cv2.inRange(hsv_small, lower_white, upper_white)

        # combine and clean
        mask_combined_small = cv2.bitwise_or(mask_orange_small, mask_white_small)
        mask_combined_small = cv2.morphologyEx(mask_combined_small, cv2.MORPH_CLOSE, kernel)
        mask_combined_small = cv2.morphologyEx(mask_combined_small, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask_combined_small, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # rebuild detections for this processing step
        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 100:  # area threshold for small frame
                continue
            x_s, y_s, w_s, h_s = cv2.boundingRect(contour)

            # compute center using orange mask moments inside small ROI
            roi_orange_small = mask_orange_small[y_s:y_s+h_s, x_s:x_s+w_s]
            M = cv2.moments(roi_orange_small)
            if M['m00'] == 0:
                continue
            cx_local = int(M['m10'] / M['m00'])
            cy_local = int(M['m01'] / M['m00'])

            # scale to display frame coordinates
            x = int(x_s * scale_up)
            y = int(y_s * scale_up)
            w = int(w_s * scale_up)
            h = int(h_s * scale_up)
            cx = int((x_s + cx_local) * scale_up)
            cy = int((y_s + cy_local) * scale_up)

            detections.append({'box': (x, y, w, h), 'center': (cx, cy)})

            # counting logic runs only on processed frames
            objek_terhitung = [(y_val, f_idx) for (y_val, f_idx) in objek_terhitung if frame_idx - f_idx < 50]
            if (350 - offset) < cy < (350 + offset):
                is_new = True
                for (y_val, f_idx) in objek_terhitung:
                    if abs(cy - y_val) < 50:
                        is_new = False
                        break
                if is_new:
                    jumlah_produk += 1
                    objek_terhitung.append((cy, frame_idx))
                    cv2.line(frame, batas_garis_end, batas_garis_start, (0, 255, 0), 2)


        last_detections = detections

    # draw detections from last processing step (keeps display smooth)
    for det in last_detections:
        x, y, w, h = det['box']
        cx, cy = det['center']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"({cx},{cy})", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        

    # --- MEMBUAT UI (USER INTERFACE) ---
    # Tombol EXIT buatan (Merah) di kanan atas
    cv2.rectangle(frame, (700, 10), (790, 50), (0, 0, 255), -1)
    cv2.putText(frame, "EXIT", (715, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Overlay settings
    overlay = frame.copy()
    # Rectangle parameters
    x, y, w, h = 10, 10, 262, 250
    cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 0, 0), -1)
    alpha = 0.4
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    
    # Text on overlay
    cv2.putText(frame, f"Product Details :", (25, 38), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f"Index : #0362", (25, 70), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Name : Cosmetic", (25, 90), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Type  : H3", (25, 110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Source : Main Production", (25, 130), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Count Prod. : {jumlah_produk}", (25, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # # Teks Jumlah
    # cv2.putText(frame, f"Total Produk: {jumlah_produk}", (22, 389), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("CAM Conveyor", frame)
    out.write(frame)

    # Tombol backup untuk keluar: tekan 'q' di keyboard
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    # read next frame for the loop
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (800, 450))
        frame_idx += 1

cap.release()
out.release()
cv2.destroyAllWindows()