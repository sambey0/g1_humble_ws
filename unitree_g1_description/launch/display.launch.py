from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg = FindPackageShare('unitree_g1_description')
    default_model = PathJoinSubstitution([pkg, 'urdf', 'g1_29dof.urdf'])

    model_arg = DeclareLaunchArgument('model', default_value=default_model,
                                      description='Path to G1 URDF/Xacro')

    # If your file is .xacro this will run xacro; if it’s .urdf it will just cat the file.
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'publish_frequency': 30.0}],
        output='screen'
    )

    jsp = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([pkg, 'rviz', 'display.rviz'])],
        output='screen'
    )

    return LaunchDescription([model_arg, rsp, jsp, rviz])
