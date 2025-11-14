from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    x = LaunchConfiguration('x'); y = LaunchConfiguration('y'); z = LaunchConfiguration('z')
    model = LaunchConfiguration('model')

    # Default model path
    default_model = os.path.join(
        get_package_share_directory('unitree_g1_description'),
        'urdf', 'g1_29dof.urdf'
    )

    # Include Gazebo Classic with ROS factory plugin
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': os.path.join(get_package_share_directory('gazebo_ros'), 'worlds', 'empty.world'),
            'verbose': 'true'
        }.items()
    )

    return LaunchDescription([
        DeclareLaunchArgument('x', default_value='0.0'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='1.0'),
        DeclareLaunchArgument('model', default_value=default_model),

        gazebo_launch,

        # Publishes /robot_description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': Command(['xacro ', model])}],
            output='screen',
        ),

        # Spawns into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic','robot_description','-entity','g1','-x', x, '-y', y, '-z', z],
            output='screen',
        ),
    ])
