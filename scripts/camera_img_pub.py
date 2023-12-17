#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class camera_publisher_node():
    def __init__(self):
        rospy.init_node('camera_publisher', anonymous=True)
        self.img_pub = rospy.Publisher('camera/img', Image, queue_size=10)
        self.rate = rospy.Rate(10)
        self.cap = cv2.VideoCapture(0)  # 0はカメラのデバイス番号
        self.bridge = CvBridge()

    def publish(self):
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if ret:
                img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                self.img_pub.publish(img_msg)
            self.rate.sleep()

        self.cap.release()

if __name__ == '__main__':
    try:
        camera_node = camera_publisher_node()
        camera_node.publish()
    except rospy.ROSInterruptException:
        pass