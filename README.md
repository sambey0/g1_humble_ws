# g1_humble_ws

ROS 2 Humble workspace to visualize and simulate **Unitree G1** in **RViz** and **Gazebo Classic**.

> Tested on Ubuntu 22.04, ROS 2 Humble, Gazebo Classic 11.

---

## Prerequisites

```bash
# ROS 2 Humble desktop
# https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

sudo apt update
sudo apt install -y \
  gazebo \
  ros-humble-gazebo-ros \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-joint-state-publisher-gui \
  ros-humble-xacro
```

---

## 1) Clone & Build

```bash
# 1) Get the workspace
git clone https://github.com/sambey0/g1_humble_ws.git
cd g1_humble_ws

# 2) Source ROS 2
source /opt/ros/humble/setup.bash

# 3) Build only this package (fast inner loop)
colcon build --symlink-install --packages-select unitree_g1_description

# 4) Source the workspace
source install/setup.bash
```

> Tip: add `source ~/g1_humble_ws/install/setup.bash` to your `~/.bashrc`.

---

## 2) RViz: View the Model

```bash
# (from the workspace root)
source /opt/ros/humble/setup.bash
source install/setup.bash

# Launch the model (URDF in the package share)
ros2 launch unitree_g1_description display.launch.py \
  model:=$(ros2 pkg prefix unitree_g1_description)/share/unitree_g1_description/urdf/g1_29dof.urdf
```

**If you only see the grid:** in RViz set **Global Options → Fixed Frame** to `pelvis` (or any valid link).

---

## 3) Gazebo Classic: Spawn the Robot

```bash
# Make sure both ROS 2 and your workspace are sourced
source /opt/ros/humble/setup.bash
source ~/g1_humble_ws/install/setup.bash

# (Optional: fix some Gazebo path warnings)
source /usr/share/gazebo/setup.sh

# Spawn into Gazebo (adjust x/y/z as needed)
ros2 launch unitree_g1_description spawn_gazebo.launch.py x:=0.0 y:=0.0 z:=0.6
```

You should see: `SpawnEntity: Successfully spawned entity [g1]`.

> Physics note: without controllers, joints have no torques—so the robot will fall under gravity. For a quick demo, you can pause physics, set a pose with `/set_model_configuration`, then unpause. Proper fix is adding `ros2_control` controllers.

---

## Notes & Troubleshooting

* **Meshes not visible**: URDF mesh paths use `package://unitree_g1_description/meshes/...` (already set). If you edited URDFs, keep that scheme.
* **RViz “Fixed frame does not exist”**: set it to `pelvis`.
* **Gazebo empty world / shader warnings**: `source /usr/share/gazebo/setup.sh`.
* **Rebuild after URDF edits**:

  ```bash
  colcon build --symlink-install --packages-select unitree_g1_description
  source install/setup.bash
  ```

---

## Project Layout

```
g1_humble_ws/
├─ unitree_g1_description/
│  ├─ launch/               # display.launch.py, spawn_gazebo.launch.py
│  ├─ meshes/               # STL meshes
│  ├─ urdf/                 # G1 URDFs (23/29 DoF variants)
│  ├─ package.xml, CMakeLists.txt
├─ build/ install/ log/     # colcon artifacts
```
