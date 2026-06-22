import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    this_dir = get_package_share_directory('vectornav')
    config_file = LaunchConfiguration('config_file')
    port = LaunchConfiguration('port')
    baud = LaunchConfiguration('baud')

    declare_config_file_cmd = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(this_dir, 'config', 'vectornav.yaml'))
    declare_port_cmd = DeclareLaunchArgument(
        'port',
        default_value='/dev/vn100')
    declare_baud_cmd = DeclareLaunchArgument(
        'baud',
        default_value='115200')
    
    # Vectornav
    start_vectornav_cmd = Node(
        package='vectornav', 
        executable='vectornav',
        output='screen',
        parameters=[
            config_file,
            {
                'port': port,
                'baud': baud,
            },
        ])
    
    start_vectornav_sensor_msgs_cmd = Node(
        package='vectornav', 
        executable='vn_sensor_msgs',
        output='screen',
        parameters=[config_file])

    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(declare_config_file_cmd)
    ld.add_action(declare_port_cmd)
    ld.add_action(declare_baud_cmd)
    ld.add_action(start_vectornav_cmd)
    ld.add_action(start_vectornav_sensor_msgs_cmd)

    return ld
