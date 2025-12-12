#!/usr/bin/env python3
"""Make robot stand"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

rclpy.init()
node = Node('stand_cmd')
pub = node.create_publisher(Float64MultiArray, '/position_controller/commands', 10)
time.sleep(2)

msg = Float64MultiArray()
# 23 joints: set all to 0 (straight standing pose)
msg.data = [0.0] * 23

print("Sending STAND command (all joints to 0)...")
for _ in range(10):
    pub.publish(msg)
    time.sleep(0.1)

print("Done! Robot should be standing straight.")
rclpy.shutdown()

