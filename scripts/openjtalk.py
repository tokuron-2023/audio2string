#!/usr/bin/env python3
#coding: utf-8

import subprocess
import rospy
from datetime import datetime
from std_srvs.srv import SetBool

class openjtalk_node():
    def __init__(self):
        rospy.init_node("openjtalk")
        rospy.Service("start_nav", SetBool, self.start_srv)
        rospy.Service("capture_img", SetBool, self.capture_srv)
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

    def start_srv(self, req):
        if req.data:
            self.say_start()
        return True

    def capture_srv(self, req):
        if req.data:
            self.say_capture()
        return True
    
    def say_start(self):
        # d = datetime.now()
        # text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
        # self.jtalk(text)
        rospy.wait_for_service("start_nav")
        try:
            text = '案内を開始します'
            self.jtalk(text)
            print("案内を開始します")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
    
    def say_capture(self):
        # rospy.wait_for_service("capture_img")
        try:
            text = '撮影します'
            self.jtalk(text)
            print("撮影します")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    openjtalk_node()