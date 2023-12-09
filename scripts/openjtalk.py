#!/usr/bin/env python3
#coding: utf-8

import subprocess
import rospy
from datetime import datetime
from std_srvs.srv import SetBool, SetBoolResponse
from std_msgs.msg import String

class openjtalk_node():
    def __init__(self):
        rospy.init_node("openjtalk")
        # rospy.Service("/openjtalk/start_nav", SetBool, self.start_srv)
        # rospy.Service("/openjtalk/capture_img", SetBool, self.capture_srv)
        # rospy.Subscriber("/speech_to_text", String, self.callback)
        rospy.Subscriber("/gpt_string", String, self.gpt_callback)

        rospy.spin()

    def jtalk(self, text, voice="f"):
        open_jtalk = ['open_jtalk']
        mecab_dict = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
        if voice == "f":
        # 女性音声
            htsvoice = ['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
        else:
        # 男性音声
            htsvoice = ['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
        # 音声スピード
        speed = ['-r','1.0']
        outwav = ['-ow','test.wav']
        cmd = open_jtalk+mecab_dict+htsvoice+speed+outwav
        try:
            c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
            c.stdin.write(text.encode('utf-8'))
            c.stdin.close()
            c.wait()
            # aplay = ['aplay','-q','test.wav','-Dhw:1,0']
            aplay = ['aplay', '-q', 'test.wav', '-Dsysdefault']
            wr = subprocess.Popen(aplay)
        except Exception as e:
            print(f"jtalkでエラーが発生しました: {e}")

    # def callback(self, data):
    #     self.received_msg = data.data
    #     self.speech_template_matching()

    def gpt_callback(self, data):
        self.gpt_msg = data.data
        self.speech_gpt()

    # def speech_template_matching(self):
    #     if "案内" in self.received_msg:
    #         text = '案内を開始します'
    #         self.jtalk(text)
    #         print("案内を開始します")
    #     elif "ナビゲーション" in self.received_msg:
    #         text = 'ナビゲーションを開始します'
    #         self.jtalk(text)
    #         print("ナビゲーションを開始します")
    #     elif "撮影" in self.received_msg:
    #         text = '撮影します'
    #         self.jtalk(text)
    #         print("撮影します")
    #     elif "写真" in self.received_msg:
    #         text = '写真を撮ります'
    #         self.jtalk(text)
    #         print("写真を撮ります")
    #     else:
    #         pass

    def speech_gpt(self):
        self.jtalk(self.gpt_msg)

    # def start_srv(self, req):
    #     if req.data:
    #         self.say_start()
    #         return SetBoolResponse(True, "Start nav successfully")
    #     else:
    #         return SetBoolResponse(False, "Invalid request")
        
    # def capture_srv(self, req):
    #     if req.data:
    #         self.say_capture()
    #         return SetBoolResponse(True, "Image captured successfully")
    #     else:
    #         return SetBoolResponse(False, "Invalid request")
    
    # def say_start(self):
    #     # d = datetime.now()
    #     # text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    #     # self.jtalk(text)
    #     # rospy.wait_for_service("start_nav")
    #     try:
    #         text = '案内を開始します'
    #         self.jtalk(text)
    #         print("案内を開始します")
    #     except Exception as e:
    #         print(f"エラーが発生しました: {e}")
    
    # def say_capture(self):
    #     # rospy.wait_for_service("capture_img")
    #     try:
    #         text = '撮影します'
    #         self.jtalk(text)
    #         print("撮影します")
    #     except Exception as e:
    #         print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    openjtalk_node()
    # openjtalk = openjtalk_node()
    # openjtalk.speech_template_matching()