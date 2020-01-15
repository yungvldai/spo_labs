#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

dirs = {
    'e': 0,
    'ne': 0,
    'n': 0,
    'nw': 0,
    'w': 0,
}
state = 0

def set_state(new_state):
    global state 
    if state != new_state:
        state = new_state

def do():
	global dirs
	linear_x = angular_z = 0
	if dirs['n'] > 0.9 and dirs['nw'] > 0.4 and dirs['ne'] > 0.4:
		set_state(0)
	elif dirs['e'] > dirs['w']:
		set_state(2)
	else:
		set_state(1)

def turn(side):
	msg = Twist()
	msg.linear.x = 0
	msg.angular.z = 0.8 if side == 'left' else -0.8
	return msg
		
def go_along():    
    msg = Twist()
    msg.angular.z = 0
    msg.linear.x = 1
    return msg

def laser_callback(msg):
	global dirs
	dirs = {
		'e': min(min(msg.ranges[50:100]), 1),
		'ne': min(min(msg.ranges[101:287]), 1),
		'n': min(min(msg.ranges[288:431]), 1),
		'nw': min(min(msg.ranges[432:611]), 1),
		'w': min(min(msg.ranges[612:679]), 1),
    }
	do()

rospy.init_node('Maze')
vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/base_scan', LaserScan, laser_callback)

while not rospy.is_shutdown():
	msg = Twist()
	if state == 2:
		msg = turn('right')
	if state == 1:
		msg = turn('left')
	if state == 0:
		msg = go_along()
	vel.publish(msg)

	


