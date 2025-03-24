#!/usr/bin/env python3

import rospy
import sys
import numpy as np
from geometry_msgs.msg import Twist

print(sys.version)

class GoLogarithmicTrajectory():
    def __init__(self, a, b):
        rospy.init_node('turtlesim_script', anonymous=False)
        rospy.loginfo("To stop Turtle CTRL + C")

        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        self.turn_left(83)

        r = rospy.Rate(10)
        t = 0.0
        while not rospy.is_shutdown() and t < 1.0:
            move_cmd = Twist()
            # Параметризация траектории
            x = a + (b - a) * t
            y = np.log(x)
            
            # Вычисление скорости
            dx_dt = (b - a)
            dy_dt = 1 / x * dx_dt
            
            # Линейная скорость
            move_cmd.linear.x = np.sqrt(dx_dt**2 + dy_dt**2)
            
            # Угловая скорость
            move_cmd.angular.z = np.arctan2(dy_dt, dx_dt)
            
            self.cmd_vel.publish(move_cmd)
            rospy.loginfo(f"X: {x}, Y: {y}, Linear: {move_cmd.linear.x}, Angular: {move_cmd.angular.z}")
            r.sleep()
            t += 0.08  # Увеличиваем параметр t

    def turn_left(self, angle):
        """Поворачивает черепашку на заданный угол влево."""
        turn_cmd = Twist()
        turn_cmd.angular.z = np.radians(angle)  # Преобразуем градусы в радианы
        start_time = rospy.Time.now()
        duration = rospy.Duration(1)  # Задаем длительность поворота
        while rospy.Time.now() - start_time < duration:
            self.cmd_vel.publish(turn_cmd)
            rospy.sleep(0.1)

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleSim")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        a, b = 1, 5
        GoLogarithmicTrajectory(a, b)
    except:
        rospy.loginfo("GoForward node terminated.")
        rospy.loginfo(sys.exc_info()[:2])