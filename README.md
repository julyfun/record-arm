Please first check if all machines are synchronized. Restart ntp on nuc if not.

## Record

```
# on nuc
jst.run1
jst.run2
# local
roslaunch easy_handeye ur10_cali.launch
roslaunch easy_handeye ur10_pub.launch
# in this repo
python3 tf.py
python3 main.py
```

## Replay

```
# on nuc
roscore
# local
roslaunch easy_handeye ur10_pub.launch
# in this repo
python3 param_replayer.py
rosbag play tf_static_camera.bag -l -r 1
rosbag play output.bag -l -r 1
rviz
```
