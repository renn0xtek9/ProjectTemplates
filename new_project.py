#!/usr/bin/env python3
import sys, os
from os import listdir
from os.path import isfile, join, isdir
import re

from PyQt5.QtCore import(QSize)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,QPushButton,QWidget, QHBoxLayout,QAction,qApp, QLineEdit)
from PyQt5.QtGui import (QIcon ,QPixmap)

class Project:	
	name=""
	type=""
	comment=""
	icon=""
	folder=""
	projlist=list()
	def __init__(self):
		pass
	def apply(self):
		print("Will apply projects"+self.name)
		#input=UserInput()
		

class UserInput(QWidget):
	

	def __init__(self,Title):
		super().__init__()
		self.initUI(Title)
		
	def initUI(self,Title):
		self.setFixedSize(400,400)
		self.setWindowTitle(Title)
		vlayout=QVBoxLayout()
		hlayout=QHBoxLayout()
		okbutton=QPushButton("OK")
		cancelbutton=QPushButton("Cancel")
		lineedit=QLineEdit("ProjectName")
		hlayout.addWidget(cancelbutton)
		hlayout.addWidget(okbutton)
		bottomwidget=QWidget()
		bottomwidget.setLayout(hlayout)
		vlayout.addWidget(bottomwidget)
		vlayout.addWidget(lineedit)
		self.setLayout(vlayout)
		self.hide()
		

class MainWindow(QMainWindow):
	
	
    
	def __init__(self,projectlist):
		super().__init__()
		self.projlist=projectlist
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.initUI()
		icon=QIcon()
		icon.addPixmap(QPixmap("applications-development.png")) #TODO marche pas
		self.setWindowIcon(icon)
        
	def initUI(self):     
		userinput=UserInput("Merde")
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		self.statusBar()
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		self.showMaximized()
		self.setWindowTitle('New Project')    
		layout=QVBoxLayout()
		layout.addStretch(1)
		for p in self.projlist :
			icon=QIcon()
			icon.addPixmap(QPixmap(p.icon))
			button=QPushButton(icon,p.name)
			button.setToolTip(p.comment)
			button.clicked.connect(p.apply)
			button.clicked.connect(userinput.show)
			button.clicked.connect(self.hide)
			button.setAutoDefault(True)
			layout.addWidget(button)
		layout.addWidget(button)
		centralwideget=QWidget()
		centralwideget.setLayout(layout)
		self.setCentralWidget(centralwideget)
	#def PromptUser(self):
		#windowtitle=""
		

def ReadATemplateDesktopFile(file):
	with open(file) as f:  #This conserve the \namenamen at en of lines
		content = [line.rstrip('\n') for line in open(file)]	#while this approach does not	
	proj=Project()
	for line in content:
		if "Name=" in line:
			proj.name=re.sub(r'Name=','',line)
		if "Type=" in line:
			proj.type=re.sub(r'Type=','',line)
		if "Comment=" in line:
			proj.comment=re.sub(r'Comment=','',line)
		if "Icon=" in line:
			proj.icon=re.sub(r'Icon=','',line)
	return proj	

def ListAvailableProjects():
	folder="/home/max/Templates/Project_Templates"
	projectlist=list()
	onlyfiles = [f for f in listdir(folder) if (isdir(join(folder, f)) and isfile(join(folder,f,"template.desktop")))]
	for file in onlyfiles:
		proj=ReadATemplateDesktopFile(join(folder,file,"template.desktop"))
		proj.folder=join(folder,file)
		projectlist.append(proj)
	return projectlist

if __name__ == '__main__':
	projectlist=ListAvailableProjects()
	app = QApplication(sys.argv)
	ex = MainWindow(projectlist)
	sys.exit(app.exec_())
