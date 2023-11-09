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

    @staticmethod
    def calculate_rpm(time_frame):
        return 60 * 4 / time_frame

    @staticmethod
    def calculate_angle(point1, point2):
        theta = math.atan((point2[0] - point1[0])/(point2[1] - point1[1]))
        return int(theta*180/math.pi)

    @staticmethod
    def midpoint(point1, point2):
        return (int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))


    def control_rotation(self, distance, body_presence):
        try:
            if body_presence:
                if distance <= 170 and not self.flag:
                    self.tick += 1
                    self.flag = True
                if distance > 170 and self.flag:
                    self.tick += 1 
                    self.flag = False

                
                if self.tick ==1:
                    self.start_time = time.time()
                if self.tick == 9:
                    self.end_time = time.time()
                    self.flag = False
                    temp = [self.start_time,self.end_time]
                    time_total = abs(max(temp)-min(temp))
                    self.tick = 0
                    self.rpm = self.calculate_rpm(time_total)  

                if(self.tick > 1 and (abs(self.start_time - time.time()) > 5 or abs(self.end_time - time.time()) > 5) ):
                    self.rpm = 0
                    self.tick = 0
                    self.flag = False
                    self.start_time = self.end_time = time.time() 

        except Exception as e:
            print(f"Error controlling rotation: {e}")

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
                    self.control_rotation(distance, body)
                    mid_point = self.midpoint(body[24], body[23])
                    angle = self.calculate_angle(mid_point, body[0])
                    cv2.putText(frame, f"Distance: {distance} RPM: {int(self.rpm)} Angle: {angle}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.line(frame,body[28],body[24],(255,0,0),2)
                except Exception as e:
                    print(f"Error processing landmarks: {e}")

            cv2.imshow("Virtual Cycling Controller", frame)
            self.gamepad.update()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()