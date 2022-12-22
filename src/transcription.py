import whisper
import torch
import soundcard as sc
import threading
import queue
import numpy as np
import argparse

class Transcription:
  def __init__(self, model='base', label=None):
    self.SAMPLE_RATE = 16000
    self.INTERVAL = 3
    self.BUFFER_SIZE = 4096

    self.label = label

    # whisperから自動音声認識モデルを読み込み
    print('音声認識モデルを読み込み中・・・')
    self.model = whisper.load_model(model, device='cpu')
    if torch.cuda.is_available():
      _ = self.model.cuda()
      print('GPU推論モードで実行します')
    else:
      print('CPU推論モードで実行します')
    print('-------------------------')

    self.recognition_waiting_audio = queue.Queue()
    self.b = np.ones(100) / 100

    self.options = whisper.DecodingOptions(language='ja', fp16=False)

  def start_transcription(self):
    # システム音声の自動認識を開始
    self.th_recognize = threading.Thread(target=self.recognize, daemon=True)
    self.th_recording = threading.Thread(target=self.recording, daemon=True)
    self.th_recognize.start()
    self.th_recording.start()

  def recording(self):
    # システム音声を取得
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.SAMPLE_RATE, channels=1) as mic:
      audio = np.empty(self.SAMPLE_RATE * self.INTERVAL + self.BUFFER_SIZE, dtype=np.float32)
      data_length = 0
      while True:
        while data_length < self.SAMPLE_RATE * self.INTERVAL:
          data = mic.record(self.BUFFER_SIZE)
          audio[data_length:data_length+len(data)] = data.reshape(-1)
          data_length += len(data)
        
        # 音声の後半(4/5 ~ 5/5)区間で音が小さい区間を探し、その区間で区切る
        breakpoint = data_length * 4 // 5
        vol = np.convolve(audio[breakpoint:data_length] ** 2, self.b, 'same')
        breakpoint += vol.argmin()
        self.recognition_waiting_audio.put(audio[:breakpoint])

        # 持ち越し分の音声
        audio_prev = audio
        audio = np.empty(self.SAMPLE_RATE * self.INTERVAL + self.BUFFER_SIZE, dtype=np.float32)
        audio[:data_length-breakpoint] = audio_prev[breakpoint:data_length]
        data_length = data_length-breakpoint

  def recognize(self):
    # 音声認識
    while True:
      audio = self.recognition_waiting_audio.get()
      if(audio ** 2).max() > 0.001:
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)

        print(f'recognize result: {result.text}')
        if self.label is not None:
          self.label['text']=result.text