import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel

if __name__ =='__main__':
    myApp = QApplication(sys.argv)

    appLabel = QLabel()
    appLabel.setText("Hello, World!!!\n Traditional first app using PyQt5")
    appLabel.setAlignment(Qt.AlignCenter)
    appLabel.setGeometry(300,300,250,175)

    appLabel.show()

    myApp.exec_()
    sys.exit()
