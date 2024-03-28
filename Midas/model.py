import cv2
import numpy as np
import torch

def perceive_depth(midas, input_batch, img, show_depth_map):
    # Prediction and resize to original resolution
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)

    depth_map_scaled = (depth_map_normalized*100).astype(np.uint8)

    depth_map_visual = (depth_map_normalized*255).astype(np.uint8)
    depth_map_colored = cv2.applyColorMap(depth_map_visual, cv2.COLORMAP_MAGMA)
    
    if show_depth_map:
        cv2.imshow('Depth Map', depth_map_colored)

    return depth_map_scaled
    