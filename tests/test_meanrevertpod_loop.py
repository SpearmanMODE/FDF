import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from strategies.meanrevert import MeanRevertPod
from ib_insync import IB
import time
import time
from ib_insync import IB
from strategies.meanrevert import MeanRevertPod

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)

pod = MeanRevertPod(ib)

for i in range(30):
    pod.run_once()
    time.sleep(5)