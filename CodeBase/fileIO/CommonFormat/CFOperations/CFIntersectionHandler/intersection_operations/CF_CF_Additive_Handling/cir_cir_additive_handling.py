from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc


def cir_cir_additive_handling(cir1, cir2, outer_left_pt, outer_right_pt, inner_left_pt, inner_right_pt):
    """
    Handles the additive overlap between two circles. Maintains cir1 as a circle and modifies cir2 to a filled symmetrical arc.

    :param cir1: The primary circle to preserve (CFCircle).
    :param cir2: The secondary circle to modify (CFCircle).
    :param outer_left_pt: Outer left intersection point, if any.
    :param outer_right_pt: Outer right intersection point, if any.
    :param inner_left_pt: Inner left intersection point, if any.
    :param inner_right_pt: Inner right intersection point, if any.
    :return: A new CFFilledSymmetricalArc representing the modified cir2.
    """
    # Validate inputs
    if not isinstance(cir1, CFCircle) or not isinstance(cir2, CFCircle):
        raise TypeError("Both cir1 and cir2 must be instances of CFCircle.")

    if not (outer_left_pt or outer_right_pt or inner_left_pt or inner_right_pt):
        raise ValueError("At least one intersection point must be provided.")

    # Extract necessary data from cir2
    center_pt = cir2.center_pt
    radius = cir2.radius

    # Determine the points for the filled symmetrical arc
    start_pt = outer_left_pt if outer_left_pt else inner_left_pt
    end_pt = outer_right_pt if outer_right_pt else inner_right_pt

    if not (start_pt and end_pt):
        raise ValueError("Both start and end points are required to form a symmetrical arc.")

    # Create the filled symmetrical arc
    arc = CFFilledSymmetricalArc(
        unit=cir2.unit,
        center_pt=center_pt,
        start_pt=start_pt,
        end_pt=end_pt,
        arc_radius=radius,
        inner_off=cir2.inner_radius if cir2.inner_radius else 0
    )

    return arc
