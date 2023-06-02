#! /usr/bin/env python

"""
.. module:: exercise2
    :platform: Unix
    :synopsis: Python module for controlling the robot.
.. moduleauthor:: GUELMAMI ABDELOUADOUD

ROS node to control our robot.

Subscribes to:
    /pos_vel

Parameters:
    frequency_param (float): the frequency in Hz.
    des_pos_x (float): represents the desired x position.
    des_pos_y (float): represents the desired y position.

This module provides a ROS node for printing robot information based on a given frequency.

It subscribes to the '/pos_vel' topic to receive updates on the robot's position and velocity using the 'assignment_2_2022.msg.vel_pos' message type.
It retrieves the target position and calculates the distance to the target and the average speed of the robot.
It prints the robot information at a specified frequency.
"""

import rospy
import math
import time
from assignment_2_2022.msg import vel_pos


# last time the robot's information was printed
previous_print_time = 0


def print_robot_info(msg):

	"""
	A function to print the distance and average.
        
	 Args:
        msg: The 'assignment_2_2022.msg.vel_pos' message containing the robot's current position and velocity.
	"""

	global frequency_param, previous_print_time
	# calculate the time period for the messages to be printed
	time_period = (1.0/frequency_param) * 1000 
	# get the current time in milliseconds
	current_time = time.time() * 1000 

	# check if the time since the last printed message is greater than the time period
	if current_time - previous_print_time > time_period:
		# retrieve the target position
		target_x = rospy.get_param("des_pos_x")
		target_y = rospy.get_param("des_pos_y")
		current_x = msg.cor_x
		current_y = msg.cor_y
		#calculate the distance to the target position
		distance = math.dist([target_x, target_y], [current_x, current_y])
		#calculate the average speed
		average_speed = math.sqrt(msg.vel_x**2 + msg.vel_y**2)
		#print the robot information
		print(' \n We are {:.3f}m far from our final postion'.format(float(distance)))
		print(' \n The average speed is {:.3f} m\s'.format(float(average_speed)))
		# update the last printed message time
		previous_print_time = current_time

if __name__ == "__main__":
	"""
	Main method for initializing the node and subscribing.
	"""

	global frequency_param
	frequency_param = 1.0
	#initialize the ros node
	rospy.init_node('rob_info')
	#retrieve the frequency parameter
	frequency_param = rospy.get_param("frequency")
	#subscribing to the /pos_vel topic
	pos_vel_subscriber = rospy.Subscriber("/pos_vel", vel_pos, print_robot_info)
	#spin to handle callbacks
	rospy.spin()
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		rate.sleep()


