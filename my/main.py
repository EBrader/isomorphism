from create_g import *
from ut.graph_io import *

with open('dot/mygraph_c.dot', 'w') as c:
    write_dot(createComplement("null", createPath(5)), c)
