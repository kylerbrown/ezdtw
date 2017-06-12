from scipy.spatial.distance import cdist
import numpy as np
try:
    from numba import jit
except ImportError:
    print('Warning, Numba not installed. Performance will be significantly slower')
    jit = lambda x: x

@jit
def dtw_distance(distances):
    '''calculate minimum cumulative distance'''
    DTW = np.empty_like(distances)
    DTW[:, 0] = np.inf
    DTW[0, :] = np.inf    
    DTW[0, 0] = 0
    for i in range(1, DTW.shape[0]):
        for j in range(1, DTW.shape[1]):
            DTW[i, j] = distances[i, j] + min(DTW[i-1, j],  # insertion
                                              DTW[i, j-1],  # deletion
                                              DTW[i-1, j-1] #match
                                             )
    return DTW

def backtrack(DTW):
    '''compute DTW backtrace
    DTW: a matrix of cumulative DTW paths
    returns (p, q): x and y index lists of the optimal DTW path'''
    i, j = DTW.shape[0] - 1, DTW.shape[1] - 1
    p, q = [i], [j]
    while i > 0 and j > 0:
        local_min = np.argmin((DTW[i - 1, j - 1], DTW[i, j - 1], DTW[i - 1, j]))
        if local_min == 0:
            i -= 1
            j -= 1
        elif local_min == 1:
            j -= 1
        else:
            i -= 1
        p.append(i)
        q.append(j)
    p.reverse()
    q.reverse()
    return p, q

def dtw(a, b, distance_metric='euclidean'):
    '''perform dynamic time warping on two matricies a and b
    first dimension must be time, second dimension shapes must be equal
    
    distance_metric: a string that matches a valid option for the 'metric' argument in
            scipy.spatial.distance.cdist, such as 'euclidean' 'cosine' 'correlaton'
            
    returns:
        trace_x, trace_y -- the warp path as two lists of indicies. Suitable for use in
        an iterpolation function such as numpy.interp
        
        to warp values from a to b, use: numpy.interp(warpable_values, trace_x, trace_y)
        to warp values from b to a, use: numpy.interp(warpable_values, trace_y, trace_x)
    '''
    distance = cdist(a, b, distance_metric)
    cum_min_dist = dtw_distance(distance)
    trace_x, trace_y = backtrack(cum_min_dist)
    return trace_x, trace_y
    
