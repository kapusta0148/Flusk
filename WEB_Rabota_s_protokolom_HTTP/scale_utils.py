def get_spn(envelope):
    lower_corner = list(map(float, envelope["lowerCorner"].split()))
    upper_corner = list(map(float, envelope["upperCorner"].split()))
    dx = abs(upper_corner[0] - lower_corner[0])
    dy = abs(upper_corner[1] - lower_corner[1])

    return str(dx), str(dy)
