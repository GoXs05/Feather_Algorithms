import numpy as np

def calculate_distance(depth_map_scaled, xmin, xmax, ymin, ymax):
    rel_dist = np.median(depth_map_scaled[ymin:ymax, xmin:xmax])
    abs_dist = ((0.0036*rel_dist*rel_dist) - (0.5373*rel_dist) + 21.714) / 4
    
    return abs_dist