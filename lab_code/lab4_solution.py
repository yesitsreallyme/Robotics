"""
Sample Solution for Lab4
Use "run.py [--sim] lab4_solution" to execute
"""

import create2
import math
import odometry


class Run:
    def __init__(self, create, time, sonar, servo):
        """Constructor.

        Args:
            create (robot.Create2Driver)
            time (time)
            sonar (robot.Sonar)
            servo (robot.Servo)
        """
        self.create = create
        self.time = time
        self.sonar = sonar
        self.servo = servo
        self.odometry = odometry.Odometry()

    def sleep(self, time_in_sec, dt = 0):
        start = self.time.time()
        last_update = None
        while True:
            state = self.create.update()
            t = self.time.time()
            if state is not None:
                if last_update == None or t - last_update >= dt:
                    self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                    # don't include the groundTruth data if you run it on the robot!
                    groundTruth = self.create.sim_get_position()
                    print("{},{},{},{},{}".format(self.odometry.x, self.odometry.y, self.odometry.theta * 180 / math.pi, groundTruth[0], groundTruth[1]))
                    last_update = t
            if start + time_in_sec <= t:
                break

    def turn_left(self, speed, angle, dt):
        self.create.drive_direct(speed, -speed)
        self.sleep(math.pi * create2.Specs.WheelDistanceInMM / (360 / angle) / speed, dt)

    def forward(self, speed, distance, dt):
        self.create.drive_direct(speed, speed)
        self.sleep(distance / speed, dt)

    def rectangle(self, speed, dt):
        self.forward(speed, 1000, dt)
        self.turn_left(speed, 90, dt)
        self.forward(speed, 500, dt)
        self.turn_left(speed, 90, dt)
        self.forward(speed, 1000, dt)
        self.turn_left(speed, 90, dt)
        self.forward(speed, 500, dt)
        self.turn_left(speed, 90, dt)

    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        # normal speed, 15ms update rate
        self.rectangle(100, 0)

        # normal speed, 150ms update rate
        # self.rectangle(100, 0.150)

        # high speed, 15ms update rate
        # self.rectangle(300, 0)

        # Move forward, 15ms update rate
        # self.create.drive_direct(100, 100)
        # self.sleep(5, 0)

        # Move in circle, 150ms update rate
        # self.create.drive_direct(100, 50)
        # self.sleep(30, 0.15)
