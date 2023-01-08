import argparse
import json
import tkinter as tk
import tkinter.font as font
from transcription import Transcription

class Application:
  def __init__(self, args):
    self.model = args.model
    self.model_list = ['tiny','base', 'small', 'medium', 'large']
    self.font_size = args.font_size
    self.side = args.side
    self.side_list = ['top', 'bottom']

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

    # メニューバー
    menubar = tk.Menu(root, bg='green', fg='blue')
    # 設定
    config_menu = tk.Menu(menubar, tearoff=False)
    # モデル選択
    config_model_menu = tk.Menu(config_menu, tearoff=False)
    self.model_var = tk.IntVar()
    config_model_menu.add_radiobutton(label='tiny', command=self.config_model_menu_click, variable=self.model_var, value=0)
    config_model_menu.add_radiobutton(label='base', command=self.config_model_menu_click, variable=self.model_var, value=1)
    config_model_menu.add_radiobutton(label='small', command=self.config_model_menu_click, variable=self.model_var, value=2)
    config_model_menu.add_radiobutton(label='medium', command=self.config_model_menu_click, variable=self.model_var, value=3)
    config_model_menu.add_radiobutton(label='large', command=self.config_model_menu_click, variable=self.model_var, value=4)
    self.model_var.set(self.model_list.index(self.model))
    # フォントサイズ
    config_font_size_menu = tk.Menu(config_menu, tearoff=False)
    # 字幕の位置
    config_side_menu = tk.Menu(config_menu, tearoff=False)
    self.side_var = tk.IntVar()
    config_side_menu.add_radiobutton(label='top', command=self.config_side_menu_click, variable=self.side_var, value=0)
    config_side_menu.add_radiobutton(label='bottom', command=self.config_side_menu_click, variable=self.side_var, value=1)
    self.side_var.set(self.side_list.index(self.side))

    # サブメニューを配置
    config_menu.add_cascade(label='モデル', menu=config_model_menu)
    config_menu.add_cascade(label='フォントサイズ', menu=config_font_size_menu)
    config_menu.add_cascade(label='字幕の位置', menu=config_side_menu)
    menubar.add_cascade(label="設定", menu=config_menu)
    root.config(menu=menubar)

    # ボールド体、フォントサイズ30に設定
    myfont = font.Font(weight='bold', size=self.font_size)

    self.label = tk.Label(root, text='ここに字幕が表示されます', font=myfont)
    if self.side == 'bottom':
      self.label.pack(side=tk.BOTTOM)
    elif self.side == 'top':
      self.label.pack(side=tk.TOP)

    return root
  
  def config_model_menu_click(self):
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.model = self.model_list[self.model_var.get()]
      config_dict['user_config']['model'] = self.model
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
  
  def config_side_menu_click(self):
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.side = self.side_list[self.side_var.get()]
      config_dict['user_config']['side'] = self.side
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))

    if self.side == 'bottom':
      self.label.pack(side=tk.BOTTOM)
    elif self.side == 'top':
      self.label.pack(side=tk.TOP)
  
  def set_to_default(self):
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      config_dict['user_config'] = config_dict['default_config']
      self.model = config_dict['user_config']['model']
      self.font_size = config_dict['user_config']['font-size']
      self.side = config_dict['user_config']['side']
      self.model_var.set(self.model)
      self.side_var.set(self.side)
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
    
    if self.side == 'bottom':
      self.label.pack(side=tk.BOTTOM)
    elif self.side == 'top':
      self.label.pack(side=tk.TOP)

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