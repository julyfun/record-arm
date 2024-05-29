import rostopic
import message_filters
from sensor_msgs.msg import Image, JointState, CompressedImage, PointCloud2, CameraInfo, Imu
from tf2_msgs.msg import TFMessage
from control_msgs.msg import JointControllerState, JointTrajectoryControllerState
import rosbag
import rospy


def get_topic_and_type():
    all = rospy.get_published_topics()
    subs_name_type = []
    for topic in all:
        name = topic[0]
        type_str = topic[1].split('/')[-1]
        if type_str in ("JointControllerState", "JointState", "JointTrajectoryControllerState", "TFMessage", "CameraInfo", ""):
            subs_name_type.append((name, eval(type_str)))

    # this two trajectory is sometimes missing when running the arm (but rviz is ok, so I removed them)
    eliminates = ['/k4a/joint_states', '/tf_static', '/filtered', '/ra_trajectory_controller/state', '/rh_wr_trajectory_controller/state']
    # eliminates = ['/k4a/joint_states']
    subs_name_type = [x for x in subs_name_type if x[0] not in eliminates]
    # subs_name_type.append(('/k4a/depth_registered/points', PointCloud2))
    # subs_name_type.append(('/k4a/rgb/image_raw/compressed', CompressedImage))
    # subs_name_type.append(('/k4a/depth/image_rect/compressed', CompressedImage))
    subs_name_type.append(('/k4a/depth/image_raw/compressed', CompressedImage))
    subs_name_type.append(('/k4a/rgb_to_depth/image_raw/compressed', CompressedImage))

    # certainly not needed
    # subs_name_type.append(('/k4a/imu', Imu))
    return subs_name_type
