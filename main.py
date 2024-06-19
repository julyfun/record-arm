import rostopic
import rospy
from collections import defaultdict
from threading import Lock
import message_filters
from sensor_msgs.msg import Image, JointState, CompressedImage, PointCloud2
from tf2_msgs.msg import TFMessage
from control_msgs.msg import JointControllerState, JointTrajectoryControllerState
import rosbag

bag = rosbag.Bag('output.bag', 'w')
cnt = 0

from utils import get_topic_and_type
subs_name_type = get_topic_and_type()
sub_lists = [message_filters.Subscriber(name, that_type) for name, that_type in subs_name_type]

RECORD_NUM = 750

def callback(*li):
    global cnt
    try:
        cnt += 1
        print(cnt)
        for idx, content in enumerate(li):
            topic_name = subs_name_type[idx][0]
            if topic_name == '/sts/tf':
                bag.write('/tf', content)
            else:
                bag.write(topic_name, content)
        if cnt >= RECORD_NUM:
            bag.close()
            exit()
    except rospy.ROSInterruptException:
        pass

# Add a subscriber for the TFMessage topic
# def callback_tf(tf_message):
#     try:
#         global cnt
#         with lock:  # Acquire the lock before writing to the bag
#             bag.write('/tf', tf_message)
#             if cnt >= RECORD_NUM:
#                 exit()
#     except rospy.ROSInterruptException:
#         pass

if __name__ == '__main__':
    rospy.on_shutdown(bag.close)
    rospy.init_node('sync_listener', anonymous=True)

    # tf_sub = rospy.Subscriber('/tf', TFMessage, callback_tf)
    
    ts = message_filters.ApproximateTimeSynchronizer(sub_lists, 1, 1, allow_headerless=True)
    ts.registerCallback(callback)
    print("ok")
    rospy.spin()
