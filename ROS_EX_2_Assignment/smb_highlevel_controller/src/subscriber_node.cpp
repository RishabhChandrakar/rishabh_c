#include<ros/ros.h>
#include<std_msgs/String.h>
#include<std_msgs/Float32.h>

void callback(const sensor_msgs::LaserScan::ConstPtr& scan){

    auto min_distance = std::min_element(scan->ranges.begin(), scan->ranges.end());
    
    ROS_INFO("Minimum distance: %f", min_distance);

}


int main(int argc, char* argv[]){

    ros::init(argc, argv, "subscriber_node");
    ros::NodeHandle subscriber_nodehandle;

    std::string laser_scan_topic;
    int queue_size;

    subscriber_nodehandle.param<std::string>("laser_scan_topic", laser_scan_topic, "/scan");
    subscriber_nodehandle.param<int>("queue_size", queue_size, 1000);

    ros::Subscriber subscriber=subscriber_nodehandle.subscribe(laser_scan_topic,queue_size, callback);
     
    ros::spin();

    return 0;

}
