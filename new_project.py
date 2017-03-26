#!/usr/bin/env python3
import sys, os
from os import listdir
from os.path import isfile, join, isdir
import re

from PyQt5.QtCore import(QSize, pyqtSignal)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,QPushButton,QWidget, QHBoxLayout,QAction,qApp, QLineEdit)
from PyQt5.QtGui import (QIcon ,QPixmap)

class Project(QPushButton):	
	m_name=""
	m_type=""
	m_comment=""
	m_icon=""
	m_folder=""
	def __init__(self):
		super().__init__("Button")
		
	def UpdateUI(self):
		icon=QIcon()
		icon.addPixmap(QPixmap(self.m_icon))
		self.setIcon(icon)
		self.setText(self.m_name)
		self.setToolTip(self.m_comment)
		self.setAutoDefault(True)
		self.clicked.connect(self.ProjectClickedEvent)
		
	projectClicked=pyqtSignal()
		
	def ProjectClickedEvent(self):
		print("Project is clicked "+self.m_name)
		self.projectClicked.emit()
	

class MainWindow(QMainWindow):

	mainwidget=None
	projlist=list()
	def __init__(self):
		super().__init__()
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.projlist=ListAvailableProjects()
		self.setWindowIcon(QIcon.fromTheme("applications-development"))
		self.initUI()	
        
	def initUI(self):     
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		self.statusBar()
		self.setWindowTitle('New Project')    
		self.showMaximized()
		
		self.GoToMainView()
	
	def ApplyWidget(self):
		vlayout=QVBoxLayout()
		hlayout=QHBoxLayout()
		okbutton=QPushButton(QIcon.fromTheme("dialog-ok-apply"),"Ok")
		cancelbutton=QPushButton(QIcon.fromTheme("dialog-cancel"),"Cancel")
		cancelbutton.clicked.connect(self.GoToMainView)
		wfolderlineedit=QLineEdit("/home/max/")
		wfolderbutton=QPushButton(QIcon.fromTheme("document-open-folder"),"Open")
		wfolderselection=QWidget()
		wfolderselection.setLayout(QHBoxLayout())
		wfolderselection.layout().addWidget(wfolderbutton)
		wfolderselection.layout().addWidget(wfolderlineedit)
		projectnameedit=QLineEdit("ProjectName")	#TODO define focus on me
		projectnameedit.setFocus()
		hlayout.addWidget(okbutton)
		hlayout.addWidget(cancelbutton)
		bottomwidget=QWidget()
		bottomwidget.setLayout(hlayout)
		vlayout.addWidget(projectnameedit)
		vlayout.addWidget(wfolderselection)
		vlayout.addWidget(bottomwidget)
		widget=QWidget()
		widget.setLayout(vlayout)
		self.setCentralWidget(widget)
		
	def GoToMainView(self):
		mainlayout=QVBoxLayout()
		for p in self.projlist :
			p.UpdateUI()
			mainlayout.addWidget(p)
		mainlayout.addStretch(1)
		widget=QWidget()
		widget.setLayout(mainlayout)
		self.setCentralWidget(widget)
		
def ReadATemplateDesktopFile(file):
	with open(file) as f:  #This conserve the \namenamen at en of lines
		content = [line.rstrip('\n') for line in open(file)]	#while this approach does not	
	proj=Project()
	for line in content:
		if "Name=" in line:
			proj.m_name=re.sub(r'Name=','',line)
		if "Type=" in line:
			proj.m_type=re.sub(r'Type=','',line)
		if "Comment=" in line:
			proj.m_comment=re.sub(r'Comment=','',line)
		if "Icon=" in line:
			proj.m_icon=re.sub(r'Icon=','',line)
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
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
