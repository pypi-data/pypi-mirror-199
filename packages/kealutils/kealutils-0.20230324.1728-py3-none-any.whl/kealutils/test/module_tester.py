import os
import sys

sys.path.append(os.path.dirname(os.path.abspath((os.path.dirname(__file__)))))


from kealutils import utils as u

print(u.is_empty(""))
print(u.is_empty("input"))
