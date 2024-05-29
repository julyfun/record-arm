import rospy
import json
import os

def record_params(file_path):
    # Initialize the node
    rospy.init_node('param_recorder', anonymous=True)
    
    # Get all parameters on the parameter server
    params = rospy.get_param_names()
    
    # Dictionary to store parameters
    param_dict = {}
    
    for param in params:
        param_dict[param] = rospy.get_param(param)
    
    # Save the parameters to a JSON file
    with open(file_path, 'w') as file:
        json.dump(param_dict, file, indent=4)
    
    rospy.loginfo("Parameters recorded to %s", file_path)

if __name__ == '__main__':
    try:
        # Specify the file path
        file_path = os.path.join("ros_params.json")
        record_params(file_path)
    except rospy.ROSInterruptException:
        pass