import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from strategies.meanrevert import MeanRevertPod
from ib_insync import IB

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=11)

pod = MeanRevertPod(ib)
pod.run_once()
