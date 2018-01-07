import os
print __file__

B = os.path.dirname(os.path.realpath(__file__))
# B is the canonicalised (?) directory where the program resides.

C = os.path.abspath(os.path.dirname(__file__))

print os.path.join(os.path.dirname(__file__), '..')
print os.path.dirname(os.path.realpath(__file__))
print os.path.abspath(os.path.dirname(__file__))
