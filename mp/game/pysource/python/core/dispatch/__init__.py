"""Multi-consumer multi-producer dispatching mechanism

Originally based on Django Dispatch (BSD), which in turn is based on Pydispatch (BSD) http://pypi.python.org/pypi/PyDispatcher/2.0.1
See license.txt for original license.

Modified for py-source-sdk-2013's purposes.
"""

from . dispatcher import Signal, receiver