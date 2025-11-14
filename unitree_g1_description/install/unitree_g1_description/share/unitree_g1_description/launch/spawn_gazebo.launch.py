from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    pkg = FindPackageShare('unitree_g1_description')
    model_path = PathJoinSubstitution([pkg, 'urdf', 'g1_29dof.urdf'])

    # Resolve xacro/urdf to string for robot_description
    robot_description = ParameterValue(Command(['xacro ', model_path]), value_type=str)

    # Help Gazebo find meshes referenced via package://
    pkg_share = PathJoinSubstitution([pkg])
    env_gazebo = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[LaunchConfiguration('GAZEBO_MODEL_PATH', default=''), (':' if os.getenv('GAZEBO_MODEL_PATH') else ''), pkg_share]
    )

    # Gazebo (classic) empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare('gazebo_ros'), '/launch', '/gazebo.launch.py']
        )
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    # Spawn from /robot_description
    spawner = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'g1'],
        output='screen'
    )

    return LaunchDescription([
        env_gazebo,
        gazebo,
        rsp,
        spawner
    ])
