import argparse
import json
import tkinter as tk
import tkinter.font as font
from transcription import Transcription

class Application:
  def __init__(self, args):
    self.model = args.model
    self.font_size = args.font_size
    self.side = args.side

    # tkinterでWindowを構築
    root = self.builder_window()
    self.start_transcription()
    root.mainloop()

  def start_transcription(self):
    ts = Transcription(model=self.model, label=self.label)
    ts.start_transcription()

  def builder_window(self):
    root = tk.Tk()
    root.title('Overlay-Auto-Subtitle')
    root.geometry('500x300')
    root.config(bg='white')
    # 常に最前面に配置
    root.wm_attributes('-topmost', True)
    # 白を透過する
    root.wm_attributes('-transparentcolor', 'white')

    # ボールド体、フォントサイズ30に設定
    myfont = font.Font(weight='bold', size=self.font_size)

    self.label = tk.Label(root, text='ここに字幕が表示されます', font=myfont)
    if self.side == 'bottom':
      self.label.pack(side=tk.BOTTOM)
    elif self.side == 'top':
      self.label.pack(side=tk.TOP)

    return root

def get_args():
  parser = argparse.ArgumentParser()
  with open('src/config.json', 'r') as json_file:
    config_dict = json.load(json_file)
    model = config_dict['user_config']['model']
    font_size = config_dict['user_config']['font-size']
    side = config_dict['user_config']['side']
  parser.add_argument('--model', default=model, choices=['tiny','base', 'small', 'medium', 'large'])
  parser.add_argument('--font_size', type=int, default=font_size, choices=range(5, 50))
  parser.add_argument('--side', default=side, choices=['bottom','top'])
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  app = Application(get_args())