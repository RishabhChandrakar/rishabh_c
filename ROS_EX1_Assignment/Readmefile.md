1. For 1st ques , download the smb_common zipped folder from the course website , after downloading unzip it and place it in the ~/git folder . write the following commands 

"mkdir -p ~/git"  
"unzip path_to_smb_common_zip -d ~/git"

Now navigate to you src directory of you workspace , and to make a symlink for your smb_common folder , type the commands 

"ln -s ~/git/smb_common ."

This command creates a symbolic link named smb_common in src directory that points to the ~/git/smb_common directory .

to compile it , navigate to root directory of workspace and type the command 

"catkin_make" 

to compile the workspace ,then source the workspce by command

 "source devel/setup.bash" .


2. For 2nd Ques ,Launch the smb_gazebo package using command 
"roslaunch smb_gazebo smb_gazebo.launch". 

While launching , ther is a chance of occuring of some error , if it is due to unavailability of some dependencies then install those ROS dependencies with the help of sudo command.

Like this , 1st update your package list through command "sudo apt-get update"

then install it by typing "sudo apt-get install ros-noetic-hector-gazebo-plugins"

replace hector-gazebo-plugins with your required dependency's name .

OR clone the required repository into your workspace
by "git clone https://github.com/tu-darmstadt-ros-pkg/hector_gazebo.git"

It launched several nodes and a gazebo simulator.
After the package is launched used "rosnode list" and "rostopic list" to find the running node and list
Then used "rostopic echo /cmd_vel" to check what is being published to /cmd_vel topic

Then used rqt_graph to check all nodes and topics .

3. For 3rd ques:-
Used rostopic pub /cmd_vel geometry_msgs/Twist 
                        "Linear: X:0.0
							y:1.0
							z:0.0
						angular:
							x:0.0
							y:0.0
							z:1.0"

4. For 4th ques , clone teleop_twist_keyboard git repo through git clone .Then launche teleop_twist_keyboard node using "rosrun teleop_twist_keyboard teleop_twist_keyboard .py"
Through this command we can move bot through the keys on our keyboard. We can visualize the motion on gazebo .

5. For 5th ques ,create a launch file which will launch gazebo launch but with change in world argument to the environmnet given in ques.

<launch>
<include file="$(find smb_gazebo)/launch/smb_gazebo.launch">
        <arg name="world_file" value="/usr/share/gazebo-11/worlds/robocup14_spl_field.world"/>
 </include>
</launch>"
