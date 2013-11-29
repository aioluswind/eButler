from PyQt4 import QtGui, QtCore
import signal, sys

def signal_handler(signal, frame):
	sys.exit(0)

basepos = QtCore.QPoint(400, 200)
relativepos = QtCore.QPoint(-200, -150)

object1name = 'butler'
object2name = 'cloud'

splashs = []

class SplashScreen(QtGui.QWidget):
 	def __init__(self, pixmap, name):
		QtGui.QWidget.__init__(self)
		self._name = name
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
		if self._name == object1name:
			self._mousePressPos = None
			if event.button() == QtCore.Qt.LeftButton:
				self._mousePressPos = event.globalPos()
				self._originalPos = self.pos()
		elif self._name == object2name:
			self.hide()
	
	def mouseMoveEvent(self, event):
		if self._name == object1name:
			globalPos = event.globalPos()
			diff = globalPos - self._mousePressPos
			# move object1 and object2
			self.move(self._originalPos + diff)
			splashs[1].move(self.pos() + relativepos)

def show_splash(path, path2):
	image = QtGui.QPixmap(path)
	image2 = QtGui.QPixmap(path2)
	splash = SplashScreen(image, object1name)
	splash2 = SplashScreen(image2, object2name)
	font = QtGui.QFont(splash.font())
	font.setPointSize(font.pointSize() + 5)
	splash.setFont(font)

	splash2.show()
	splash.show()
	splash.move(basepos)
	splash2.move(basepos + relativepos)
	splash2.showMessage(splash2.tr('Hello World!!'), QtCore.Qt.AlignCenter)

	splashs.append(splash)
	splashs.append(splash2)

	QtGui.QApplication.processEvents()
	
	while True:
		QtGui.QApplication.processEvents()

if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	# draw a butler
	show_splash(sys.argv[1], sys.argv[2])

