
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QLineEdit, QMainWindow, QProgressBar, QPushButton, QComboBox

import pyperclip
import sys
import pafy 

class Youtubers (QMainWindow):
    
    def __init__(self):
        super(Youtubers,self).__init__()
      
        self.__window()
        self.__paste()
        self.__loader()
        self.__combo()
        self.__save()
        self.__combo_button()
        self.__editText()
        self.__progres_bar()
        self.__save_text()
        
    def __window(self):  
        self.setWindowTitle("Loader YouTube Video")  # Титульний текст
        self.setGeometry(500, 300, 450,350)   # Розміщення вікна на моніторі і величина вікна

    def __progres_bar(self):    
        self.progres = QProgressBar(self)
        self.progres.move (15,270)
        self.progres.setFixedWidth(430)
    
    def __editText(self):    
        self.text = QLineEdit(self) # Створюємо поле для вводу тексту
        self.text.setPlaceholderText("Вставте силку для скачування" )
        self.text.move(130,35 ) # Розміщення поля у вікні
        self.text.setFixedWidth(300)
    
    def __combo(self):
        self.combo = QComboBox(self)
        self.combo.addItems(["Формат відео"])
        self.combo.move(130,160)
        self.combo.setFixedWidth(300)
   
    def __save_text(self): 
        self.SaveText = QLineEdit(self)
        self.SaveText.setPlaceholderText("Виберіть папку для зберігання" )
        self.SaveText.move(130,100 )
        self.SaveText.setFixedWidth(300)

    def __paste(self):
        self.paste_button = QPushButton(self)
        self.paste_button.move(15,35)
        self.paste_button.setText('Paste')
        self.paste_button.clicked.connect(self.Paste)
    
    def __loader(self): 
        self.Loader_button = QPushButton(self)
        self.Loader_button.move(180, 210)
        self.Loader_button.setText('Loader')
        self.Loader_button.clicked.connect(self.download)
    
    def __combo_button(self):
        self.Combo_button = QPushButton(self)
        self.Combo_button.move(15, 160)
        self.Combo_button.setText('Вибір')
        self.Combo_button.clicked.connect(self.Combo)

    def __save(self): 
        self.Save_button = QPushButton(self) # Кнопка вибору каталогу 
        self.Save_button.move(15, 100)
        self.Save_button.setText('Save')
        self.Save_button.clicked.connect(self.saveFile)

    def Paste(self):
        self.rezult = pyperclip.paste()
        self.text.setText(self.rezult)
       
 
    def saveFile(self):         # Select directory metod
        self.file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select file")
        if self.file != "":
            self.SaveText.setText(self.file)
    
    def Combo(self):            # Loading video streams into combobox
        self.rezult = self.text.text()
        print(self.rezult)
        v = pafy.new(self.rezult)
        self.streams = {}

        for stream in v.streams:
            self.streams[str(stream)] = stream
        self.combo.clear()
        self.combo.addItems(list(self.streams.keys()))

    def download (self):         # Start download video metod
        self.quality =  self.combo.currentText()
        self.finish_url = self.streams[ self.quality ]
        self.th = Downloader(self.finish_url, self.file, self)
        self.th.download()
    
    def progress(self, size):    # Progress bar metod
        self.progres.setValue(size)


class Downloader(): 
   
    def __init__(self, url = None, file = None, ui_object = None) -> None:
        self.url = url 
        self.file = file  
        self.ui_object = ui_object
            
    def download (self): 
        filename = self.url.download(self.file, quiet=True, callback=self.mycb)  
        
    def mycb(self, total, recvd, ratio, rate, eta):
        self.ui_object.progress(ratio * 100)   

def youtube():
    app = QApplication(sys.argv)  # передаємо системні настройки даного компютера
    window = Youtubers()

    window.show()  # Запускаємо вікно
    sys.exit(app.exec_()) #Коректне закривання програми

if __name__ == '__main__':
    youtube()