import viz
import vizshape
import vizact
import random
import vizinput
import vizcam
import viztask
import vizproximity
import vizfx.postprocess
import vizinfo

view = None
resultPanel = None
startingInstructions = 'test'

def init():
	print "init called"
	viz.setMultiSample(4)
	viz.go()
	viz.MainWindow.fov(60)
	vizshape.addAxes()
	piazza = viz.addChild('piazza.osgb')
	viz.collision(viz.ON)
	view = viz.MainView
	# Create panel to display trial results
	resultPanel = vizinfo.InfoPanel('',align=viz.ALIGN_CENTER,fontSize=25,icon=False,key=None)
	resultPanel.visible(False)
	
	# Setup keyboard/mouse tracker
	tracker = vizcam.addWalkNavigate(moveScale=2.0)
	tracker.setPosition([0,1.8,0])
	viz.link(tracker,viz.MainView)
	viz.mouse.setVisible(False)
	generateQuestions()
	return

def displayOnCenterPanel(text):
	return vizinfo.InfoPanel(text,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)

def removeCenterPanel(panel):
	panel.remove()
	return

#Use test group to determine the environment to load (with or without door)
def loadEnvironment():
	print "loadEnvironment called"

	panel = vizinfo.InfoPanel(startingInstructions,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)
	#data = yield viztask.waitKeyDown(' ')
	#panel.remove()
	return

#Place user inside room with start prompt
def beginExperiment():
	print "beginExperiment called"
	return


