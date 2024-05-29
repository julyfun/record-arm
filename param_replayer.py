import rospy
import json
import os

def replay_params(file_path):
    # Initialize the node
    rospy.init_node('param_replayer', anonymous=True)
    
    # Load the parameters from the JSON file
    with open(file_path, 'r') as file:
        param_dict = json.load(file)
    
    # Set the parameters on the parameter server
    for param, value in param_dict.items():
        rospy.set_param(param, value)
    
    rospy.loginfo("Parameters replayed from %s", file_path)

if __name__ == '__main__':
    try:
        # Specify the file path
        file_path = os.path.join("ros_params.json")
        replay_params(file_path)
    except rospy.ROSInterruptException:
        pass