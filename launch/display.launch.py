from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    xacro_file = os.path.join(
        os.path.expanduser("~"),
        "ros2_ws",
        "src",
        "differential_robot_simulation",
        "model",
        "robot.xacro",
    )

    robot_description = ParameterValue(Command(["xacro ", xacro_file]), value_type=str)

    urg_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("urg_node2"),
                "launch",
                "urg_node2.launch.py",
            )
        )
    )

    return LaunchDescription(
        [
            # ── Robot description ────────────────────────────────────────
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                arguments=["0", "0", "0", "0", "0", "0", "lidar_link", "laser"],
            ),
            # ── Lidar ────────────────────────────────────────────────────
            urg_launch,
            # ── Hardware bridge ──────────────────────────────────────────
            Node(
                package="esp_bridge",
                executable="esp_bridge_node",
                name="esp_bridge",
                output="screen",
            ),
            # ── Visualización ────────────────────────────────────────────
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=[
                    "-d",
                    os.path.join(
                        get_package_share_directory("robot_bringup"), "display.rviz"
                    ),
                ],
            ),
        ]
    )
