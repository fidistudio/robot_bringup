from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def create_nodes(context, *args, **kwargs):
    nav_mode = LaunchConfiguration("nav").perform(context)
    is_real = nav_mode.upper() == "REAL"

    # ── Nodos comunes a ambos modos ──────────────────────────────────

    velocity_controller = Node(
        package="motion_controller",
        executable="velocity_controller_node",
        name="velocity_controller",
        output="screen",
    )

    # ── Nodos que cambian según el modo ──────────────────────────────
    if is_real:
        state_node = Node(
            package="robot_state",
            executable="state_node",
            name="state_node",
            output="screen",
            parameters=[{"odom_topic": "/odom", "pose_topic": "/robot_pose"}],
        )
        obstacle_extractor = Node(
            package="lidar_processing",
            executable="obstacle_extractor_real_node",
            name="obstacle_extractor",
            output="screen",
        )
        field_planner = Node(
            package="potential_fields",
            executable="field_planner_real_node",
            name="field_planner",
            output="screen",
            parameters=[{"d0": 5.0, "epsilon1": 1.0, "epsilon2": 1.0, "eta": 2.0}],
        )
    else:  # SIM
        state_node = Node(
            package="robot_state",
            executable="state_node",
            name="state_node",
            output="screen",
            parameters=[{"odom_topic": "/odom1", "pose_topic": "/robot_pose"}],
        )
        obstacle_extractor = Node(
            package="lidar_processing",
            executable="obstacle_extractor_node",
            name="obstacle_extractor",
            output="screen",
        )
        field_planner = Node(
            package="potential_fields",
            executable="field_planner_node",
            name="field_planner",
            output="screen",
            parameters=[{"d0": 5.0, "epsilon1": 1.0, "epsilon2": 1.0, "eta": 2.0}],
        )

    return [state_node, obstacle_extractor, field_planner, velocity_controller]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "nav",
                default_value="SIM",
                description="Modo de navegación: SIM o REAL",
                choices=["SIM", "REAL", "sim", "real"],
            ),
            OpaqueFunction(function=create_nodes),
        ]
    )
