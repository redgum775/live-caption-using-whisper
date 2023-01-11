# live-caption-using-whisper  
[OpenAIのWhisper](https://openai.com/blog/whisper/)を使用して、PCのシステム音声から字幕を自動的に生成して、Tkinterによる透過ウィンドウに字幕を表示させます。  

## Introduction  
- FFmpegをインストール ([FFmpegの公式Webサイト](https://www.ffmpeg.org/download.html)をチェックしてください)  
- PyTorchをインストール (環境によってインストールするバージョンが異なります。[PyTorchの公式Webサイト](https://pytorch.org/)をチェックしてください)
  - CPU推論モードでも動きますが遅延が大きくなるため、GPU推論モードを使用することを推奨します。
- 必要なpipパッケージをインストール  
```sh
# SoundCardのインストール  
pip install SoundCard  
# whisperのインストール  
pip install git+https://github.com/openai/whisper.git  
```
- ※文字起こしの際にスピーカーから音声を流したくない人向け (このステップは無視しても構いません)  
  - 仮想オーディオデバイス[VB-Cableをインストール](https://vb-audio.com/Cable/) (Linux系は対応していないため、別の仮想オーディオデバイスを探してDLしてください)    
  - 音声出力先をCABLE Input (VB-Audio Virtual Cable)に変更 (Linux系はDLした仮想オーディオデバイスに合わせて変更してください)  
- `src/app.py`を実行  
```sh
# 実行
python src/app.py  
```

文字起こしされない、精度が悪い時は音量を調整してください  

## Option  
- --model (default value: `base`)  
  - 使用する自動音声認識モデルを選択します。使用できるモデル一覧は[こちら](https://github.com/openai/whisper/blob/main/model-card.md)から確認してください。  
- --font_size (default value: `24`)  
  - フォントサイズを選択します。`5`~`50`の範囲で選択できます。  
- --side (default value: `bottom`)
  - 字幕の位置を選択します。`top`と`bottom`の二択です。  

例: 
```sh
# mediumモデルを使用する・フォントサイズを30にする
python src/app.py --model=medium --font_size=30
```
複数オプションを使用する場合、スペースで区切ってください。  
また、オプションはウィンドウの設定メニューから変更することができます。  

## Reference  
- [Introducing Whisper](https://openai.com/blog/whisper/)
- [openai/whisper](https://github.com/openai/whisper)
- [PCで再生中の音声をWhisperでリアルタイムに文字起こしする](https://tadaoyamaoka.hatenablog.com/entry/2022/10/15/175722)  
- [VB-Cable 仮想オーディオ・ケーブル (Virtual Audio Cable)](https://kii-memo.blogspot.com/2020/09/vb-cable.html)  

## Author  
- [@redgum775](https://twitter.com/redgum775) (Twitter)  

## License  
- [MIT License](LICENSE)  