import rostopic
import rospy
import message_filters
from sensor_msgs.msg import Image, JointState, CompressedImage
from control_msgs.msg import JointControllerState, JointTrajectoryControllerState
import rosbag

bag = rosbag.Bag('output.bag', 'w')
cnt = 1

all = rospy.get_published_topics()
subs_name_type = []
for topic in all:
    name = topic[0]
    type_str = topic[1].split('/')[-1]
    if type_str in ("JointControllerState", "JointState", "JointTrajectoryControllerState"):
        subs_name_type.append((name, eval(type_str)))

# this is a weird topic with no data
eliminates = ['/k4a/joint_states']
subs_name_type = [x for x in subs_name_type if x[0] not in eliminates]
subs_name_type = [('/k4a/rgb/image_raw/compressed', CompressedImage)] + subs_name_type
sub_lists = [message_filters.Subscriber(name, that_type) for name, that_type in subs_name_type]

def callback(*li):
    try:
        global cnt
        cnt += 1
        print(cnt)
        for idx, content in enumerate(li):
            print(subs_name_type[idx][0], content.header.stamp.to_sec())
            bag.write(subs_name_type[idx][0], content)
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    rospy.on_shutdown(bag.close)
    rospy.init_node('sync_listener', anonymous=True)

    # joints_sub = message_filters.Subscriber('joint_0s/joint_states', JointState)
    # ts = message_filters.ApproximateTimeSynchronizer([joints_sub2, joints_sub], queue_size=10, slop=0.2)

    ts = message_filters.ApproximateTimeSynchronizer(sub_lists, queue_size=10, slop=0.1)
    ts.registerCallback(callback)
    print("ok")
    rospy.spin()
