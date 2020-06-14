import glob
import os

import argparse

from utils import visualization_utils as vis_util
from utils import cacli_models as models

working_dir = os.getcwd()
print(working_dir) #gets path to wd

test_image_paths = glob.glob(os.path.join(working_dir + "/model/images", "*.jpg")) 
model_path = working_dir + "/model/model.tflite"
model_anchor_path = working_dir + "/model/anchors.json"
model_label_path = working_dir + "/model/labels.json"

model_interpreter = models.initiate_tflite_model(model_path)
anchor_points = models.json_to_numpy(model_anchor_path)
label_list = models.json_to_numpy(model_label_path)

category_index = { i : {"name" : label_list[i]} for i in list(range(len(label_list))) }
print(category_index)
print(test_image_paths)
count = 0
for image in test_image_paths:
    count += 1
    models.detect_objects(model_interpreter,image,category_index,anchor_points,0.10,SAVE_DIR="output/")
    
