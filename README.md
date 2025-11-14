# 1) Get the workspace
git clone https://github.com/sambey0/g1_humble_ws.git
cd g1_humble_ws

# 2) Source ROS 2
source /opt/ros/humble/setup.bash

# 3) Build only this package (fast inner loop)
colcon build --symlink-install --packages-select unitree_g1_description

# 4) Source the workspace
source install/setup.bash



2) RViz: View the model
# (from the workspace root)
source /opt/ros/humble/setup.bash
source install/setup.bash

# Launch the model (uses a URDF in the package share)
ros2 launch unitree_g1_description display.launch.py \
  model:=$(ros2 pkg prefix unitree_g1_description)/share/unitree_g1_description/urdf/g1_29dof.urdf


# Make sure both ROS 2 and your workspace are sourced
source /opt/ros/humble/setup.bash
source ~/g1_humble_ws/install/setup.bash

# Spawn into Gazebo (x/y/z can be adjusted)
ros2 launch unitree_g1_description spawn_gazebo.launch.py x:=0.0 y:=0.0 z:=0.6
