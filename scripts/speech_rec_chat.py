#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import speech_recognition as sr

class speech_to_text_node:
    def __init__(self):
        rospy.init_node("speech_to_text")
        self.pub = rospy.Publisher("speech_to_text", String, queue_size=1)
        self.rate = rospy.Rate(10)

        self.r = sr.Recognizer()

        self.mic = sr.Microphone()
        self.sample_rate = 44100
        self.chunk_size = 512

        self.chat_templates = ["こんにちは"]

        self.new_message_received = False
    
    def get_audio(self):
        with self.mic as source:
            print("start record")
            # 音声のノイズを除去
            self.r.adjust_for_ambient_noise(source)
            # 音声を録音(5秒録音)
            self.audio = self.r.listen(source, timeout=8)
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
    
    def chat_template_matching(self, text):
        for template in self.chat_templates:
            if template in text:
                return True
        return False

    def wait_for_hello(self):
        while not self.chat_template_matching(self.get_text(self.get_audio())):
            pass

    def spin(self):
        while not rospy.is_shutdown():
            self.wait_for_hello()

            # self.new_message_received = True
            self.new_message_received = False
            print("こんにちは, 何かご用ですか？")

            audio = self.get_audio()
            text = self.get_text(audio)
            if text:
                print(text)
                self.pub.publish(text)
                rospy.loginfo("Text '{}' published".format(text))

                # self.wait_for_hello()
                self.rate.sleep()

        self.new_message_received = False

if __name__ == "__main__":
    rg = speech_to_text_node()
    rg.spin()
