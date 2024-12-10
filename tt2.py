import cv2

# Mở video
cap = cv2.VideoCapture("video/video_2.mp4")

if not cap.isOpened():
    print("Không thể mở video.")
    exit()

# Lấy FPS của video
fps = cap.get(cv2.CAP_PROP_FPS)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Hiển thị khung hình
    cv2.imshow("Video", frame)

    # Đảm bảo đúng tốc độ chơi
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):  # 'q' để thoát
        break

cap.release()
cv2.destroyAllWindows()
