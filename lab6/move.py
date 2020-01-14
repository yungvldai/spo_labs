#!/usr/bin/env python

import rospy
import math
import time
from std_srvs.srv import Empty
from turtlesim.msg import Color
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x = y = yaw0 = 0
speed = 5
BG_COL = [0, 0, 0]
PEN_COL = [255, 255, 255]

def set_bg(color):
	rospy.wait_for_service('clear')
	fill_bg = rospy.ServiceProxy('clear', Empty)
	rospy.set_param('/background_b', color[0])
	rospy.set_param('/background_r', color[1])
	rospy.set_param('/background_g', color[2])
	fill_bg()

def teleport(x, y, angle):
	rospy.wait_for_service('turtle1/teleport_absolute')
	turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
	pen_color(BG_COL, 1)
	turtle1_teleport(x, y, angle)
	pen_color(PEN_COL, 0)

def pen_color(color, off, width = 2):
    rospy.wait_for_service('turtle1/set_pen')
    set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    set_pen(color[0], color[1], color[2], width, off)

def turn(angle, clockwise):
    global yaw
    yaw0 = yaw
    vel_msg = Twist()
    ang_speed = 90 * 2 * math.pi / 360
    rel_ang = angle * 2 * math.pi / 360
    vel_msg.angular.z = -abs(ang_speed) if clockwise else abs(ang_speed)
    angle_moved = 0
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while angle_moved < rel_ang:
        velocity_publisher.publish(vel_msg)
        angle_moved = abs(yaw - yaw0)
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

def move(distance, is_forward):
    velocity_message = Twist()
    global x, y, speed
    x0 = x
    y0 = y
    velocity_message.linear.x = abs(speed) if is_forward else -abs(speed)
    distance_moved = 0.0
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while distance_moved < distance:
        velocity_publisher.publish(velocity_message)
        distance_moved = abs(0.4 * math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2))) 
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

def callback(pose_message):
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def next_sym():
    pen_color(BG_COL, 1)
    move(0.2, 1)
    turn(90, False)
    move(1, 1)
    turn(90, True)
    pen_color(PEN_COL, 0)

nums = [
    'gcggcgcggcgcgga',
    'cgga',
    'gcgcgagag',
    'gcgcgccgcgcgccg',
    'cgagagccgga',
    'gccgagagcgcgccg',
    'gcggcgcgcg',
    'gcgga',
    'gcggcgcggccgagcga',
    'gcgcgcgcgcggcgccg'
]

def print_sym(num):
    for cmd in nums[num]:
        if cmd == 'g':
            move(0.5, 1)
        if cmd == 'a':
            turn(90, False)
        if cmd == 'c':
            turn(90, True)
	
rospy.init_node('Turtlesim_number', anonymous=False, disable_signals=True)
pose_subscriber = rospy.Subscriber('turtle1/pose', Pose, callback)
time.sleep(1)  
set_bg(BG_COL)
teleport(0.2, 7, 0)
pen_color(PEN_COL, 0)
print_sym(2)
next_sym()
print_sym(4)
next_sym()
print_sym(3)
next_sym()
print_sym(9)
next_sym()
print_sym(3)
next_sym()
print_sym(5)
next_sym()

