import argparse
import torch
from Midas import model as depth_model

from ultralytics import YOLO
from yolo import model as obj_det_model

import cv2

def parse_args():
    supported_depth_models = ["DPT_Large", "DPT_Hybrid", "MiDaS_small"]
    supported_obj_det_models = ['rsc/yolov8x.pt', 'rsc/yolov8n.pt']

    parser = argparse.ArgumentParser(description='Select a depth model')
    parser.add_argument('--depth_model', default="MiDaS_small", choices=supported_depth_models, help='select a depth perception model')
    parser.add_argument('-show_depth', default=False, action='store_const', const=True, help='show depth map or not?')
    parser.add_argument('--obj_model', default='rsc/yolov8x.pt', choices=supported_obj_det_models, help='select an object detection model')
    parser.add_argument('-show_obj_det', default=False, action='store_const', const=True, help='show object detection or not?')
    parser.add_argument('-image', default=False, action='store_const', const=True, help='use preloaded image or not?')

    args = parser.parse_args()
    return args


def run_program(in_loop):
    if (in_loop):
        success, img = cap.read()
    else:
        img = cv2.imread("rsc/droneFlightTest.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    

    # Apply input transforms
    input_batch = transform(img).to(device)

    #depth perception
    depth_map_scaled = depth_model.perceive_depth(midas, input_batch, img, show_depth_map)

    #object detection
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #reset image color
    obj_det_model.detect_objects(yolo_model, img, depth_map_scaled, show_obj_det)


if  __name__ == '__main__':
    args = parse_args()

    depth_model_type = args.depth_model
    show_depth_map = args.show_depth
    obj_det_model_path = args.obj_model
    show_obj_det = args.show_obj_det
    use_image = args.image

    midas = torch.hub.load("intel-isl/MiDaS", depth_model_type)

    # Move model to GPU if available
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()

    # Load transforms to resize and normalize the image
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

    if depth_model_type == "DPT_Large" or depth_model_type == "DPT_Hybrid":
        transform = midas_transforms.dpt_transform
    else:
        transform = midas_transforms.small_transform

    
    yolo_model = YOLO(obj_det_model_path)

    # Initialize the camera
    cap = cv2.VideoCapture(0) # '0' is usually the default camera

    try:

        if (not use_image):
            while cap.isOpened():
                run_program(in_loop=True)

                # Break the loop with the 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()

        else:
            run_program(in_loop=False)
        
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
