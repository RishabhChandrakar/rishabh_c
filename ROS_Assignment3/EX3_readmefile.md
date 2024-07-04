#Here are the steps to complete the assignment 3

For Que1
Download the smb_common_v2 zipped folder from the given link . Unzip it and place it in the ~/git folder.

Then Navigate to source folder of workspace through following commmand cd ~/Workspaces/smb_ws/src Create a symlink to the smb_common_v2 through

ln -s ~/git/smb_common_v2
This command creates a symbolic link named smb_common in src directory that points to the ~/git/smb_common_v2 directory .

to compile it , navigate to root directory of workspace and type the command

catkin_make 
to compile the workspace ,then source the workspce by command

source devel/setup.bash
For Que2 , To create a launch file from the previous one
First remove the keyboard twist node .

Download singlePillar.world as mentioned in the ques.

And then update the launch file to add the new world through this command

<arg name="world_file" default="$(find smb_highlevel_controller)/worlds/singlePillar.world"/> "
For task 3 , 4 ,5 we will write the node which will extract the position of the pillar from the laser scan by subscribing to "laser_scan" topic and then we will make a controller in this node which will find the relative position of the pillar and then direct the robot accordingly to reach there .
like this

rospy.Subscriber('/scan', LaserScan, self.laser_callback)

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
Here we laser_callback function is called whenever it receives msg from laser through '/scan' topic , and then it finds minimum distance from laser to pillar ,

and then it calciulates its relative location with respect to robot with the help of sin and cos function to calculate y & x oordinates respectively .

And then we will publish the velocity of the robot , calculated by our controller function , in "/cmd_vel" topic.

since we are about to publish velocity using "geometry_msgs" package we have to make some changes in the package , first add geometry_msgs as a dependency to your CMakeLists.txt and package.xml like

In CMakeLists.txt

find_package(catkin REQUIRED COMPONENTS roscpp sensor_msgs geometry_msgs )

And in package.xml

<depend>geometry_msgs</depend>

we are adding this package geometry_msgs package because we would be using it in our publiher node to publish the velocity , like this

   def driver(self, pillar_x, pillar_y):
   
    distance_error = pillar_x
    angle_error = math.atan2(pillar_y, pillar_x)
    
    cmd = Twist()
    cmd.linear.x = self.kp_linear * distance_error
    cmd.angular.z = self.kp_angular * angle_error
    self.cmd_vel_pub.publish(cmd)
here this driver function acts as a controller or it directs velocity to robot , first it gets relative position of pillar with respect to robot , and then it calculates the speed depending on how far it is from robot and angular speed depending upon at what angle the pillar is . then keeps on updating the speed depending upon current relative position of pillar .

The code to create the node i will upload it in different file named "controller.py" .

And to pass the laser_scan_min_height to -0.2 and laser_scan_max_height to 1.0 as arguments , we will add following lines in launch file

<param name="laser_scan_min_height" value="-0.2"/>
<param name="laser_scan_max_height" value="1.0"/>


<node name="your_laser_scanner_node" pkg="your_laser_scanner_package" type="your_laser_scanner_executable" output="screen">

<param name="laser_scan_min_height" value="$(arg laser_scan_min_height)"/>
<param name="laser_scan_max_height" value="$(arg laser_scan_max_height)"/>
</node>
To visualize the SMB robot in Rviz , follow the following steps
For your robot model you would need a URDF file for your SMB robot. You can create it or you can download it also , let's assume it is named smb.urdf and located in the smb_description package of your workspace .

navigate to the smb_description/launch directory (create it if it doesn't exist) , through following command

cd ~/Workspaces/smb_ws/src/smb_description/launch
mkdir -p ~/Workspaces/smb_ws/src/smb_description/
Create a new launch file named visual.launch

touch visual.launch
and add following content in this launch file

<launch>

<param name="robot_description" command="$(find xacro)/xacro $(find smb_description)/urdf/smb.urdf"/>


<node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" output="screen">
    <param name="publish_frequency" type="double" value="50.0"/>
    <param name="tf_prefix" type="string" value=""/>
</node>
now before running compile it agin though

cd ~/Workspaces/smb_ws
catkin_make
now launch the file for visualization

roslaunch smb_description visual.launch
now open rviz through following command

rosrun rviz rviz
add the RobotModel Plugin

in rviz window , look for the "Displays" panel on the left side. click the "Add" button at the bottom of the "Displays" panel. In the pop-up window, scroll down and select "RobotModel", then click "OK". Configure the RobotModel Plugin:

In the "Displays" panel, you should now see an entry for "RobotModel".

Ensure the "Robot Description" parameter is set to /robot_description (this should be the default) , this robot_descripyion is your parameter name in your visual.launch file which loads your urdf file .

Now to solve que 7 ,
in the rviz window,

locate the "Displays" panel on the left side. Click on the "Add" button at the bottom of the "Displays" panel.

In the "Add Display" dialog that appears, scroll down or search for "TF" in the search bar. Select "TF" and click "OK" to add it.

After adding the TF plugin, it will appear in the "Displays" panel.

Click on the TF plugin to open its configuration options.

Configure the TF plugin settings as per your needs:

Choose a frame that makes sense for your application , for example : baselinlk , odom , etc.

Now to solve que 8 , to implement the tf listener to transform the extracted point from
the laser frame to the odom frame .

First ensure your ROS package has the necessary dependencies tf2_rosin CMakeLists.txt and package.xml .

write the following code in your main script wher you extract the position of pillar from laser_scan

tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)

def transform_point(laser_point):

   
    laser_point_stamped = PointStamped()
    laser_point_stamped.header.frame_id = "laser_frame"
    laser_point_stamped.header.stamp = rospy.Time.now()
    laser_point_stamped.point = laser_point

    
    odom_point_stamped = tf_buffer.transform(laser_point_stamped, "odom")

    return odom_point_stamped.point
to use this tf_listener , in your main loop or callback where you have the laser point or extracted position of the pillar call the transform_point method to get the transformed point.
