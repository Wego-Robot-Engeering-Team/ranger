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
    slam_toolbox_base_path = get_package_share_path('slam_toolbox')

    gui_arg = DeclareLaunchArgument(
        'slam_gui',
        default_value='true',
        description='Launch RViz2 together with 2D SLAM'
    )
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value=os.path.join(wego_base_path, 'rviz', 'slam.rviz'),
        description='RViz2 config file'
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )
    slam_params_file_arg = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(wego_base_path, 'config', 'slam_toolbox_2d.yaml'),
        description='slam_toolbox parameter file'
    )

    teleop_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(wego_base_path / 'launch/teleop_launch.py')),
        launch_arguments={
            'gui': 'false',
        }.items()
    )

    slam_toolbox_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(slam_toolbox_base_path / 'launch/online_async_launch.py')),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'slam_params_file': LaunchConfiguration('slam_params_file'),
        }.items()
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
        condition=IfCondition(LaunchConfiguration('slam_gui'))
    )

    return LaunchDescription([
        gui_arg,
        rviz_config_arg,
        use_sim_time_arg,
        slam_params_file_arg,
        teleop_bringup,
        slam_toolbox_bringup,
        rviz_node,
    ])
