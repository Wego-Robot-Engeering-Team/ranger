import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sllidar_share = get_package_share_directory('sllidar_ros2')

    front_x_default = '0.61'
    front_y_default = '0.0'
    front_z_default = '0.28'
    front_roll_default = '0.0'
    front_pitch_default = '0.0'
    front_yaw_default = '3.141592653589793'

    rear_x_default = '-0.61'
    rear_y_default = '0.0'
    rear_z_default = '0.28'
    rear_roll_default = '0.0'
    rear_pitch_default = '0.0'
    rear_yaw_default = '0.0'

    target_frame_id_default = 'base_link'
    fixed_frame_id_default = 'base_link'
    serial_baudrate_default = '1000000'
    scan_mode_default = 'DenseBoost'
    filter_robot_body_default = 'true'
    motion_compensation_default = 'false'
    body_min_x_default = '-0.60'
    body_max_x_default = '0.60'
    body_min_y_default = '-0.45'
    body_max_y_default = '0.45'

    front_x = LaunchConfiguration('front_x')
    front_y = LaunchConfiguration('front_y')
    front_z = LaunchConfiguration('front_z')
    front_roll = LaunchConfiguration('front_roll')
    front_pitch = LaunchConfiguration('front_pitch')
    front_yaw = LaunchConfiguration('front_yaw')

    rear_x = LaunchConfiguration('rear_x')
    rear_y = LaunchConfiguration('rear_y')
    rear_z = LaunchConfiguration('rear_z')
    rear_roll = LaunchConfiguration('rear_roll')
    rear_pitch = LaunchConfiguration('rear_pitch')
    rear_yaw = LaunchConfiguration('rear_yaw')

    target_frame_id = LaunchConfiguration('target_frame_id')
    fixed_frame_id = LaunchConfiguration('fixed_frame_id')
    serial_baudrate = LaunchConfiguration('serial_baudrate')
    scan_mode = LaunchConfiguration('scan_mode')
    filter_robot_body = LaunchConfiguration('filter_robot_body')
    motion_compensation = LaunchConfiguration('motion_compensation')
    body_min_x = LaunchConfiguration('body_min_x')
    body_max_x = LaunchConfiguration('body_max_x')
    body_min_y = LaunchConfiguration('body_min_y')
    body_max_y = LaunchConfiguration('body_max_y')

    dual_s3_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sllidar_share, 'launch', 'dual_sllidar_s3_launch.py')),
        launch_arguments={
            'serial_baudrate': serial_baudrate,
            'scan_mode': scan_mode,
            'front_frame_id': 'front_s3_laser',
            'rear_frame_id': 'rear_s3_laser',
        }.items()
    )

    front_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='front_s3_tf',
        arguments=[
            '--x', front_x,
            '--y', front_y,
            '--z', front_z,
            '--roll', front_roll,
            '--pitch', front_pitch,
            '--yaw', front_yaw,
            '--frame-id', 'base_link',
            '--child-frame-id', 'front_s3_laser',
        ],
        output='screen'
    )

    rear_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='rear_s3_tf',
        arguments=[
            '--x', rear_x,
            '--y', rear_y,
            '--z', rear_z,
            '--roll', rear_roll,
            '--pitch', rear_pitch,
            '--yaw', rear_yaw,
            '--frame-id', 'base_link',
            '--child-frame-id', 'rear_s3_laser',
        ],
        output='screen'
    )

    merger = Node(
        package='laser_scan_merger',
        executable='scans_merger_node',
        name='laser_scan_merger',
        parameters=[{
            'active': True,
            'publish_scan': True,
            'publish_pcl': True,
            'motion_compensation': motion_compensation,
            'ranges_num': 1440,
            'min_scanner_range': 0.05,
            'max_scanner_range': 30.0,
            'min_x_range': -30.0,
            'max_x_range': 30.0,
            'min_y_range': -30.0,
            'max_y_range': 30.0,
            'filter_robot_body': filter_robot_body,
            'body_min_x': body_min_x,
            'body_max_x': body_max_x,
            'body_min_y': body_min_y,
            'body_max_y': body_max_y,
            'fixed_frame_id': fixed_frame_id,
            'target_frame_id': target_frame_id,
        }],
        remappings=[
            ('front_scan', '/frontS3/scan'),
            ('rear_scan', '/rearS3/scan'),
            ('scan', '/scan_filtered'),
            ('pcl', '/merged/points'),
        ],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument('front_x', default_value=front_x_default),
        DeclareLaunchArgument('front_y', default_value=front_y_default),
        DeclareLaunchArgument('front_z', default_value=front_z_default),
        DeclareLaunchArgument('front_roll', default_value=front_roll_default),
        DeclareLaunchArgument('front_pitch', default_value=front_pitch_default),
        DeclareLaunchArgument('front_yaw', default_value=front_yaw_default),
        DeclareLaunchArgument('rear_x', default_value=rear_x_default),
        DeclareLaunchArgument('rear_y', default_value=rear_y_default),
        DeclareLaunchArgument('rear_z', default_value=rear_z_default),
        DeclareLaunchArgument('rear_roll', default_value=rear_roll_default),
        DeclareLaunchArgument('rear_pitch', default_value=rear_pitch_default),
        DeclareLaunchArgument('rear_yaw', default_value=rear_yaw_default),
        DeclareLaunchArgument('target_frame_id', default_value=target_frame_id_default),
        DeclareLaunchArgument('fixed_frame_id', default_value=fixed_frame_id_default),
        DeclareLaunchArgument('serial_baudrate', default_value=serial_baudrate_default),
        DeclareLaunchArgument('scan_mode', default_value=scan_mode_default),
        DeclareLaunchArgument('filter_robot_body', default_value=filter_robot_body_default),
        DeclareLaunchArgument('motion_compensation', default_value=motion_compensation_default),
        DeclareLaunchArgument('body_min_x', default_value=body_min_x_default),
        DeclareLaunchArgument('body_max_x', default_value=body_max_x_default),
        DeclareLaunchArgument('body_min_y', default_value=body_min_y_default),
        DeclareLaunchArgument('body_max_y', default_value=body_max_y_default),
        dual_s3_bringup,
        front_tf,
        rear_tf,
        merger,
    ])
