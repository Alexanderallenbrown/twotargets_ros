#!/usr/bin/env python

import roslib; roslib.load_manifest('fishgantry_ros')
import rospy
from std_msgs.msg import * #import all of the standard message types
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped,Pose
from numpy import *
import time
import serial
import tf
from hunting_fishbrain.hunting_fishbrain.TwoTargets import TwoTargets
from hunting_fishbrain.hunting_fishbrain.HybridFishBrain import FishState


#this node subscribes to a float and a string. The float represents the input to a first order system. The string represents a state.

class TargetsNode():
  def __init__(self):
    self.timenow = rospy.Time.now()#inser case you need this
    self.listener = tf.TransformListener()
    #set up your publishers with appropriate topic types

    self.conditionpub = rospy.Publisher("/fishtarget_ros/experimental_condition",String,queue_size=1)
    self.statepub = rospy.Publisher("/fishtarget_ros/target_is_out",String,queue_size=1)
    self.targetposepub = rospy.Publisher("/fishtarget_ros/targetpose",PoseStamped,queue_size=1)
    self.targetMarkerpub = rospy.Publisher("/fishtarget_ros/target_marker",Marker,queue_size=1)
    self.remainingpub = rospy.Publisher("/fishtarget_ros/time_remaining",String,queue_size=1)

    self.xoffset,self.yoffset,self.zoffset = 0,0,0#-.2,-.05,0

    self.port = rospy.get_param('~port','/dev/ttyARDUINOTARGETS')
    self.baud = rospy.get_param('~baud',115200)
    self.ser = serial.Serial(self.port, self.baud,timeout=1) #this initializes the serial object

    #set up your subscribers
    self.robotshot = False
    self.exprunning = False
    self.sub1 = rospy.Subscriber("/fishgantry/robotshot",Bool,self.sub1Callback)
    self.squirtpose_sub = rospy.Subscriber("/fishgantry/squirtpose",PoseStamped,self.squirtCallback)
    self.sub2 = rospy.Subscriber("/fishgantry/exprunning",Bool,self.sub2Callback)

    #initialize any variables that the class "owns. these will be available in any function in the class.
    #(self,ITI_mean,ITI_random,Trial_mean,Trial_random,tleftPose,trightPose)
    ITI_mean,ITI_random,Trial_mean,Trial_random = 300,15,25,1
    rTarg = FishState(.3,.15,.25,0,0) #the target has no inherent pitch or yaw requirement
    lTarg = FishState(0,.15,.25,0,0) 
    self.targets = TwoTargets(ITI_mean,ITI_random,Trial_mean,Trial_random,lTarg,rTarg)

    self.dt = 0.1
    #set up timed loop to run like an arduino's "void loop" at a particular rate (100Hz)
    rospy.Timer(rospy.Duration(self.dt),self.loop,oneshot=False) 

    # now some stuff for the arduino
    self.outPosition = 90
    self.inPosition = 0

    #transform broadcaster
    self.br = tf.TransformBroadcaster()



  def squirtCallback(self,data):
    #self.robotshot = bool(data.pose.orientation.z)
    #rospy.logwarn("ROBOT SHOT FROM TARGET: "+str(self.robotshot))
    pass

  def sub1Callback(self,data):
    #the actual string is called by data.data. update the appropriate class-owned variable.
    self.robotshot = data.data
    #print(data.data)
    #pass

  def sub2Callback(self,data):
    self.exprunning = data.data


  def loop(self,event):
    #this function runs over and over again at dt.
    #do stuff based on states. 
    #rospy.logwarn("!"+str(self.outPosition)+","+str(self.inPosition)+","+str(int(self.robotshot))+","+str(0))

    #update the target controller
    if self.exprunning:
        lhunt, lpose, lstate, lblock,remaining = self.targets.update(self.robotshot)
        trialtypemsg = String()
        trialtypemsg.data = self.targets.trialType
        tstatemsg = String()
        tstatemsg.data = self.targets.state
        remainingmsg = String()
        remainingmsg.data = str(remaining)


        self.conditionpub.publish(trialtypemsg)
        self.statepub.publish(tstatemsg)
        self.remainingpub.publish(remainingmsg)
        rospy.logwarn("ROBOT SHOT: "+str(self.robotshot))
        if ((self.targets.trialType == 'EL') or (self.targets.trialType == 'CL')):
            if( (self.targets.state == 'target' )):
                self.ser.write("!"+str(self.outPosition)+","+str(self.inPosition)+","+str(int(self.robotshot))+","+str(0)+"\r\n")
            
                rospy.logwarn("!"+str(self.outPosition)+","+str(self.inPosition)+","+str(int(self.robotshot))+","+str(0))
            else:
                self.ser.write("!"+str(self.inPosition)+","+str(self.inPosition)+","+str(int(self.robotshot))+","+str(0)+"\r\n")
        elif ((self.targets.trialType == 'ER') or (self.targets.trialType == 'CR')):
            if( (self.targets.state == 'target' )):
                self.ser.write("!"+str(self.inPosition)+","+str(self.outPosition)+","+str(0)+","+str(int(self.robotshot))+"\r\n")
                rospy.logwarn("!"+str(self.inPosition)+","+str(self.outPosition)+","+str(0)+","+str(int(self.robotshot)))
            else:
                self.ser.write("!"+str(self.inPosition)+","+str(self.inPosition)+","+str(0)+","+str(int(self.robotshot))+"\r\n")
        
        timenow = rospy.Time.now()

        # now set up output messages
        self.br.sendTransform((self.xoffset,self.yoffset,self.zoffset),tf.transformations.quaternion_from_euler(0,0,0),timenow,'/target_coord_system','/robot_static_cmd')


        targetmarker = Marker()
        targetmarker.header.frame_id='/target_coord_system'
        targetmarker.header.stamp = timenow
        targetmarker.type = targetmarker.SPHERE
        # targetmarker.mesh_resource = 'package://fishgantry_ros/meshes/static.dae'
        # targetmarker.mesh_use_embedded_materials = True
        targetmarker.action = targetmarker.MODIFY
        targetmarker.scale.x = .05
        targetmarker.scale.y = .05
        targetmarker.scale.z = .05
        targetmarker.color.a=1.0
        if self.targets.state == "target":
            if self.targets.trialType[0]=='E':
                targetmarker.color.r=0
                targetmarker.color.g=1.0
                targetmarker.color.b=0
            else:
                targetmarker.color.r=0
                targetmarker.color.g=0
                targetmarker.color.b=1.0
        else:
            targetmarker.color.r=1.0
            targetmarker.color.g=0
            targetmarker.color.b=0
        tempquat = tf.transformations.quaternion_from_euler(0,0,0)#this is RELATIVE TO FISH ORIENTATION IN TF (does the mesh have a rotation?)
        targetmarker.pose.orientation.w = tempquat[3]
        targetmarker.pose.orientation.x = tempquat[0]
        targetmarker.pose.orientation.y = tempquat[1]
        targetmarker.pose.orientation.z = tempquat[2]
        targetmarker.pose.position.x = self.targets.pose.x
        targetmarker.pose.position.y = self.targets.pose.y
        targetmarker.pose.position.z = self.targets.pose.z
        self.targetMarkerpub.publish(targetmarker)

        #now send the pose of the target to the robot brain

        tpose = PoseStamped()
        tpose.header.stamp = timenow
        tpose.pose.position.x = self.targets.pose.x
        tpose.pose.position.y = self.targets.pose.y
        tpose.pose.position.z = self.targets.pose.z
        self.targetposepub.publish(tpose)
        #rospy.logwarn("hello from target node")






    
      
#main function
def main(args):
  rospy.init_node('targets_node', anonymous=True)
  my_node = TargetsNode()
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv) 