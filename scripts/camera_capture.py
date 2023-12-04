#!/usr/bin/env python3
import cv2
import rospy
import os
import roslib
import time
from std_srvs.srv import SetBool, SetBoolResponse

class camera_capture_node():
    def __init__(self):
        rospy.init_node("camera_capture")
        rospy.Service("capture_img", SetBool, self.capture_srv)
        # rospy.Service("start_nav", SetBool, self.capture_srv)
        self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
        self.path = roslib.packages.get_pkg_dir('tokuron') + '/data/'
        os.makedirs(self.path + self.start_time)
        rospy.spin()

    def capture_srv(self, req):
        if req.data:
            self.capture()
            return SetBoolResponse(True, "Image captured successfully")
        else:
            return SetBoolResponse(False, "Invalid request")

    def capture(self):
        # rospy.wait_for_service("start_nav")
        rospy.wait_for_service("/capture_img")
        #select port nu)mber(0, 1, 2, ...)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        image_path = os.path.join(self.path + self.start_time, "test.png")
        cv2.imwrite(image_path, frame)
        cap.release()
        print("caputure_img successfully")

if __name__ == '__main__':
    camera_capture_node()