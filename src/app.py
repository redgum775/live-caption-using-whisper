import argparse
import json
import tkinter as tk
import tkinter.font as font
from transcription import Transcription

class Application:
  def __init__(self, args):
    self.model = args.model
    self.lang = args.lang
    self.font_size = args.font_size
    self.side = args.side

    # tkinterでWindowを構築
    root = self.builder_window()
    self.start_transcription()
    root.mainloop()

  def start_transcription(self):
    self.ts = Transcription(model_name=self.model, lang=self.lang, label=self.label)
    self.ts.start_transcription()

  def builder_window(self):
    root = tk.Tk()
    root.title('Live Caption using Whisper')
    root.geometry('500x300')
    root.config(bg='green')

    # 常に最前面に配置
    root.wm_attributes('-topmost', True)
    # 緑を透過する
    root.wm_attributes('-transparentcolor', 'green')

    # メニューバー
    menubar = tk.Menu(root)

    # 設定メニュー
    config_menu = tk.Menu(menubar, tearoff=False)

    # モデル選択選択メニュー
    config_model_menu = tk.Menu(config_menu, tearoff=False)
    self.model_var = tk.StringVar()
    config_model_menu.add_radiobutton(label='tiny', command=self.config_model_menu_click, variable=self.model_var, value='tiny')
    config_model_menu.add_radiobutton(label='base', command=self.config_model_menu_click, variable=self.model_var, value='base')
    config_model_menu.add_radiobutton(label='small', command=self.config_model_menu_click, variable=self.model_var, value='small')
    config_model_menu.add_radiobutton(label='medium', command=self.config_model_menu_click, variable=self.model_var, value='medium')
    config_model_menu.add_radiobutton(label='large', command=self.config_model_menu_click, variable=self.model_var, value='large')
    self.model_var.set(self.model)

    # 使用言語選択メニュー
    config_lang_menu = tk.Menu(config_menu, tearoff=False)
    self.lang_var = tk.StringVar()
    config_lang_menu.add_radiobutton(label='日本語', command=self.config_lang_menu_click, variable=self.lang_var, value='ja')
    config_lang_menu.add_radiobutton(label='English', command=self.config_lang_menu_click, variable=self.lang_var, value='en')
    config_lang_menu.add_radiobutton(label='Auto', command=self.config_lang_menu_click, variable=self.lang_var, value='auto')
    self.lang_var.set(self.lang)

    # フォントサイズ選択メニュー
    config_font_size_menu = tk.Menu(config_menu, tearoff=False)
    self.font_size_var = tk.IntVar()
    config_font_size_menu.add_radiobutton(label='16', command=self.config_font_size_menu_click, variable=self.font_size_var, value=16)
    config_font_size_menu.add_radiobutton(label='24', command=self.config_font_size_menu_click, variable=self.font_size_var, value=24)
    config_font_size_menu.add_radiobutton(label='32', command=self.config_font_size_menu_click, variable=self.font_size_var, value=32)
    config_font_size_menu.add_radiobutton(label='40', command=self.config_font_size_menu_click, variable=self.font_size_var, value=40)
    self.font_size_var.set(self.font_size)

    # 字幕の位置選択メニュー
    config_side_menu = tk.Menu(config_menu, tearoff=False)
    self.side_var = tk.StringVar()
    config_side_menu.add_radiobutton(label='top', command=self.config_side_menu_click, variable=self.side_var, value='top')
    config_side_menu.add_radiobutton(label='bottom', command=self.config_side_menu_click, variable=self.side_var, value='bottom')
    self.side_var.set(self.side)

    # サブメニューを配置、メニューバーに設定メニューを配置
    config_menu.add_cascade(label='モデル', menu=config_model_menu)
    config_menu.add_cascade(label='言語', menu=config_lang_menu)
    config_menu.add_cascade(label='フォントサイズ', menu=config_font_size_menu)
    config_menu.add_cascade(label='字幕の位置', menu=config_side_menu)
    config_menu.add_command(label='デフォルトに戻す', command=self.set_to_default)
    menubar.add_cascade(label="設定", menu=config_menu)
    root.config(menu=menubar)

    # 字幕ラベルを配置
    self.label = tk.Label(root, text='ここに字幕が表示されます')
    self.set_subtitle_font()
    self.set_subtitle_position()

    return root

  # 字幕のフォントを設定する
  def set_subtitle_font(self):
    myfont = font.Font(weight='bold', size=self.font_size)
    self.label.config(font=myfont)
  
  # 字幕の表示位置を設定する
  def set_subtitle_position(self):
    if self.side == 'bottom':
      self.label.pack(side=tk.BOTTOM)
    elif self.side == 'top':
      self.label.pack(side=tk.TOP)
  
  # モデル選択選択メニューからモデルが選択されたときの処理
  def config_model_menu_click(self):
    # configファイルに反映
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.model = self.model_var.get()
      config_dict['user_config']['model'] = self.model
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))

    # モデルを切り替える処理
    self.ts.switch_model(self.model)
  
  # 使用言語選択メニューから言語が選択されたときの処理
  def config_lang_menu_click(self):
    # configファイルに反映
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.lang = self.lang_var.get()
      config_dict['user_config']['lang'] = self.lang
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))

    # 音声認識の言語を切り替える処理
    self.ts.set_decoding_option(lang=self.lang)

  # フォントサイズ選択メニューからフォントサイズが選択されたときの処理
  def config_font_size_menu_click(self):
    # configファイルに反映
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.font_size = self.font_size_var.get()
      config_dict['user_config']['font-size'] = self.font_size
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
    
    # 字幕のフォントを変える処理
    self.set_subtitle_font()
  
  # 字幕の位置選択メニューから位置が選択されたときの処理
  def config_side_menu_click(self):
    # configファイルに反映
    with open('src/config.json', 'r') as json_file:
      config_dict = json.load(json_file)
      self.side = self.side_var.get()
      config_dict['user_config']['side'] = self.side
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
    
    # 字幕の位置を変える処理
    self.set_subtitle_position()
  
  # 設定メニューからデフォルトに戻すが選択されたときの処理
  def set_to_default(self):
    # configファイルに反映
    with open('src/config.json', 'w+') as json_file:
      config_dict = json.load(json_file)
      config_dict['user_config'] = config_dict['default_config']
      self.model = config_dict['user_config']['model']
      self.font_size = config_dict['user_config']['font-size']
      self.side = config_dict['user_config']['side']
      self.model_var.set(self.model)
      self.side_var.set(self.side)
    with open('src/config.json', 'w') as json_file:
      json.dump(config_dict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
    
    # デフォルトに戻す処理
    self.ts.switch_model(self.model)
    self.ts.set_decoding_option(lang=self.lang)
    self.set_subtitle_font()
    self.set_subtitle_position()

def get_args():
  parser = argparse.ArgumentParser()
  with open('src/config.json', 'r') as json_file:
    config_dict = json.load(json_file)
    model = config_dict['user_config']['model']
    lang = config_dict['user_config']['lang']
    font_size = config_dict['user_config']['font-size']
    side = config_dict['user_config']['side']
  parser.add_argument('--model', default=model, choices=['tiny','base', 'small', 'medium', 'large'])
  parser.add_argument('--lang', default=lang, choices=['ja','en', 'auto'])
  parser.add_argument('--font_size', type=int, default=font_size, choices=range(5, 50))
  parser.add_argument('--side', default=side, choices=['bottom','top'])
  args = parser.parse_args()
  return args

if __name__ == '__main__':
  app = Application(get_args())