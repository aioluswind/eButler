from PyQt4 import QtGui, QtCore
import signal, sys

def signal_handler(signal, frame):
	sys.exit(0)

class SplashScreen(QtGui.QWidget):
 	def __init__(self, pixmap):
		QtGui.QWidget.__init__(self)
		self._pixmap = pixmap
		self._message = QtCore.QString()
		self._color = QtGui.QColor.black
		self._alignment = QtCore.Qt.AlignLeft
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
		                    QtCore.Qt.WindowStaysOnTopHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setFixedSize(self._pixmap.size())
		self.setMask(self._pixmap.mask())

		# registe stop signal (^c)
		signal.signal(signal.SIGINT, signal_handler)

	def clearMessage(self):
		self._message.clear()
		self.repaint()

	def showMessage(self, message, alignment=QtCore.Qt.AlignLeft,
	                               color=QtGui.QColor.black):
		self._message = QtCore.QString(message)
		self._alignment = alignment
		self._color = color
		self.repaint()

	def paintEvent(self, event):
		textbox = QtCore.QRect(self.rect())
		textbox.setRect(textbox.x() + 5, textbox.y() + 5,
		                textbox.width() - 10, textbox.height() - 10)
		painter = QtGui.QPainter(self)
		painter.drawPixmap(self.rect(), self._pixmap)
		painter.setPen(QtGui.QColor(self._color))
		painter.drawText(textbox, self._alignment, self._message)

	def mousePressEvent(self, event):
		self._mousePressPos = None
		if event.button() == QtCore.Qt.LeftButton:
			self._mousePressPos = event.globalPos()
			self._originalPos = self.pos()
	
	def mouseMoveEvent(self, event):
		globalPos = event.globalPos()
		diff = globalPos - self._mousePressPos
		self.move(self._originalPos + diff)

def show_splash(path):
	image = QtGui.QPixmap(path)
	splash = SplashScreen(image)
	font = QtGui.QFont(splash.font())
	font.setPointSize(font.pointSize() + 5)
	splash.setFont(font)
	splash.show()
	QtGui.QApplication.processEvents()
	while True:
		QtGui.QApplication.processEvents()

if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	show_splash(sys.argv[1])
