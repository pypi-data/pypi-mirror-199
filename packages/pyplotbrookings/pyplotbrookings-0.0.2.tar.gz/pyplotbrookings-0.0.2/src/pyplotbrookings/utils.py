import matplotlib.pyplot as plt

def get_coords(loc, obj=None):
    '''
    Helper function for getting plot coordinates
    '''
    fig = plt.gcf()
    # If passed an object get its coords
    if obj is None:
        bbox = fig.get_tightbbox(fig.canvas.get_renderer())
        coords = fig.transFigure.inverted().transform(bbox)*100
    # Otherwise get the figure coords
    else:
        bbox = obj.get_tightbbox(fig.canvas.get_renderer())
        coords = fig.transFigure.inverted().transform(bbox)
    
    return {'left': coords[0, 0], 'right': coords[1, 0], 'bottom': coords[0, 1], 'top': coords[1, 1]}[loc]
