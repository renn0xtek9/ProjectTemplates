#!/usr/bin/env python3
import sys, os,subprocess
from os import listdir
from os.path import isfile, join, isdir
import re
import shutil
from PyQt5.QtCore import(QSize, pyqtSignal)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,QPushButton,QWidget, QHBoxLayout,QAction,qApp, QLineEdit,QFileDialog,QStackedWidget)
from PyQt5.QtGui import (QIcon ,QPixmap)


class Project(QPushButton):	
	m_name=""
	m_type=""
	m_comment=""
	m_iconurl=""
	m_folder=""
	def __init__(self):
		super().__init__("Button")
		self.m_icon=QIcon()
		
	def UpdateUI(self):
		self.m_icon.addPixmap(QPixmap(self.m_iconurl))
		self.setIcon(self.m_icon)
		self.setText(self.m_name)
		self.setToolTip(self.m_comment)
		self.setAutoDefault(True)
		self.clicked.connect(self.ProjectClickedEvent)
		
	projectClicked=pyqtSignal(object)
		
	def ProjectClickedEvent(self):
		self.projectClicked.emit(self)
	

class MainWindow(QMainWindow):

	mainwidget=None
	projlist=list()
	
	m_wmainwidget=None 
	m_wapplywidget=None
	m_stackedwidget=None
	def __init__(self):
		super().__init__()
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.projlist=ListAvailableProjects()
		self.setWindowIcon(QIcon.fromTheme("applications-development"))
		self.initUI()	
        
	def initUI(self):   
		self.m_stackedwidget=QStackedWidget(self)
		self.m_wmainwidget=QWidget(self)
		self.m_wapplywidget=QWidget(self)
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
		self.initApplyWidget()
		self.initMainWidget()
		self.m_stackedwidget.addWidget(self.m_wmainwidget)
		self.m_stackedwidget.addWidget(self.m_wapplywidget)
		self.setCentralWidget(self.m_stackedwidget)
		self.GoToMainView()
		
	def initApplyWidget(self):
		vlayout=QVBoxLayout()
		hlayout=QHBoxLayout()
		okbutton=QPushButton(QIcon.fromTheme("dialog-ok-apply"),"Ok")
		okbutton.clicked.connect(self.CreateNewProject)
		cancelbutton=QPushButton(QIcon.fromTheme("dialog-cancel"),"Cancel")
		cancelbutton.clicked.connect(self.GoToMainView)
		self.wfolderlineedit=QLineEdit("/home/max/")	#TODO use default path value form within templates
		wfolderbutton=QPushButton(QIcon.fromTheme("document-open-folder"),"Open")
		wfolderbutton.clicked.connect(self.OnFolderSelectionButton)
		wfolderselection=QWidget()
		wfolderselection.setLayout(QHBoxLayout())
		wfolderselection.layout().addWidget(wfolderbutton)
		wfolderselection.layout().addWidget(self.wfolderlineedit)
		self.projectnameedit=QLineEdit("ProjectName")	#TODO define focus on me TODO use default name value
		self.projectnameedit.setFocus()
		hlayout.addWidget(okbutton)
		hlayout.addWidget(cancelbutton)
		bottomwidget=QWidget()
		bottomwidget.setLayout(hlayout)
		vlayout.addWidget(self.projectnameedit)
		vlayout.addWidget(wfolderselection)
		vlayout.addWidget(bottomwidget)
		self.m_wapplywidget.setLayout(vlayout)
	
	def initMainWidget(self):
		self.m_wmainwidget.setLayout(QVBoxLayout())
		for p in self.projlist :
			p.UpdateUI()
			p.projectClicked.connect(self.ApplyWidget)
			self.m_wmainwidget.layout().addWidget(p)
		self.m_wmainwidget.layout().addStretch(1)
	
	def ApplyWidget(self,p_Project):
		self.preselectedproject=p_Project
		self.m_stackedwidget.setCurrentIndex(1)
	def CreateNewProject(self):
		name=self.projectnameedit.text()
		folder=self.wfolderlineedit.text()
		print("process.sh"+name+folder)
		destdir=join(folder,name)
		#os.makedirs(destdir) # create all directories, raise an error if it already exists
		print(self.preselectedproject.m_name)
		print(self.preselectedproject.m_folder)
		shutil.copytree(self.preselectedproject.m_folder, destdir)
		os.chdir(destdir)
		os.remove("template.desktop")
		os.remove("template_description.txt")
		os.remove("template_type.txt")
		os.remove("process.sh")
		spc=subprocess.Popen(["/bin/bash","applyname.sh",name],stdout=subprocess.PIPE)
		out,err=spc.communicate()	#catch stdout and stderr
		outstr=out.decode(sys.stdout.encoding)	#out is a bytstring i.e 'b'blalbal\n'  while outstr now soleley contains blablala
		spc.wait()			#Wait until end (remove if you want parrall exec
		if spc.returncode != 0:
			pass #TODO prompt a Dialog file saying it could not apply the name
		
		#clean with bad files 
		os.remove("applyname.sh")
		
	
	def OnFolderSelectionButton(self):
		selectedfolder=QFileDialog.getExistingDirectory(self,"Select directory where to place new project",os.path.expanduser('~'))
		self.wfolderlineedit.setText(selectedfolder)
		
	def GoToMainView(self):
		self.m_stackedwidget.setCurrentIndex(0)
		
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
			proj.m_iconurl=re.sub(r'Icon=','',line)
	return proj	

def ListAvailableProjects():
	folder="/home/max/Templates/Project_Templates"
	projectlist=list()
	onlyfiles = [f for f in listdir(folder) if (isdir(join(folder, f)) and isfile(join(folder,f,"template.desktop")))]
	for file in onlyfiles:
		proj=ReadATemplateDesktopFile(join(folder,file,"template.desktop"))
		proj.m_folder=join(folder,file)
		projectlist.append(proj)
	return projectlist

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
