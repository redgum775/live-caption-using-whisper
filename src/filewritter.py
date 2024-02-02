from tkinter import filedialog

class FileWriter():
  def __init__(self):
    typ = [('テキストファイル', '*.txt')]
    dir = './'
    self.filename = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 

  def write(self, text):
    with open(self.filename, 'a', encoding='utf-8') as fp:
      fp.write(f'{text}\n')
  