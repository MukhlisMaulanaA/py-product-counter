import cv2

# Variabel global untuk menyimpan koordinat
clicked_point = None

# Fungsi callback mouse
def mouse_callback(event, x, y, flags, param):
    global clicked_point

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"Koordinat diklik: X={x}, Y={y}")

# Buka video (0 untuk webcam, atau ganti dengan path video)
cap = cv2.VideoCapture('0326.mp4')

# Ambil nama window
window_name = "Video Coordinate Tracker"

cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (800, 450))
    # Jika ada titik diklik, tampilkan di frame
    if clicked_point is not None:
        x, y = clicked_point

        # Gambar titik
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

        # Tampilkan teks koordinat
        text = f"({x}, {y})"
        cv2.putText(frame, text, (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow(window_name, frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()