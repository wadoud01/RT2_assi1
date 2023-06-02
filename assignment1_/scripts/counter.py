#! /usr/bin/env python

"""
.. module:: assignment_2_2022

   :platform: Unix
   
   :synopsis: ROS service code to count goals reached and canceled.

.. moduleauthor:: GUELMAMI ABDELOUADOUD

This module contains a ROS node for goal counting.
It subscribes to the '/reaching_goal/result_callback' topic to receive result messages from the 'assignment_2_2022.msg.PlanningActionResult' type.
It also provides a service named 'counter' of type 'count' to retrieve the number of canceled and reached goals.

The node keeps track of the number of canceled and reached goals and provides logging messages to indicate the counts.

"""

import rospy
from assignment_2_2022.srv import count
import actionlib
import actionlib.msg
import assignment_2_2022.msg

cancelled_goals = 0 #intilaize which represents Canceled goals 
reached_goals = 0 #initilize which represnets Reached goals

def result_callback(msg):
	"""
	This class provides a ROS service to get the number of goals reached and cancelled.
	
	Args:
	msg (Pose):
	the turtlesim Pose

	Attributes:
        cancelled_goals (int): The number of goals that have been cancelled.
        reached_goals (int): The number of goals have been reached.
        srv (rospy.Service): The ROS service that will provide the data.
        sub_result (rospy.Subscriber): The ROS subscriber for the result topic.
	"""
	global cancelled_goals, reached_goals
	state = msg.status.status
	if state == 2:
		cancelled_goals += 1
		rospy.loginfo("Number of goal canceled is {:.1f}".format(cancelled_goals))
	elif state == 3:
		reached_goals += 1
		rospy.loginfo("Number of goal reached is {:.1f}".format(reached_goals))

def info_callback(req):
	
	"""
	Callback function for the 'counter' service.

	Returns the current count of canceled and reached goals.

	Args:
	req: The request message.

	Returns:
	An instance of 'goal_srvResponse' containing the current count of canceled and reached goals.
	"""
       
	global cancelled_goals, reached_goals
	rospy.loginfo("Number of goal canceled is {:.1f} and Number of goal reached is {:.1f}".format(cancelled_goals, reached_goals))
	return goal_srvResponse()

if __name__ == "__main__":
	"""
	the main function that inzialise and create nodes.
	"""
	rospy.init_node('counter') #intializing the node counter 
	sub_result = rospy.Subscriber('/reaching_goal/result_callback', assignment_2_2022.msg.PlanningActionResult, result_callback) #subscribing to the result topic
	srv = rospy.Service('counter', count, info_callback)
	rospy.spin() #spin to handle callbacks


