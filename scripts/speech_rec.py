#!/usr/bin/env python3
import rospy
from std_srvs.srv import SetBool
from std_msgs.msg import String
import speech_recognition as sr
import time

class speech_to_text_node:
    def __init__(self):
        rospy.init_node("speech_to_text")
        self.pub = rospy.Publisher("speech_to_text", String, queue_size=1)
        self.rate = rospy.Rate(10)

        self.r = sr.Recognizer()

        self.mic = sr.Microphone()
        self.sample_rate = 44100
        self.chunk_size = 512

        self.nav_templates = ["ナビゲーション", "開始"]
        self.img_templates = ["写真", "撮影"]

        rospy.Service("start_nav", SetBool, self.start_nav_srv)
        rospy.Service("capture_img", SetBool, self.capture_img_srv)

    def start_nav_srv(self, req):
        if req.data:
            rospy.loginfo("Service 'start_nav' called with True")
        return {"success": True, "message": "Service called successfully"}
    
    def capture_img_srv(self, req):
        if req.data:
            rospy.loginfo("Service 'capture_srv' called with True")
        return {"success": True, "message": "Service called successfully"}
    
    def get_audio(self):
        # 'Enter' キーが押されるまで待機
        input("Press 'Enter' to start recording...")
        time.sleep(2)

        with self.mic as source:
            print("start record")
            # 音声のノイズを除去
            self.r.adjust_for_ambient_noise(source)
            # 音声を録音(5秒録音)
            self.audio = self.r.listen(source, timeout=5)
        return self.audio

    def get_text(self, audio):
        try:
            print("convert success!!")
            self.text = self.r.recognize_google(audio, language="ja-JP")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.text = ""
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.text = ""
        return self.text

    def nav_template_matching(self, text):
        for template in self.nav_templates:
            if template in text:
                return True
        return False
    
    def img_template_matching(self, text):
        for template in self.img_templates:
            if template in text:
                return True
        return False

    def spin(self):
        while not rospy.is_shutdown():
            audio = self.get_audio()
            text = self.get_text(audio)
            if text:
                print(text)
                self.pub.publish(text)
                rospy.loginfo("Text '{}' published".format(text))

                if self.nav_template_matching(text):
                    rospy.wait_for_service("start_nav")
                    try: 
                        start_nav = rospy.ServiceProxy("start_nav", SetBool)
                        start_nav(True)
                    except rospy.ServiceException as e:
                        print("Service call failed: {0}".format(e))

                elif self.img_template_matching(text):
                    rospy.wait_for_service("capture_img")
                    try: 
                        capture_img = rospy.ServiceProxy("capture_img", SetBool)
                        capture_img(True)
                    except rospy.ServiceException as e:
                        print("Service call failed: {0}".format(e))
            self.rate.sleep()
                    

if __name__ == "__main__":
    rg = speech_to_text_node()
    # while not rospy.is_shutdown():
    rg.spin()
        # rg.rate.sleep()
