import rospy
from collections import defaultdict
from threading import Lock

class TopicMessageCounter:
    def __init__(self, topic_names):
        self.topic_names = topic_names
        self.message_counts = defaultdict(int)
        for topic_name in self.topic_names:
            self.message_counts[topic_name] = 0
        self.lock = Lock()

        # Set up ROS subscribers for the given topic names
        self.subscribers = []
        for topic_name in self.topic_names:
            sub = rospy.Subscriber(topic_name, rospy.AnyMsg, self.message_callback)
            self.subscribers.append(sub)

        # Set up a ROS timer to count messages every 1 second
        self.timer = rospy.Timer(rospy.Duration(1.0), self.count_messages)

    def message_callback(self, msg):
        with self.lock:
            for topic_name in self.topic_names:
                if msg._connection_header['topic'] == topic_name:
                    self.message_counts[topic_name] += 1

    def count_messages(self, event):
        with self.lock:
            print("Message counts in the last 1 second:")
            for topic_name, count in self.message_counts.items():
                print(f"\t{topic_name}: {count}")
            for topic_name in self.topic_names:
                self.message_counts[topic_name] = 0

if __name__ == '__main__':
    rospy.init_node('topic_message_counter')

    # Define the list of topic names to monitor
    from utils import get_topic_and_type
    topics = get_topic_and_type()
    topic_names = [name for name, _ in topics]

    counter = TopicMessageCounter(topic_names)
    rospy.spin()