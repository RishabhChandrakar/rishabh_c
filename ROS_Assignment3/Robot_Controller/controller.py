import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class pillarcontroller:
    def __init__(self):
        rospy.init_node('pillar_controller', anonymous=True)
    
        rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        
    
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        
        self.kp_linear = rospy.get_param('~kp_linear', 0.5)
        self.kp_angular = rospy.get_param('~kp_angular', 2.0)
        
        self.pillar_position = None

    def laser_callback(self, scan):
      
        kp_linear = rospy.get_param('~kp_linear', 0.5)
        kp_angular = rospy.get_param('~kp_angular', 2.0)

     
        mind = float('inf')
        min_a = 0

        for i, range in enumerate(scan.ranges):
            if range < mind:
                mind = range
                min_a = scan.angle_min + i * scan.angle_increment

        
        pillar_x = mind * math.cos(min_a)
        pillar_y = mind * math.sin(min_a)
        self.pillar_position = (pillar_x, pillar_y)

        rospy.loginfo(f"Pillar position: x={pillar_x}, y={pillar_y}")

        
        self.driver(pillar_x, pillar_y)

    def driver(self, pillar_x, pillar_y):
       
        distance_error = pillar_x
        angle_error = math.atan2(pillar_y, pillar_x)
        
        cmd = Twist()
        cmd.linear.x = self.kp_linear * distance_error
        cmd.angular.z = self.kp_angular * angle_error
        self.cmd_vel_pub.publish(cmd)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    
    controller = pillarcontroller()
    controller.run()
  
