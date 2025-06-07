import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)


if __name__ == '__main__':
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertendo a imagem para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectando as mãos
        result = hands.process(rgb_frame)

        # Desenhando os pontos-chave nas mãos detectadas
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Exibindo o resultado
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
