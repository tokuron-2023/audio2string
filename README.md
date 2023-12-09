# tokuron  
このパッケージは音声入力から以下のことができます  
- 文字として出力し, string型でpublish
- 特定の文字が来た場合にserviceを投げる  

## このリポジトリをcloneして使えるようにするまでの手順  

## install
* 環境 ubuntu20.04, ros noetic, python3  

* ワークスペースの用意
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
cd ../
catkin build
```
* tokuronの用意
```
cd ~/catkin_ws/src
git clone https://github.com/YukiTakahashi4690/tokuron.git
catkin build tokuron
```
* ライブラリのinstall（for speech_rec.py & speech_rec_chat.py）  
```
pip3 install SpeechRecognition
sudo apt-get install portaudio19-dev  
pip3 install PyAudio  
```
* ライブラリのinstall（for openjtalk.py）
```
sudo apt install open-jtalk
sudo apt-get install open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
```
## 使い方  
```  
roscore  
```  
- "**Enter**" keyで録音する場合
```
python3 speech_rec.py
```
- "**こんにちは**"と呼びかけて録音する場合  
> **"こんにちは"と呼びかけない限り, 文字をpublishしません. また, serviceも投げません**  
```  
python3 speech_rec_chat.py
```
or  
```
python3 speech_rec_srv.py
```
- 写真を取る
> **写真**や**撮影**などの単語に反応して写真が撮れます  
> 例）写真を撮ってください  
> 写真はscripts内に保存されます
```
python3 camera_capture.py  
```
- テキストの読み上げ
> ファイル内のテキストを変更することで任意の文章を読み上げます
```
python3 openjtalk.py
```
- まとめて起動
```
roslaunch tokuron tokuron.launch
```
> launchで起動する場合, 撮影がされないためうまく動作しません  
> 現在調査中...  
