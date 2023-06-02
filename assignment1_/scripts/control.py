#!/usr/bin/env python



"""

Module: assignment_2_2022
Platform: Unix
Synopsis: This is a ROS node designed to control a robot. It subscribes to the "/odom" topic to obtain information about the robot's position and velocity, and publishes this data to the "/vel_pos" topicments an action client to prompt the user to enter a target position or cancel the current goal and sends the goal to the action server and waits for a response.
Module author: GUELMAMI ABDELOUADOUD <wadoud.guelmami@gmail.com>

ROS node for controlling the robot. Subscribes to /odom and publishes to /posxy_velxy. Also implements an action client.

Subscribes to:
    /odom

Publishes to:
    /vel_pos

Clients:
    /reaching_goal

This module provides a ROS node for user input and controlling a robot.

It subscribes to the '/odom' topic to receive updates on the robot's position and velocity using the 'nav_msgs.msg.Odometry' message type.
It publishes the current state of the robot, including position and velocity, to the '/pos_vel' topic using the 'assignment_2_2022.msg.vel_pos' message type.
It interacts with the user to set a target position and control the robot's movement using the 'assignment_2_2022.msg.PlanningAction' action server.

    
"""

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import vel_pos
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
import actionlib
import actionlib.msg
import time
import math

 
def update_current_robot_state(msg):
	"""
	function for the publisher.

	it publisher the current cordination of x, y to and thier velocity to 

	Args:
        msg: The 'nav_msgs.msg.Odometry' message containing the robot's current position and velocity.
	"""
	global current_state_publisher
	# extract the current position and velocity from the message
	position = msg.pose.pose.position
	velocity = msg.twist.twist.linear
	# create a custom message to store and publish the current state
	current_state = vel_pos()
	current_state.cor_x = position.x
	current_state.cor_y = position.y
	current_state.vel_x = velocity.x
	current_state.vel_y = velocity.y
	current_state_publisher.publish(current_state)

def main():
	"""
	Main function to control the robot based on user input.
	Sets up subscribers, publishers, and an action client for controlling the robot.
	Runs the action client.
	Prompts the user to enter a target position or cancel the current goal.
	Sends the goal to the action server and waits for a response.
	The program executes the action client, prompting the user to input a target position or cancel the ongoing goal.
	It then sends the goal to the action server and waits for a response.

	"""
	global current_state_publisher
	# create a publisher to send the current state of the robot
	current_state_publisher = rospy.Publisher("/pos_vel", vel_pos, queue_size = 1)
	# subscribe to the odometry topic to receive updates on the robot's position and velocity
	odom_subscriber = rospy.Subscriber("/odom", Odometry, update_current_robot_state)
	# create a client for the reaching_goal action server
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	rospy.loginfo('Waiting for server to start...')
	client.wait_for_server()
	while not rospy.is_shutdown():
		# get the desired x and y position from the user
		x_des = float(input("Please enter the desired X position: "))
		y_des = float(input("Please enter the desired Y position: "))
		rospy.loginfo("Target position is set!")
		goal = assignment_2_2022.msg.PlanningGoal()
		goal.target_pose.pose.position.x = x_des
		goal.target_pose.pose.position.y = y_des
		client.send_goal(goal)
		# check if the user wants to cancel the goal
		c_input = input("Please type 'cancel' to cancel the goal: ")
		if (c_input == "cancel"):
			print("Goal canceled!")
			client.cancel_goal()
		else:
			continue

if __name__ == '__main__':
	rospy.init_node('user_input')
	main()
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		rate.sleep()

