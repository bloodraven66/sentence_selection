import collections
import math

def entropy(list2D):
    s = [j for sub in list2D for j in sub]
    probabilities = [n_x/len(s) for x,n_x in collections.Counter(s).items()]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]
    return sum(e_x)
