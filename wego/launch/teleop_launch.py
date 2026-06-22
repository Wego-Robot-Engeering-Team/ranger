import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_path


def generate_launch_description():
    wego_base_path = get_package_share_path('wego')
    ranger_base_path = get_package_share_path('ranger_base')
    vectornav_base_path = get_package_share_path('vectornav')
    scan_merger_base_path = get_package_share_path('laser_scan_merger')
    robot_localization_base_path = get_package_share_path('robot_localization')

    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='false',
        description='Launch RViz2 together with teleop bringup'
    )
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=os.path.join(wego_base_path, 'rviz', 'display.rviz'),
        description='RViz2 config file'
    )
    body_min_x_arg = DeclareLaunchArgument('body_min_x', default_value='-0.60')
    body_max_x_arg = DeclareLaunchArgument('body_max_x', default_value='0.60')
    imu_x_arg = DeclareLaunchArgument('imu_x', default_value='0.0')
    imu_y_arg = DeclareLaunchArgument('imu_y', default_value='0.0')
    imu_z_arg = DeclareLaunchArgument('imu_z', default_value='0.28')
    imu_roll_arg = DeclareLaunchArgument('imu_roll', default_value='0.0')
    imu_pitch_arg = DeclareLaunchArgument('imu_pitch', default_value='0.0')
    imu_yaw_arg = DeclareLaunchArgument('imu_yaw', default_value='0.0')

    ranger_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(ranger_base_path / 'launch/ranger.launch.py')),
        launch_arguments={
            'publish_odom_tf': 'false',
        }.items()
    )

    imu_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(vectornav_base_path / 'launch/vectornav.launch.py'))
    )

    imu_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='vectornav_tf',
        arguments=[
            '--x', LaunchConfiguration('imu_x'),
            '--y', LaunchConfiguration('imu_y'),
            '--z', LaunchConfiguration('imu_z'),
            '--roll', LaunchConfiguration('imu_roll'),
            '--pitch', LaunchConfiguration('imu_pitch'),
            '--yaw', LaunchConfiguration('imu_yaw'),
            '--frame-id', 'base_link',
            '--child-frame-id', 'vectornav',
        ],
        output='screen'
    )

    lidar_and_merger_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(scan_merger_base_path / 'launch/dual_s3_scan_merger.launch.py')),
        launch_arguments={
            'body_min_x': LaunchConfiguration('body_min_x'),
            'body_max_x': LaunchConfiguration('body_max_x'),
        }.items()
    )

    robot_localization_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(robot_localization_base_path / 'launch/ranger_ekf.launch.py'))
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    return LaunchDescription([
        gui_arg,
        rviz_config_arg,
        body_min_x_arg,
        body_max_x_arg,
        imu_x_arg,
        imu_y_arg,
        imu_z_arg,
        imu_roll_arg,
        imu_pitch_arg,
        imu_yaw_arg,
        ranger_bringup,
        imu_bringup,
        imu_tf,
        lidar_and_merger_bringup,
        robot_localization_bringup,
        rviz_node,
    ])
