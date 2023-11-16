#!/usr/bin/env python3
import cv2
import rospy
from std_msgs.msg import String

class camera_capture_node():
    def __init__(self):
       self.sub = rospy.Subscriber("/speech_to_text", String, self.callback)
       self.text = ""


    def callback(self, data):
        self.text = data

    def capture(self):
        if len(self.text.data) > 0:
            #select port number(0, 1, 2, ...)
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cv2.imwrite("test.png", frame)
            cap.release()