from .process import ProcessStartLoop
from ..include_modules import LIST_MODULES

LIST_LOOPS = []

for module in LIST_MODULES:
    LIST_LOOPS.append(ProcessStartLoop(module))
