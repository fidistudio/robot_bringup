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
            executable="obstacle_extractor_real",
            name="obstacle_extractor",
            output="screen",
        )
        field_planner = Node(
            package="potential_fields",
            executable="field_planner_real",
            name="field_planner",
            output="screen",
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
            executable="obstacle_extractor_sim",
            name="obstacle_extractor",
            output="screen",
        )
        field_planner = Node(
            package="potential_fields",
            executable="field_planner_sim",
            name="field_planner",
            output="screen",
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
