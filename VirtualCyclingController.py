import cv2
import math
import time
import vgamepad as vg
import mediapipe as mp

class VirtualCyclingController:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.gamepad = vg.VX360Gamepad()
        
        self.rpm = 0
        self.tick = 0
        self.flag = False
        self.start_time = self.end_time = time.time()
    
    @staticmethod
    def calculate_distance(point1, point2):
        return int(math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2))

    def run(self):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)
            body = []

            if results.pose_landmarks:
                h, w, _ = frame.shape
                body = [(int(lm.x * w), int(lm.y * h)) for lm in results.pose_landmarks.landmark]
                self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                
                try:
                    distance = self.calculate_distance(body[28], body[24])

                    cv2.putText(frame, f"Distance: {distance}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.line(frame,body[28],body[24],(255,0,0),2)
                except Exception as e:
                    print(f"Error processing landmarks: {e}")

            cv2.imshow("Virtual Cycling Controller", frame)
            self.gamepad.update()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()