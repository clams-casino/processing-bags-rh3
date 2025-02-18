import rosbag
import os
from tqdm import tqdm

import cv2 as cv
from cv_bridge import CvBridge
bridge = CvBridge()

# Assume bags always mounted to this directory in the docker container
# And we will write the output bag to the same directory
bag_dir = '/bags/'

# Assume that we pass the bag name into the docker image with an environment variable
in_bag_name = os.environ['BAG_NAME']
in_bag_path = bag_dir + in_bag_name

out_bag_path = in_bag_path[:in_bag_path.find('.')] + '_processed' + in_bag_path[in_bag_path.find('.'):]

in_bag = rosbag.Bag(in_bag_path)
out_bag = rosbag.Bag(out_bag_path, 'w')

# Parameters for drawing text
TEXT_POSITION = (50,50)
TEXT_FONT = cv.FONT_HERSHEY_SIMPLEX
TEXT_FONTSCALE = 1
TEXT_COLOR = (0,0,0)
TEXT_THICKNESS = 2

print('Processing bag file: {}'.format(in_bag_path))
for topic, msg, t in tqdm(in_bag.read_messages(), desc='processing bag images', total=in_bag.get_message_count()):
    if msg._type == "sensor_msgs/Image":
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        cv.putText(cv_img, 'Time: '+str(msg.header.stamp.to_sec()), 
                    TEXT_POSITION, TEXT_FONT, TEXT_FONTSCALE, TEXT_COLOR, TEXT_THICKNESS)

        img_msg = bridge.cv2_to_imgmsg(cv_img, encoding="passthrough")
        
    elif msg._type == "sensor_msgs/CompressedImage":
        cv_img = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding='passthrough')

        cv.putText(cv_img, 'Time: '+str(msg.header.stamp.to_sec()), 
                    TEXT_POSITION, TEXT_FONT, TEXT_FONTSCALE, TEXT_COLOR, TEXT_THICKNESS)

        img_msg = bridge.cv2_to_compressed_imgmsg(cv_img, dst_format='jpeg')

    else:
        continue

    out_bag.write(topic, img_msg, t)

in_bag.close()
out_bag.close()
print('Wrote processed bag file to: {}'.format(out_bag_path))