"""
Actual helper script to execute code.
It takes care of proper error handling (e.g. if you press CTRL+C) and the difference between
running code on the robot vs. in simulation.

Usage:
  python3 run.py --sim lab1 [for simulation]
  python3 run.py lab1 [to run on a robot]
"""


import sys
import argparse
import importlib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run", help="run specified module")
    parser.add_argument("--sim", help="Run using VREP simulation", action="store_true")
    args = parser.parse_args()
    clientID = None
    if args.sim:
        from simulation.vrep import vrep as vrep
        vrep.simxFinish(-1)  # just in case, close all opened connections
        clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP

        # enable the synchronous mode on the client:
        vrep.simxSynchronous(clientID, True)

        # start the simulation:
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)

        from simulation import KukaLBR4PlusVrep, TimeHelper
        arm = KukaLBR4PlusVrep(clientID)
        timeHelper = TimeHelper(clientID)
    else:
        pass

    try:
        mod = importlib.import_module(args.run)
        Run = getattr(mod, "Run")
        r = Run(arm, timeHelper)
        r.run()
    except KeyboardInterrupt:
        pass

    if args.sim:
        # stop the simulation:
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        # close the connection to V-REP:
        vrep.simxFinish(clientID)

    # quit
    sys.exit()
