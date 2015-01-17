import viztask

ball1 = viz.add('white_ball.wrl')
ball2 = viz.add('white_ball.wrl')
#Create a signal.
changeColorSignal = viztask.Signal()

def colorBall():
    #This task will wait for the signalVi.
    while True:
        yield changeColorSignal.wait()
        ball2.color( viz.RED )
        yield changeColorSignal.wait()
        ball2.color( viz.BLUE )

def moveBall():
    #This task will repeated send the signal.
    while True:
        yield viztask.addAction( ball1, vizact.moveTo([0,0,0],speed=1) )
        changeColorSignal.send()
        yield viztask.addAction( ball1, vizact.moveTo([-1,0,0],speed=1) )
        changeColorSignal.send()

viztask.schedule( colorBall() )
viztask.schedule( moveBall() )