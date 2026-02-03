from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription(
        [
            Node(
                package="robot_state",
                executable="state_node",
                name="state_node",
                output="screen",
                parameters=[{"odom_topic": "/odom1", "pose_topic": "/robot_pose"}],
            ),
            Node(
                package="lidar_processing",
                executable="obstacle_extractor_node",
                name="obstacle_extractor",
                output="screen",
            ),
            Node(
                package="potential_fields",
                executable="field_planner_node",
                name="field_planner",
                output="screen",
                parameters=[{"d0": 5.0, "epsilon1": 1.0, "epsilon2": 1.0, "eta": 2.0}],
            ),
            Node(
                package="motion_controller",
                executable="velocity_controller_node",
                name="velocity_controller",
                output="screen",
            ),
        ]
    )
