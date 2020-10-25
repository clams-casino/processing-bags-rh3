import rosbag
import os
from tqdm import tqdm

import cv2 as cv
from cv_bridge import CvBridge
bridge = CvBridge()

# # For docker container, assume bags always mounted to this directory in the docker container
# # And we will write the output bag to the same folder
# bag_dir = '/bags/'

# # Assume that we pass the bag name into the docker image with an environment variable
# in_bag_name = os.environ['BAG_NAME']
# in_bag_path = bag_dir + bag_name

# TODO For testing remove later
in_bag_path = '/home/mike/duckietown/RH4/bags/cam_april.bag'

out_bag_path = in_bag_path[:in_bag_path.find('.')] + '_processed' + in_bag_path[in_bag_path.find('.'):]

in_bag = rosbag.Bag(in_bag_path)
out_bag = rosbag.Bag(out_bag_path, 'w')


# Parameters for drawing text
TEXT_POSITION = (50,50)
TEXT_FONT = cv.FONT_HERSHEY_SIMPLEX
TEXT_FONTSCALE = 1
TEXT_COLOR = (0,0,0)
TEXT_THICKNESS = 2

print('Processing bag file: {}', in_bag_path)
for topic, msg, t in tqdm(in_bag.read_messages(), desc='processing bag images', total=in_bag.get_message_count()):
    if 'image' in topic:
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        timestamp = msg.header.stamp.to_sec()

        cv.putText(cv_img, 'Time: '+str(timestamp), 
                    TEXT_POSITION, TEXT_FONT, TEXT_FONTSCALE, TEXT_COLOR, TEXT_THICKNESS)

        # TODO For testing remove later
        # cv.imshow('image', cv_img)
        # cv.waitKey(2)

        img_msg = bridge.cv2_to_imgmsg(cv_img, encoding="passthrough")
        out_bag.write(topic, img_msg)

in_bag.close()
out_bag.close()
print('Wrote processed bag file to: {}', out_bag_path)