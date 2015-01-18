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

def buildScene(walls, roof, scale):
	#build scene
	#load room and set scale
	walls = viz.addChild('models/new/room_large.osgb')
	walls.setScale(scale, scale, scale)
	walls.disable(viz.PICKING)
	#walls.setEuler( [ 90, 0, 0 ] )
	#walls.setPosition([0,0,2.5])
	roof = viz.addChild('models/new/roof_large.osgb')
	roof.setScale(scale, scale, scale)
	roof.disable(viz.PICKING)

def init(viz, viztracker):
	viz.setMultiSample(4)
	viz.go()
	viz.MainWindow.fov(60)
	#vizshape.addAxes()
	viz.collision(viz.ON)
	viz.mouse(viz.OFF)
	viz.go(viz.FULLSCREEN)
	viztracker.go()
	keyTracker = viztracker.Keyboard6DOF()
	keyTracker.setPosition(0, 1.8, 10) 
	viz.link(keyTracker, viz.MainView)
	viztracker.get("movable").setPosition([0,1.8,10])

def enableNavigation(tracker, viz):
	tracker = vizcam.addWalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=1.0, turnScale=1.0)
	tracker.setPosition([0,1,10])
	#viz.MainView.setPosition(0, 1.8, 10) 
	#viz.link(tracker,viz.MainView)



def makeShapes( viz, vizshape):
	#Make selectable shapes
	box1 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.BLUE)
	box1.setPosition([-1,1.35,12])
	box1.name = 'BOX_BLUE'
	ball1 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.YELLOW)
	ball1.setPosition([-0.7,1.35,12])
	ball1.name = 'SPHERE_YELLOW'
	tube1 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.GREEN)
	tube1.setPosition([-0.4,1.35,12])
	tube1.name = 'CYLINDER_GREEN'
	tri1 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.PURPLE)
	tri1.setPosition([-0.1,1.25,12])
	tri1.name = 'TRIANGLE_PURPLE'
	box2 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.RED)
	box2.setPosition([0.2,1.35,12])
	box2.name = 'BOX_RED'
	ball2 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.GREEN)
	ball2.setPosition([0.6,1.35,12])
	ball2.name = 'BALL_GREEN'
	tube2 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.BLUE)
	tube2.setPosition([0.9,1.35,12])
	tube2.name = 'CYCLINDER_BLUE'
	tri2 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
	tri2.setPosition([1.2,1.25,12])
	tri2.name = 'TRIANGLE_YELLOW'
	box3 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.GREEN)
	box3.setPosition([-1,1.35,-12])
	box3.name = 'BOX_GREEN'
	ball3 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.BLUE)
	ball3.setPosition([-0.7,1.35,-12])
	ball3.name = 'SPHERE_BLUE'
	tube3 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.RED)
	tube3.setPosition([-0.4,1.35,-12])
	tube3.name = 'CYLINDER_RED'
	tri3 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
	tri3.setPosition([-0.1,1.25,-12])
	tri3.name = 'TRIANGLE_YELLOW'
	box4 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.PURPLE)
	box4.setPosition([0.2,1.35,-12])
	box4.name = 'BOX_PURPLE'
	ball4 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.BLUE)
	ball4.setPosition([0.6,1.35,-12])
	ball4.name = 'SPHERE_BLUE'
	tube4 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.YELLOW)
	tube4.setPosition([0.9,1.35,-12])
	tube4.name = 'CYCLINDER_YELLOW'
	tri4 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.GREEN)
	tri4.setPosition([1.2,1.25,-12])
	tri4.name = 'TRIANGLE_GREEN'


def addSensors(stationOne, stationTwo, stationOneSensor, stationTwoSensor, doorStation, doorStationSensor):
	stationOne = viz.addChild('plant.osgb',pos=[0, 0, 10],scale=[1, 1, 1])
	stationOne.disable(viz.PICKING)
	stationOne.disable(viz.RENDERING)
	stationOneSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=stationOne)

	doorStation = viz.addChild('plant.osgb',pos=[0, 0, 0],scale=[1,1,1])
	doorStation.disable(viz.PICKING)
	doorStation.disable(viz.RENDERING)
	#doorStationSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=doorStation)
	doorStationSensor = vizproximity.Sensor(vizproximity.Box([2.5,2.5,3.5]),source=viz.Matrix.translate(0,1.75,0))

	stationTwo = viz.addChild('plant.osgb',pos=[0, 0, -12],scale=[1, 1, 1])
	stationTwo.disable(viz.PICKING)
	stationTwo.disable(viz.RENDERING)
	stationTwoSensor = vizproximity.Sensor(vizproximity.Box([3,4,3],center=[0,1.5,1]),source=stationTwo)
	target = vizproximity.Target(viz.MainView)

	#Create proximity manager
	manager = vizproximity.Manager()

	#Add destination sensors to manager
	manager.addSensor(stationOneSensor)
	manager.addSensor(stationTwoSensor)
	manager.addSensor(doorStationSensor)
	#Add viewpoint target to manager
	manager.addTarget(target)

	#Toggle debug shapes with keypress
	vizact.onkeydown('t',manager.setDebug,viz.TOGGLE)

#save results into document
def saveResults(participant, result):
	print 'Saving results...'
	#Write the data to our file.
	question_data = open('results.txt','a')
	data = "\n############################"
	data += "\nfirst name: " + participant.firstName
	data += "\nlast name: " + participant.lastName
	data += "\ngroup: " + participant.group
	data += "\nage group: " + participant.ageGroup

	data += "\nresults: " + str(result) +"\t"
	question_data.write(data)
	#Flush the internal buffer.
	question_data.flush()
	return

def displayOnCenterPanel(text):
	return vizinfo.InfoPanel(text,align=viz.ALIGN_CENTER,fontSize=22,icon=False,key=None)

def removeCenterPanel(panel):
	panel.remove()
	return