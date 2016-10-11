"""
Sample Code for Lab1
Use "run.py [--sim] lab1" to execute
"""


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

    def run(self):
        self.create.start()
        self.create.safe()

        self.create.drive_direct(-100, -100)
        self.time.sleep(5)
        self.create.drive_direct(-19, 19)
        self.time.sleep(10)
        self.create.drive_direct(100, 100)
        self.time.sleep(10)
        self.create.drive_direct(100, -100)
        self.time.sleep(5)
        self.create.drive_direct(100, -100)

       
        self.create.stop()
