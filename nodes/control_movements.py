#!/usr/bin/env python
import sys, getopt     # for getting and parsing command line arguments
import time
import math
import threading
import rospy
import smach
import smach_ros

#from std_msgs.msg import Float64, Float64MultiArray, MultiArrayDimension, Bool, Int32

import numpy as np

class ReadyState(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["done", "exit"])
    def execute(self, userdata):
        print "***************"
        print "Executing ReadyState."
        print "***************"
        if rospy.is_shutdown():
            return "exit"
        else:
            return "done"

class FaceRec(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["done", "exit"])

    def execute(self, userdata):
        print "***************"
        print "Executing FaceRec."
        print "***************"
		#runs the program to recognize the face.
		#note: need to store name in a global variable

        if rospy.is_shutdown():
            return "exit"
        else:
            return "done"

class HandShake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["done", "exit"])

    def execute(self, userdata):
        print "***************"
        print "Executing HandShake."
        print "***************"
		#execute handshake program

        if rospy.is_shutdown():
            return "exit"
        else:
            return "done"

class Greet:
	#Scan, Center, FaceRec, HandShake, HumanMovesAway
    def __init__(self):
        self = self;

    def createFSM(self):
        # define the states
        toReadyState = ReadyState()
       	toFaceRec = FaceRec()
       	toHandShake = HandShake()

        # wire the states into a FSM
        self.fsm = smach.StateMachine(outcomes=['exit'])
        with self.fsm:
            smach.StateMachine.add("GoToReady", toReadyState, 
                transitions={'done':'FaceRec',
                             'exit':'exit'})
            smach.StateMachine.add("FaceRec", toFaceRec, 
                transitions={'done':'HandShake',
                             'exit':'exit'})
            smach.StateMachine.add("HandShake", toHandShake, 
                transitions={'done':'FaceRec',
                             'exit':'exit'})
    def run(self):
        self.createFSM()

        # Create and start the introspection server
        sis = smach_ros.IntrospectionServer('server_name', self.fsm, '/SM_ROOT')
        sis.start()

        index = raw_input("Start demo? Y/n\n")
        if index == "N" or index == "n":
            return

        outcome = self.fsm.execute()

        rospy.spin()  # just to prevent this node from exiting
        sis.stop()


# Main method
if __name__ == "__main__":
    rospy.init_node('Greet', anonymous=True)
    demo = Greet()
    demo.run()