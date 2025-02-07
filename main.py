import sys
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
class Weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather App')
        self.label = QLabel("Enter City name:", self)
        self.ui = QLineEdit(self)
        self.getB = QPushButton("Get Weather", self)
        self.describer = QLabel(self)
        self.displayer = QLabel(self.describer)
        self.label_1 = QLabel(self.describer)
        self.label_2 = QLabel(self.describer)
        self.initUI()
    def initUI(self):
        self.setGeometry(500, 300, 300, 400)
        self.setStyleSheet('''
                            font-family: Arial;
                            font-weight: bold;
                            background-color: #f5e9f7;
                            color: #50d5b7;;
                                ''')
        self.label.setFixedHeight(50)
        self.ui.setStyleSheet('border-radius: 5px;'
                            'border: #000000 3px solid;'
                            'opacity: 0.8'
                            )
        self.getB.setStyleSheet("margin-top: 10px;"
                                "height: 20px;")
        self.getB.clicked.connect(self.get_w)
        self.label.setAlignment(Qt.AlignCenter)
        self.ui.setPlaceholderText("Example: Marrakech")
        main_wid = QWidget()
        self.setCentralWidget(main_wid)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.ui)
        vbox.addWidget(self.getB)
        vbox.addWidget(self.describer)
        main_wid.setLayout(vbox)
        self.describer.setStyleSheet("font-size: 20px;")
        self.label_1.setFixedHeight(50)
        self.label_2.setFixedHeight(50)
        vbox_2 = QVBoxLayout()
        vbox_2.addWidget(self.label_1)
        vbox_2.addWidget(self.displayer)
        vbox_2.addWidget(self.label_2)
        self.describer.setLayout(vbox_2)

    def get_w(self):
        self.getB.hide()
        API_c  = '9d7b00bdb4534543a4a174145250602'
        city = self.ui.text()
        url = f"http://api.weatherapi.com/v1/current.json?key={API_c}&q={city.upper()}&aqi=yes"
        x = requests.get(url)
        if x.status_code != 200:
            self.label_1.setText('Invalid input, or may\nthe connection was lost.')
        else:
            x = x.json()
            y = {
                'location': x['location']['name'] +"\n" + x['location']['country'],
                'tempeture': [x['current']['temp_c'], x['current']['temp_f']],
                'img_url': x['current']['condition']['icon'],
                'description': x['current']['condition']['text']
            }
            self.label_1.setText(f"{y.get('description')} in {y.get('location')}.")
            self.label_2.setText(f"{y.get('tempeture', [])[0]}C | {y.get('tempeture', [])[1]}F")
            self.label_1.setAlignment(Qt.AlignCenter)
            self.label_2.setAlignment(Qt.AlignCenter)
            url = f"https:{y.get('img_url')}"
            z =  requests.get(url)
            self.img = QPixmap()
            self.img.loadFromData(z.content)
            self.displayer.setPixmap(self.img)
            self.displayer.setAlignment(Qt.AlignCenter)

App = QApplication(sys.argv)
Window = Weather_app()
Window.show()
sys.exit(App.exec_())