from pymouse import PyMouse
from collections import deque
from itertools import islice

m = PyMouse()

x_dim, y_dim = m.screen_size()
m.move(400, 400)

def moving_average(asd, n=10):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    d = asd
    s = sum(d)
    print (s / n)


promediadorY = [1,2,3,4,5,6,7,8,9,10]
deqY = deque(promediadorY)
moving_average(deqY)
