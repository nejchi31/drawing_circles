__author__ = 'Nejchi31'

## Drawing App - Made for job application
## Enjoy!

import sys, random, math
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPainter, QColor, QBrush

class ColourRGB:
    R=0
    G=0
    B=0
    #Constructor
    def __init__(self):
        self.R = 0
        self.G = 0
        self.B = 0
    #Constructor - optional with the values to give in
    def __init__(self, cR, cG, cB):
        self.R = cR
        self.G = cG
        self.B = cB

class Point:
    #X coordinate
    X = 0
    #Y coordinate
    Y = 0
    #Constructor
    def __init__(self):
        self.X = 0
        self.Y = 0
    #Constructor with values in it
    def __init__(self, cX, cY):
        self.X = cX
        self.Y = cY
    #Method to SET both values at the same time
    def Set(self, cX, cY):
        self.X = cX
        self.Y = cY

class Radius:
    rx = 0
    ry = 0
    #Constructor
    def __init__(self):
        self.rx = 0
        self.ry = 0
    #Constructor values in it
    def __init__(self, rX, rY):
        self.rx = rX
        self.ry = rY
    #Method to SET both the same time
    def Set(self, rX, rY):
        self.rx = rX
        self.ry = rY

## Shape - Circle needs to hold data at drawing point
class Circle:
    Location = Point(0, 0)
    Radi = Radius(0, 0)
    ColourDark = ColourRGB(0, 0, 0)
    ColourLight = ColourRGB(0, 0, 0)
    CircleNum = 0
    #Constructor to give value in
    def __init__(self, loc, rad, colD, colL, cir_num):
        self.Location = loc
        self.Radi = rad
        self.ColourDark = colD
        self.ColourLight = colL
        self.CircleNum = cir_num

#This class holds all the drawing circles information and allow quick and easy to use fun to the drawing panel
class Circles:
    #Stores all circles that have been drawn
    __Circles = []
    __selectedC = 0

    #Constructor
    def __init__(self):
        self.__Circles = []
        self.__selectedC = 0

    #Return the number of circles being stored
    def NumOfCircles(self):
        return len(self.__Circles)

    #Add circle to the database, recording its position, radius, colour and circle relation info
    def NewCircle(self, loc, rad, colDark, colLight, cir_num):
        Cr = Circle(loc, rad, colDark, colLight, cir_num)
        self.__Circles.append(Cr)

    def NewCircleColor(self, index, colDark, colLight):
        Cr = self.__Circles[index]
        Cr.ColourDark = colDark
        Cr.ColourLight = colLight
        self.__Circles[index]=Cr


    #Return the circle of the requested data
    def GetCircle(self, Index):
        return self.__Circles[Index]
    #Return selected circle
    def GetSelCircle(self):
        return self.__selectedC
    #Setting index
    def SetSelCircle(self, Index):
        self.__selectedC = Index
    #Remove Circle
    def RemoveCircle(self, index):
        del self.__Circles[index]

#Painter class - handling paint event
class Painter(QtWidgets.QWidget):
    ParentLink = 0
    LastPos = Point(0, 0)
    def __init__(self, parent):
        super(Painter, self).__init__()
        self.ParentLink = parent
        self.LastPos = Point(0, 0)


    def paintEvent(self, event):

        pe = QtGui.QPainter()
        pe.begin(self)
        self.drawCircle(event, pe)
        pe.end()

    def drawCircle(self, event, pe):
        pe.setRenderHint(QtGui.QPainter.Antialiasing)

        for i in range(self.ParentLink.DrawingCircles.NumOfCircles()):
            if self.ParentLink.SelectedCircleBol==True and self.ParentLink.DrawingCircles.GetSelCircle()==i:
                T = self.ParentLink.DrawingCircles.GetCircle(i)
                pen = QtGui.QPen(QtGui.QColor(255, 249, 105))
                pe.setPen(pen)
                center = QtCore.QPoint(T.Location.X, T.Location.Y)
                #Implementing gradiendt brush
                grad = QtGui.QConicalGradient(center, 300)
                dark = QtGui.QColor(T.ColourDark.R, T.ColourDark.G, T.ColourDark.B)
                light = QtGui.QColor(T.ColourLight.R, T.ColourLight.G, T.ColourLight.B)
                grad.setStops([(0.0, dark), (0.5, light), (1.0, dark)])
                pe.setBrush(grad)
                pe.drawEllipse(center, T.Radi.rx, T.Radi.ry)
            else:
                T = self.ParentLink.DrawingCircles.GetCircle(i)
                pen = QtGui.QPen(QtGui.QColor(22, 11, 4))
                pe.setPen(pen)
                #Implementing gradiendt brush
                center = QtCore.QPoint(T.Location.X, T.Location.Y)
                grad = QtGui.QConicalGradient(center, 300)
                dark = QtGui.QColor(T.ColourDark.R, T.ColourDark.G, T.ColourDark.B)
                light = QtGui.QColor(T.ColourLight.R, T.ColourLight.G, T.ColourLight.B)
                grad.setStops([(0.0, dark), (0.5, light), (1.0, dark)])
                pe.setBrush(grad)
                pe.drawEllipse(center, T.Radi.rx, T.Radi.ry)



    #Mouse down event
    def mousePressEvent(self, ev):
        self.LastPos = Point(ev.x(), ev.y())
        # print('Mouse X: {}'.format(self.LastPos.X))
        # print('Mouse Y: {}'.format(self.LastPos.Y))
        self.ParentLink.SelectedCircle()


#Main UIClass and methods
class drawCircle(QtWidgets.QWidget):
    DrawingCircles = Circles()
    CurrentColour = ColourRGB(0, 0, 0)
    CurrentRadius = Radius(10, 10)
    CircleNum = 0
    PaintPanel = 0
    SelectedCircleBol = False
    GradDarkColor = ColourRGB(0, 0, 0)
    GradLightColor = ColourRGB(0, 0, 0)


    #Contructor
    def __init__(self):
        super(drawCircle, self).__init__()
        self.setupUI(self)
        self.PaintPanel = Painter(self)
        self.PaintPanel.close()
        self.drawingWidget.insertWidget(0, self.PaintPanel)
        self.drawingWidget.setCurrentWidget(self.PaintPanel)
        # self.Establish_Conns()


    def setupUI(self, Main):
        self.styleData = ''
        f=open('orange.stylesheet', 'r')
        self.styleData = f.read()
        f.close()
        Main.setGeometry(700, 250, 500, 540)
        Main.setWindowTitle('Drawing Panel')
        Main.setFixedSize(500, 540)
        #Drawing panel
        self.drawingWidget = QtWidgets.QStackedWidget(Main)
        self.drawingWidget.setObjectName('drawingWidget')
        self.drawingWidget.setGeometry(QtCore.QRect(120, 20, 360, 500))
        #Layout tool
        self.verLay1Widget = QtWidgets.QWidget(Main)
        self.verLay1Widget.setGeometry(QtCore.QRect(10, 20, 100, 500))
        self.verLay1 = QtWidgets.QVBoxLayout(self.verLay1Widget)


        #Buttons
        self.buton1 = QtWidgets.QPushButton('Add Circle')
        self.buton1.setToolTip('Draw a circle on drawing area')
        self.buton2 = QtWidgets.QPushButton('Clear All')
        self.buton2.setToolTip('Clear drawing area')
        self.buton3 = QtWidgets.QPushButton('Clear One')
        self.buton3.setToolTip('Delete circle by index respectively or selected one')
        self.buton4 = QtWidgets.QPushButton('Change Color')
        self.buton4.setToolTip('Change color to Solid Color')
        self.buton5 = QtWidgets.QPushButton('Set Gradient')
        self.buton5.setToolTip('Set color for custom gradient layer')
        self.buton6 = QtWidgets.QPushButton('Change Color')
        self.buton6.setToolTip('Change color of selected circle')

        #Setup Slider settings
        self.labelIndex = QtWidgets.QLabel('Drawing \n Circle \n App')
        self.labelIndex.setMaximumHeight(42)
        self.labelIndex.setAlignment(QtCore.Qt.AlignCenter)
        self.labelIndex.setToolTip('@Nejc Necemer, May 2017')
        self.labelRad = QtWidgets.QLabel()
        self.labelRad.setToolTip('Circle Radium in "px"')
        self.sliderRad = QtWidgets.QSlider()
        self.sliderRad.setToolTip('Drag slider to Increase/Decrease circle radium')
        self.sliderRad.setMaximum(150)
        self.sliderRad.setMinimum(5)
        self.sliderRad.setValue(20)
        self.sliderRad.setOrientation(QtCore.Qt.Horizontal)
        self.labelRad.setText(str(20))
        self.labelRad.setMaximumHeight(20)
        self.labelRad.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBlank = QtWidgets.QLabel()
        self.labelBlank.setToolTip('@Nejc Necemer, May 2017')

        #Adding widgets to the layout
        self.verLay1.addWidget(self.labelIndex)
        self.verLay1.addWidget(self.buton1)
        self.verLay1.addWidget(self.buton2)
        self.verLay1.addWidget(self.buton3)
        self.verLay1.addWidget(self.buton4)
        self.verLay1.addWidget(self.buton5)
        self.verLay1.addWidget(self.buton6)
        self.verLay1.addWidget(self.labelRad)
        self.verLay1.addWidget(self.sliderRad)
        self.verLay1.addWidget(self.labelBlank)



        #Establish connections
        self.buton1.clicked.connect(self.activate)
        self.buton2.clicked.connect(self.activateBrisi)
        self.buton3.clicked.connect(self.activateBrisiOne)
        self.buton4.clicked.connect(self.ChangeColour)
        self.buton5.clicked.connect(self.ChangeGradColor)
        self.sliderRad.valueChanged.connect(self.value_changed)
        self.buton6.clicked.connect(self.ChangeSelColor)

        self.setStyleSheet(self.styleData)

    def value_changed(self):
        rad = self.sliderRad.value()
        self.CurrentRadius = Radius(rad, rad)
        self.labelRad.setText(str(rad))

    def activate(self):
        self.PaintPanel.ParentLink.CircleNum += 1
        self.PaintPanel.ParentLink.DrawingCircles.NewCircle(Point(random.randint(0+self.PaintPanel.ParentLink.CurrentRadius.rx,
            360-self.PaintPanel.ParentLink.CurrentRadius.rx), random.randint(0+self.PaintPanel.ParentLink.CurrentRadius.ry,
            500-self.PaintPanel.ParentLink.CurrentRadius.ry)),self.PaintPanel.ParentLink.CurrentRadius, self.PaintPanel.ParentLink.GradDarkColor,
        self.PaintPanel.ParentLink.GradLightColor, self.PaintPanel.ParentLink.CircleNum)
        self.repaint()
    # def Establish_Conns(self):
    #     self.buton1.clicked.connect(Painter.activate)

    #Delete all the circles on the drawing panel
    def activateBrisi(self):
        self.DrawingCircles = Circles()
        self.SelectedCircleBol = False
        self.PaintPanel.repaint()

    #Delete just selected circle
    def activateBrisiOne(self):
        try:
            index = self.PaintPanel.ParentLink.DrawingCircles.GetSelCircle()
            self.PaintPanel.ParentLink.DrawingCircles.RemoveCircle(index)
            self.SelectedCircleBol = False
            self.PaintPanel.repaint()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Upsss mistake")
            msg.setInformativeText("Error")
            msg.setWindowTitle("Incorrect inputs")
            msg.setDetailedText("Try again")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msg.setStyleSheet(self.styleData)
            msg.exec_()

    def SelectedCircle(self):
        #In case of if condition would took more than 1 circle
        try:
            temp = []
            numInd = []
            for i in range(self.PaintPanel.ParentLink.DrawingCircles.NumOfCircles()):
                T = self.PaintPanel.ParentLink.DrawingCircles.GetCircle(i)
                #Check if mouse position on click is in drawing eara of the i-th circle - treshold
                if (T.Location.X-T.Radi.rx <= self.PaintPanel.LastPos.X <= T.Location.X+T.Radi.rx) and (T.Location.Y-T.Radi.ry <= self.PaintPanel.LastPos.Y <= T.Location.Y+T.Radi.ry):
                    print('Match X: {}'.format(T.Location.X))
                    print('Match Y: {}'.format(T.Location.Y))
                    #Pitagorov izrek for the closest point
                    lenght = math.sqrt(math.pow(self.PaintPanel.LastPos.X-T.Location.X, 2)+ math.pow(self.PaintPanel.LastPos.Y-T.Location.Y, 2))
                    temp.append(lenght)
                    numInd.append(i)
                    self.SelectedCircleBol = True
            if not temp:
                self.SelectedCircleBol=False
            else:
                j = temp.index(min(temp))
                self.PaintPanel.ParentLink.DrawingCircles.SetSelCircle(numInd[j])
            self.PaintPanel.repaint()
        except:
            pass

    #Method for changing the color if you select solid mode
    def ChangeColour(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.GradDarkColor = ColourRGB(col.red(),col.green(),col.blue())
            self.GradLightColor = ColourRGB(col.red(),col.green(),col.blue())

    #Change gradient colors by calling a new class
    def ChangeGradColor(self):
        self.changeGrad = GradColorDialog()
        self.GradDarkColor = self.changeGrad.GetDarkColor()
        self.GradLightColor = self.changeGrad.GetLightColor()

    def ChangeRadius(self, rx, ry):
        self.CurrentRadius = Radius(rx, ry)

    def ChangeSelColor(self):
        try:
            tempDC = self.GradDarkColor
            tempLC = self.GradLightColor
            #First we need to get Color we want to change in
            col = QtWidgets.QColorDialog.getColor()
            if col.isValid():
                self.GradDarkColor = ColourRGB(col.red(),col.green(),col.blue())
                self.GradLightColor = ColourRGB(col.red(),col.green(),col.blue())
            #index of selected circle
            index = self.PaintPanel.ParentLink.DrawingCircles.GetSelCircle()
            self.PaintPanel.ParentLink.DrawingCircles.NewCircleColor(index, self.GradDarkColor,  self.GradLightColor)
            self.SelectedCircleBol = False
            #Changing back to previous selected colors
            self.GradDarkColor = tempDC
            self.GradLightColor = tempLC
            self.PaintPanel.repaint()
        except:
            pass


#QDialog class - a new window where color will be selected for purpose of the gradient
class GradColorDialog(QtWidgets.QDialog):
    GradDarkColor = ColourRGB(0, 0, 0)
    GradLightColor = ColourRGB(0, 0, 0)
    #Constructor
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.constructUI(self)

    #Gui method
    def constructUI(self, Dialog):
        # setting stylesheet
        self.styleData = ''
        f=open('orange.stylesheet', 'r')
        self.styleData = f.read()
        f.close()
        #Creating window with associated widgets
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.setSizeGripEnabled(False)
        Dialog.setGeometry(500, 400, 150, 150)
        Dialog.setWindowTitle('Entry Custom Data')

        layout = QtWidgets.QGridLayout(Dialog)
        self.darklabel = QtWidgets.QLabel()
        self.lightlabel = QtWidgets.QLabel()
        label= QtWidgets.QLabel()
        label.setText('Color Selection for custom GRADIENT')


        self.button1 = QtWidgets.QPushButton('Dark')
        self.button1.clicked.connect(self.dark)
        self.button2 = QtWidgets.QPushButton('Light')
        self.button2.clicked.connect(self.light)
        self.button3 = QtWidgets.QPushButton('Accept')
        self.button3.clicked.connect(self.accept)

        layout.addWidget(label,0, 0, 1, 2)
        layout.addWidget(self.button1, 1, 0)
        layout.addWidget(self.darklabel, 1, 1)
        layout.addWidget(self.button2, 2, 0)
        layout.addWidget(self.lightlabel, 2, 1)
        layout.addWidget(self.button3, 3, 1)

        self.setStyleSheet(self.styleData)

        self.exec_()
    #Select Dark Color for gradient and show it on label widget
    def dark(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.GradDarkColor = ColourRGB(col.red(), col.green(), col.blue())
            values = "{}, {}, {}".format(col.red(), col.green(), col.blue())
            self.darklabel.setStyleSheet("QLabel { background-color: rgb("+values+"); }")

    #Select ¸Light Color for gradient and show it on label widget
    def light(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            self.GradLightColor = ColourRGB(col.red(), col.green(), col.blue())
            values = "{}, {}, {}".format(col.red(), col.green(), col.blue())
            self.lightlabel.setStyleSheet("QLabel { background-color: rgb("+values+"); }")
    #closing dialog widget
    def accept(self):
        self.close()

    #Get Dark Color object
    def GetDarkColor(self):
        return self.GradDarkColor
    #Get Light Color object
    def GetLightColor(self):
        return self.GradLightColor



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    global ex
    ex = drawCircle()
    ex.show()
    sys.exit(app.exec_())
