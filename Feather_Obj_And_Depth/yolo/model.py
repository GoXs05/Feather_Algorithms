from ultralytics import YOLO
from transformers import pipeline
import numpy as np
from utils import distance

def get_box_dimensions(box, x_size, y_size):
    
    x_center = int(box.xywh[0][0].item())
    y_center = int(box.xywh[0][1].item())
    width = int(box.xywh[0][2].item())
    height = int(box.xywh[0][3].item())

    if x_center > x_size: x_center = x_size - 1
    elif x_center < 0: x_center = 0

    if y_center > y_size: y_center = y_size - 1
    elif y_center < 0: y_center = 0

    xmin = x_center - int(width/2)
    xmax = x_center + int(width/2)
    ymin = y_center - int(height/2)
    ymax = y_center + int(height/2)

    if xmin < 0: xmin = 0
    if xmax > x_size: xmax = x_size - 1
    if ymin < 0: ymin = 0
    if ymax > y_size: ymax = y_size - 1

    return xmin, xmax, ymin, ymax, x_center, y_center



def detect_objects(yolo_model, img, depth_map_scaled, show_obj_det):
    item_names = yolo_model.names
    results = yolo_model(source=img, show=show_obj_det, conf=0.4, save=False)

    x_size = results[0].orig_shape[0]
    y_size = results[0].orig_shape[1]
    for r in results:
        num_boxes = r.boxes.xywh.size(dim=0)

        if num_boxes != 0:
            print(f"Number of Recognized objects: {num_boxes}")

            for i in range(num_boxes):
                xmin, xmax, ymin, ymax, x_center, y_center = get_box_dimensions(r.boxes[i], x_size, y_size)

                abs_dist = distance.calculate_distance(depth_map_scaled, xmin, xmax, ymin, ymax)

                if (item_names[int(r.boxes[i].cls.item())] == "person"):
                    print(f"Center of {item_names[int(r.boxes[i].cls.item())]}: {x_center}, {y_center}")
                    print(f"Distance of {item_names[int(r.boxes[i].cls.item())]}: {abs_dist}")