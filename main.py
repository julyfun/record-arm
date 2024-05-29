import rostopic
import rospy
from collections import defaultdict
from threading import Lock
import message_filters
from sensor_msgs.msg import Image, JointState, CompressedImage, PointCloud2
from control_msgs.msg import JointControllerState, JointTrajectoryControllerState
import rosbag

bag = rosbag.Bag('output.bag', 'w')
cnt = 0

from utils import get_topic_and_type
subs_name_type = get_topic_and_type()
sub_lists = [message_filters.Subscriber(name, that_type) for name, that_type in subs_name_type]

def callback(*li):
    try:
        global cnt
        cnt += 1
        print(cnt)
        for idx, content in enumerate(li):
            # print(subs_name_type[idx][0], content.header.stamp.to_sec())
            bag.write(subs_name_type[idx][0], content)
        if cnt >= 300:
            bag.close()
            exit()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    rospy.on_shutdown(bag.close)
    rospy.init_node('sync_listener', anonymous=True)

    # joints_sub = message_filters.Subscriber('joint_0s/joint_states', JointState)
    # ts = message_filters.ApproximateTimeSynchronizer([joints_sub2, joints_sub], queue_size=10, slop=0.2)

    ts = message_filters.ApproximateTimeSynchronizer(sub_lists, queue_size=1, slop=0.2, allow_headerless=True)
    ts.registerCallback(callback)
    print("ok")
    rospy.spin()
