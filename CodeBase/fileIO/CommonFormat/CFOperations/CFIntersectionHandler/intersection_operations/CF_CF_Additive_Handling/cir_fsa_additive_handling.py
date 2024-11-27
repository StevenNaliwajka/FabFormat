from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_circle import CFCircle
from CodeBase.fileIO.CommonFormat.CFLayer.CFShapes.CFSolids.cf_filled_symmetrical_arc import CFFilledSymmetricalArc


def cir_fsa_additive_handling(cir1, fsa1, outer_left_pt, outer_right_pt, inner_left_pt, inner_right_pt):
    """
    Handles the additive overlap between a circle and a filled symmetrical arc.
    Maintains cir1 as a circle and creates a new complex shape using a symmetrical arc prim as an edge.

    :param cir1: The primary circle to preserve (CFCircle).
    :param fsa1: The filled symmetrical arc to use for creating the complex shape.
    :param outer_left_pt: Outer left intersection point, if any.
    :param outer_right_pt: Outer right intersection point, if any.
    :param inner_left_pt: Inner left intersection point, if any.
    :param inner_right_pt: Inner right intersection point, if any.
    :return: A new CFComplexShape containing the edge defined by the overlap.
    """
    # Validate inputs
    if not isinstance(cir1, CFCircle) or not isinstance(fsa1, CFFilledSymmetricalArc):
        raise TypeError("cir1 must be a CFCircle and fsa1 must be a CFFilledSymmetricalArc.")

    if not (outer_left_pt or outer_right_pt or inner_left_pt or inner_right_pt):
        raise ValueError("At least one intersection point must be provided.")

    # Determine intersection points
    start_pt = None
    end_pt = None
    if outer_left_pt and outer_right_pt:
        outer_start_pt = outer_left_pt
        outer_end_pt = outer_right_pt
    elif inner_left_pt and inner_right_pt:
        inner_start_pt = inner_left_pt
        inner_end_pt = inner_right_pt
    elif outer_left_pt or outer_right_pt:
        outer_start_pt = outer_left_pt or outer_right_pt
        outer_end_pt = outer_left_pt or outer_right_pt
    elif inner_left_pt or inner_right_pt:
        inner_start_pt = inner_left_pt or inner_right_pt
        inner_end_pt = inner_left_pt or inner_right_pt

    # Validate start and end points
    if not start_pt or not end_pt:
        raise ValueError("Both start and end points are required to create the arc edge.")

    # Create a symmetrical arc prim from cir1's edge within the overlap
    arc_edge = CFSymmetricalArcPrim(
        unit=cir1.unit,
        center_pt=cir1.center_pt,
        start_pt=start_pt,
        end_pt=end_pt,
        arc_radius=cir1.radius
    )

    # Create the new complex shape
    new_complex_shape = CFComplexShape(
        unit=cir1.unit,
        primitive_list=[arc_edge]  # Add the arc edge as the defining feature of the complex shape
    )

    return new_complex_shape
