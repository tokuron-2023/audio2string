#!/usr/bin/env python3
import cv2
import rospy
import os
import roslib
import time
from sensor_msgs.msg import Image
from std_srvs.srv import SetBool, SetBoolResponse
from cv_bridge import CvBridge, CvBridgeError

class camera_subscriber_node():
    def __init__(self):
        rospy.init_node("camera_subscriber", anonymous=True)
        rospy.Service("capture_img", SetBool, self.capture_srv)
        # rospy.Service("start_nav", SetBool, self.capture_srv)
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber("camera/img", Image, self.img_callback)
        self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
        self.path = roslib.packages.get_pkg_dir('audio2string') + '/data/'
        os.makedirs(self.path + self.start_time)
        rospy.spin()

    def img_callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def capture_srv(self, req):
        if req.data:
            self.capture()
            return SetBoolResponse(True, "Image captured successfully")
        else:
            return SetBoolResponse(False, "Invalid request")

    def capture(self):
        rospy.wait_for_service("/capture_img")
        image_path = os.path.join(self.path + self.start_time, "test.png")
        cv2.imwrite(image_path, self.cv_image)
        print("caputure_img successfully")

if __name__ == '__main__':
    camera_subscriber_node()