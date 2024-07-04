# Here are the steps to complete EX4

1. To complete task 1 , which asking us to find out what the node ekf_localization is doing 

first of all run the launch file of you package so that we can see what exaclyt this node is doing , for that run the command 

    roslaunch smb_highlevel_controller smb_highlevel_controller.launch

then to find information about /ekf_localization node , run the 'rqt_graph' to see in pictorial form .

OR you can directly run 
    rosnode info /ekf_localization 
 

and you will find  the ekf localization subscribes to `/imu/data` and `/smb_velocity_controller/odom` topics and publishes `/odometry/filtered` topic .

2. for doing this task , first of all launch the package you built in last exercise through following command 


then , in another terminal run 'rqt_multiplot' , In the rqt_multiplot window, to add a new plot click on the Add new plot button (usually represented by a '+' icon) ,
A new plot area will appear in the workspace.

then to configure plot ,right click on the new plot area and select Add Curve. A new window will pop up to configure the curve.

to set curve parameters:

Curve Name: Give a name to the curve.
Topic: Select the topic you want to plot . Here we want to plot /odometry/filtered .

and then select the specific field you want to plot , here the pose/pose/position/x against pose/pose/position/y

and at last , click apply to add the curve to the plot.

3. and now tonvestigate the smb_navigation.bag file run the following command 

    rosbag info smb_navigation.bag

4. to complete the task 4 . write the launch file 

        <launch>
        
        <param file="$(find smb_control)/config/localization.yaml" command="load" />

        
        <node name="ekf_localization_node" pkg="robot_localization" type="ekf_localization_node" output="screen">
            
            <remap from="/smb_velocity_controller/odom" to="smb_velocity_controller/odom" />
            <remap from="imu/data" to="/imu/data" />
    
            
        </node>
        </launch>



and dont forget to write the names of the topic , which are there in smb_navigation.bag , in a localiztion.yaml file   

and then run the rosbag play to read the content of smb_navigation.bag in another terminal thorugh following command 

    rosbag play smb_navigation.bag --clock

5. to plot the path of the recorded robot in the x/y-plane , repeat the steps of task 2

6. 

<launch>
   
    <param name="/use_sim_time" value="true" />

    
    <param file="$(find smb_control)/config/localization.yaml" command="load" />

    
    <param name="robot_description" command="$(find xacro)/xacro '$(find smb_description)/urdf/smb.urdf.xacro'" />

    
    <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" output="screen">
        <param name="publish_frequency" value="50.0" />
    </node>

    
    <node name="ekf_localization_node" pkg="robot_localization" type="ekf_localization_node" output="screen">
        
        <remap from="/smb_velocity_controller/odom" to="smb_velocity_controller/odom" />
        <remap from="imu/data" to="/imu/data" />
        
    </node>

</launch>

and then in open aother terminal , and run 

    rosbag play smb_navigation.bag --clock

and then in another terminal run rviz for visualizing the movement of robot 

    rviz

and then in rviz,  add a RobotModel display type
set the Robot Description parameter to robot_description , 
add a TF display type to visualize the TF frames.

now you would visualize the SMB model and its motion in RViz. 



