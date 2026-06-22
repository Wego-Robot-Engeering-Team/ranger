#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    channel_type = LaunchConfiguration('channel_type', default='serial')
    serial_baudrate = LaunchConfiguration('serial_baudrate', default='1000000')
    inverted = LaunchConfiguration('inverted', default='false')
    angle_compensate = LaunchConfiguration('angle_compensate', default='true')
    scan_mode = LaunchConfiguration('scan_mode', default='DenseBoost')

    front_serial_port = LaunchConfiguration('front_serial_port', default='/dev/frontS3')
    rear_serial_port = LaunchConfiguration('rear_serial_port', default='/dev/rearS3')
    front_frame_id = LaunchConfiguration('front_frame_id', default='front_s3_laser')
    rear_frame_id = LaunchConfiguration('rear_frame_id', default='rear_s3_laser')

    return LaunchDescription([
        DeclareLaunchArgument(
            'channel_type',
            default_value=channel_type,
            description='Specifying channel type of lidar'),
        DeclareLaunchArgument(
            'serial_baudrate',
            default_value=serial_baudrate,
            description='Specifying usb port baudrate to connected lidar'),
        DeclareLaunchArgument(
            'inverted',
            default_value=inverted,
            description='Specifying whether or not to invert scan data'),
        DeclareLaunchArgument(
            'angle_compensate',
            default_value=angle_compensate,
            description='Specifying whether or not to enable angle compensation'),
        DeclareLaunchArgument(
            'scan_mode',
            default_value=scan_mode,
            description='Specifying scan mode of lidar'),
        DeclareLaunchArgument(
            'front_serial_port',
            default_value=front_serial_port,
            description='Front S3 serial port'),
        DeclareLaunchArgument(
            'rear_serial_port',
            default_value=rear_serial_port,
            description='Rear S3 serial port'),
        DeclareLaunchArgument(
            'front_frame_id',
            default_value=front_frame_id,
            description='Front S3 frame id'),
        DeclareLaunchArgument(
            'rear_frame_id',
            default_value=rear_frame_id,
            description='Rear S3 frame id'),
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='frontS3',
            parameters=[{
                'channel_type': channel_type,
                'serial_port': front_serial_port,
                'serial_baudrate': serial_baudrate,
                'frame_id': front_frame_id,
                'inverted': inverted,
                'angle_compensate': angle_compensate,
                'scan_mode': scan_mode,
            }],
            remappings=[('scan', 'frontS3/scan')],
            output='screen'),
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='rearS3',
            parameters=[{
                'channel_type': channel_type,
                'serial_port': rear_serial_port,
                'serial_baudrate': serial_baudrate,
                'frame_id': rear_frame_id,
                'inverted': inverted,
                'angle_compensate': angle_compensate,
                'scan_mode': scan_mode,
            }],
            remappings=[('scan', 'rearS3/scan')],
            output='screen'),
    ])
