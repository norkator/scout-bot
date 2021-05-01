import numpy


def get_avg_color(frame):
    avg_color_per_row = numpy.average(frame, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color
    # colors, count = numpy.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    # return colors[count.argmax()]
