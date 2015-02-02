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
	viz.mouse(viz.OFF)
	viz.go(viz.FULLSCREEN)
	viztracker.go()
	#keyTracker = viztracker.Keyboard6DOF()
	#keyTracker.setPosition(0, 1.8, 10) 
	#viz.link(keyTracker, viz.MainView)
	#viztracker.get("movable").setPosition([0,1.8,10])

def makeBag(viewTracker, bagNumber):
	bag = vizshape.addBox(size = [0.3 ,0.6,0.2], color = viz.WHITE)
	bag.name = 'BAG' + str(bagNumber)
	bagLink = viz.link(viewTracker, bag)
	if (bagNumber == 1):
		bagLink.postTrans([0,-1,0.5])
	else:
		bagLink.postTrans([0,-1,-0.5])
	return bagLink

def enableNavigation(viewTracker, mouseTracker, viz, viztracker):
	#viewTracker = vizcam.addWalkNavigate(forward='w', backward='s', left='a', right='d', moveScale=1.0, turnScale=1.0)
	#viewTracker.setPosition([0,1,10])
	
	viewTracker = viztracker.Keyboard6DOF()
	viewTracker.setPosition([0,1.8,10])
	viewlink = viz.link( viewTracker, viz.MainView )
	##viewlink.preTrans([0,1.8,0])
	
	#viz.collision(viz.ON)
	#viz.MainView.collision( viz.ON )
	viewTracker.collision( viz.ON )
	viewTracker.gravity (0)
	#mouseTracker = viztracker.MouseTracker()
	#trackerlink = viz.link( mouseTracker, arrow )
	#trackerlink.postTrans([0,0,-4])
	#viz.MainView.setPosition(0, 1.8, 10) 
	#viz.link(tracker,viz.MainView)
	return viewTracker

def makeShapes1( viz, vizshape):
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
	ball2.name = 'SPHERE_GREEN'
	tube2 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.BLUE)
	tube2.setPosition([0.9,1.35,12])
	tube2.name = 'CYCLINDER_BLUE'
	tri2 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
	tri2.setPosition([1.2,1.25,12])
	tri2.name = 'TRIANGLE_YELLOW'
	

	#Second row of shapes. 
	box3 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.BLUE)
	box3.setPosition([-1,1.35,-12])
	box3.name = 'BOX_BLUE'
	ball3 =  vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.YELLOW)
	ball3.setPosition([-0.7,1.35,-12])
	ball3.name =  'SPHERE_YELLOW' 
	tube3 =vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.GREEN)
	tube3.setPosition([-0.4,1.35,-12])
	tube3.name = 'CYLINDER_GREEN'
	tri3 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.PURPLE)
	tri3.setPosition([-0.1,1.25,-12])
	tri3.name = 'TRIANGLE_PURPLE'
	box4 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.RED)
	box4.setPosition([0.2,1.35,-12])
	box4.name =  'BOX_RED'
	ball4 =vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.GREEN)
	ball4.setPosition([0.6,1.35,-12])
	ball4.name = 'SPHERE_GREEN'
	tube4 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.BLUE)
	tube4.setPosition([0.9,1.35,-12])
	tube4.name = 'CYCLINDER_BLUE'
	tri4 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
	tri4.setPosition([1.2,1.25,-12])
	tri4.name =  'TRIANGLE_YELLOW'
	
	shapesArray = [box1, ball1, tube1, tri1, box2, ball2, tube2, tri2]
	return shapesArray


def makeShapes2( viz, vizshape):
		#final row of shapes
	#Make selectable shapes
	box5 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.BLUE)
	box5.setPosition([-1,1.35,12])
	box5.name = 'BOX_BLUE'
	ball5 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.YELLOW)
	ball5.setPosition([-0.7,1.35,12])
	ball5.name = 'SPHERE_YELLOW'
	tube5 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.GREEN)
	tube5.setPosition([-0.4,1.35,12])
	tube5.name = 'CYLINDER_GREEN'
	tri5 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.PURPLE)
	tri5.setPosition([-0.1,1.25,12])
	tri5.name = 'TRIANGLE_PURPLE'
	box6 = vizshape.addBox(size = [0.2,0.2,0.2], color = viz.RED)
	box6.setPosition([0.2,1.35,12])
	box6.name = 'BOX_RED'
	ball6 = vizshape.addSphere(radius=0.1,slices=10,stacks=10, color = viz.GREEN)
	ball6.setPosition([0.6,1.35,12])
	ball6.name = 'SPHERE_GREEN'
	tube6 = vizshape.addCylinder(height=0.2,radius=0.1,topRadius=None,bottomRadius=None,slices=10,bottom=True,top=True, color = viz.BLUE)
	tube6.setPosition([0.9,1.35,12])
	tube6.name = 'CYCLINDER_BLUE'
	tri6 = vizshape.addPyramid(base=(0.2,0.2),height=0.2, color = viz.YELLOW)
	tri6.setPosition([1.2,1.25,12])
	tri6.name = 'TRIANGLE_YELLOW'
	shapesArray = [box5, ball5, tube5, tri5, box6, ball6, tube6, tri6]
	return shapesArray

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

