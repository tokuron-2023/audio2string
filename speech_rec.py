#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import pyaudio
import speech_recognition as sr

# 音声認識オブジェクトを作成
r = sr.Recognizer()

# マイクを使うための設定
mic = sr.Microphone()
sample_rate = 44100
chunk_size = 512

# マイクから音声を取得する関数
def get_audio():
    # マイクを開く
    with mic as source:
        print("start record")
        # 音声のノイズを除去
        r.adjust_for_ambient_noise(source)
        # 音声を録音
        audio = r.listen(source)
    # 音声を返す
    return audio

# 音声をテキストに変換する関数
def get_text(audio):
    # Google Speech Recognitionに音声を送る
    try:
        # 音声をテキストに変換
        print("convert success!!")
        text = r.recognize_google(audio, language="ja-JP")
    # エラーが発生した場合
    except sr.RequestError as e:
        # エラーメッセージを表示
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        # テキストを空にする
        text = ""
    # テキストを返す
    return text

# メインの処理
if __name__ == "__main__":
    rospy.init_node("speech_to_text")
    pub = rospy.Publisher("speech_to_text", String, queue_size=10)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        # 音声を取得
        audio = get_audio()
        # 音声をテキストに変換
        text = get_text(audio)
        # テキストが空でない場合
        if text:
            # テキストを表示
            print(text)
            pub.publish(text)
            rospy.loginfo("Text ' {}' published".format(text))
        rate.sleep()
