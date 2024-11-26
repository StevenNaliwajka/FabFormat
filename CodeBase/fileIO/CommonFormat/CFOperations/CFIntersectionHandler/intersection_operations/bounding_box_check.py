def bounding_box_check(bounding_box_1, bounding_box_2):
    # The most general check to see if a shape intersects with each-other.


    # takes in two bounding box touples of the following form
    # bx#_c_pt : Box # center point
    # bx#_w : Box # Width
    # bx#_h: Box # Height
    bx1_c_pt = bounding_box_1[0]
    bx1_w = bounding_box_1[1]
    bx1_h = bounding_box_1[2]

    bx2_c_pt = bounding_box_2[0]
    bx2_w = bounding_box_2[1]
    bx2_h = bounding_box_2[2]

    # Returns true if they overlap in both the X and the Y axis.

    # Unpack center points
    bx1_cx, bx1_cy = bx1_c_pt
    bx2_cx, bx2_cy = bx2_c_pt

    # Calculate the half-widths and half-heights of each box
    bx1_half_w = bx1_w / 2
    bx1_half_h = bx1_h / 2
    bx2_half_w = bx2_w / 2
    bx2_half_h = bx2_h / 2

    # Check if boxes overlap in the x-axis
    x_overlap = abs(bx1_cx - bx2_cx) <= (bx1_half_w + bx2_half_w)

    # Check if boxes overlap in the y-axis
    y_overlap = abs(bx1_cy - bx2_cy) <= (bx1_half_h + bx2_half_h)

    # Boxes intersect if they overlap in both axes: return true.
    return x_overlap and y_overlap