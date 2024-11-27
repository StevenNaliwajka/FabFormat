def lin_lin_intersection(lin1, lin2):
    # Extract start and end points for both lines
    p1, p2 = lin1.start_pt, lin1.end_pt
    q1, q2 = lin2.start_pt, lin2.end_pt

    # Sort the points of each line to ensure p1 <= p2 and q1 <= q2
    if (p2[0], p2[1]) < (p1[0], p1[1]):
        p1, p2 = p2, p1
    if (q2[0], q2[1]) < (q1[0], q1[1]):
        q1, q2 = q2, q1

    # Check if the lines bound or overlap
    if (q1[0] > p2[0] or q2[0] < p1[0]) or (q1[1] > p2[1] or q2[1] < p1[1]):
        # No overlap or bounding
        return None

    # Determine the "left" and "right" intersection points
    outer_left_pt = max(p1, q1, key=lambda pt: (pt[0], pt[1]))
    outer_right_pt = min(p2, q2, key=lambda pt: (pt[0], pt[1]))

    # Determine the overlap_flag
    if outer_left_pt == outer_right_pt:
        overlap_flag = 0  # Touching but no overlap
    else:
        overlap_flag = 1  # Overlapping

    # Return the result as specified
    return lin1, outer_left_pt, outer_right_pt, overlap_flag