#!/usr/bin/env python3
import cv2
import rospy
from std_srvs.srv import SetBool

class camera_capture_node():
    def __init__(self):
        rospy.init_node("camera_capture")
        rospy.Service("/capture_img", SetBool, self.capture_srv)
        # rospy.Service("start_nav", SetBool, self.capture_srv)
        rospy.spin()

    def capture_srv(self, req):
        if req.data:
            self.capture()
        return True

    def capture(self):
        # rospy.wait_for_service("start_nav")
        rospy.wait_for_service("/capture_img")
        #select port nu)mber(0, 1, 2, ...)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("test.png", frame)
        cap.release()
        print("caputure_img successfully")

if __name__ == '__main__':
    camera_capture_node()