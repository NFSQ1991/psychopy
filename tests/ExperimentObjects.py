class LoopHandler(list):    
    def __init__(self, name, loopType, nReps):
        list.__init__(self)
        self.loopType=loopType
        self.name = name
        self.nReps=nReps
    def start(self):
        pass
    def stop(self):
        pass
class LoopInitiator:
    """A simple class for inserting into the flow"""
    def __init__(self, loop):
        self.loop=loop        
class LoopTerminator:
    """A simple class for inserting into the flow"""
    def __init__(self, loop):
        self.loop=loop
        
class Flow(list):
    def addLoop(self, loop, startPos, endPos):
        """Adds initiator and terminator objects for the loop
        into the Flow list"""
        self.insert(int(endPos), LoopTerminator(loop))
        self.insert(int(startPos), LoopInitiator(loop))
    def addProcedure(self, newProc, pos):
        """Adds the object to the Flow list"""
        self.insert(int(pos), newProc)
        
        
class Procedure(list):
    """
    A Procedure determines a single sequence of events, such
    as the presentation of trial. Multiple Procedures might be
    used to comprise an Experiment (e.g. one for presenting
    instructions, one for trials, one for debriefing subjects).
    
    In practice a Procedure is simply a python list of Event objects,
    each of which knows when it starts and stops.
    """
    def __init__(self):
        list.__init__(self)
        
class EventPatch(dict):
    """An event class for presenting image-based stimuli"""
    def __init__(self, name, image, pos, size, ori,onTimes):
        dict.__init__(self)
        self['image']= image
        self['pos']=pos
        self['size']=size
        self['ori']=ori
        self['onTimes']=onTimes
class EventKeyboard(dict):
    """An event class for checking the keyboard at given times"""
    def __init__(self, name, allowedKeys,onTimes):
        self['allowedKeys']=allowedKeys
        self['onTimes']=onTimes
        
class Experiment:
    """
    An experiment contains a single Flow and at least one
    Procedure. The Flow controls how Procedures are organised
    e.g. the nature of repeats and branching of an experiment.
    """
    def __init__(self):
        self.flow = Flow()
        self.procs={}
    def exportToScript(self):
        pass
    def addProcedure(self,procName, proc=None):
        """Add a Procedure to the current list of them. 
        
        Can take a Procedure object directly or will create
        an empty one if none is given.
        """
        if proc==None:
            self.procs[procName]=Procedure()
        else:
            self.procs=proc
        
ourExp = Experiment()
#the following are the sort of commands that should be generated by GUI
#create a new procedure
ourExp.addProcedure('trial')
#add events (stimuli or keyboard checking etc...)
ourExp.procs['trial'].append( 
    EventPatch(name='fixation', image=None, 
        size=0.5, pos=[0,0],ori=0,
        onTimes=[(0,1), (1.5,2.0)],#on twice
        )
    )
ourExp.procs['trial'].append(
    EventPatch(name='face', image='face.jpg', 
        size=3.0, pos=[0,0], ori=45,
        onTimes=[(1.0,1.5)],#on just once
        )
    )
    
#insert the procedure into the flow (so that it gets used)    
ourExp.flow.addProcedure(
    ourExp.procs['trial'], pos=1)
#also add a trial handler (a loop, basically)
ourExp.flow.addLoop(
    LoopHandler(name='trials', loopType='simple', nReps=5),
        startPos=0.5, endPos=1.5,#specify positions relative to the
        )
    
for entry in ourExp.flow:
    print entry

