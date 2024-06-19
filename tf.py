#!/usr/bin/env python

import rospy
from tf2_msgs.msg import TFMessage

def tf_callback(msg):
    # Calculate the length of the message
    message_length = len(msg.transforms)
    
    # Print the length of the message
    rospy.loginfo(f"Length of current /tf message: {message_length}")
    
    # Check if the message length is more than 10
    if message_length > 10:
        # Publish to /fixed_tf
        fixed_tf_pub.publish(msg)
        rospy.loginfo("Published to /fixed_tf")

def tf_listener():
    # Initialize the ROS node
    rospy.init_node('tf_listener', anonymous=True)
    
    # Create a subscriber to the /tf topic
    rospy.Subscriber('/tf', TFMessage, tf_callback)
    
    # Create a publisher for the /fixed_tf topic
    global fixed_tf_pub
    fixed_tf_pub = rospy.Publisher('/sts/tf', TFMessage, queue_size=10)
    
    # Keep the node running
    rospy.spin()

if __name__ == '__main__':
    try:
        tf_listener()
    except rospy.ROSInterruptException:
        pass
