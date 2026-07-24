from typing import Dict, Optional, Tuple, Any
import asyncio

import rclpy
import tf2_ros
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.node import Node
from tf2_ros import TransformException


class Nav2APINode(Node):
    def __init__(self) -> None:
        super().__init__("nav2_api_node")

        self.action_client = ActionClient(self, NavigateToPose, f"/navigate_to_pose")
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.goal_handle = None

    @staticmethod
    async def await_rclpy_future(ros_future) -> Any:
        loop = asyncio.get_running_loop()
        asyncio_future = loop.create_future()

        def complete(future):
            try:
                value = future.result()
            except Exception as exc:
                def set_exception():
                    if not asyncio_future.done():
                        asyncio_future.set_exception(exc)

                loop.call_soon_threadsafe(set_exception)
            else:
                def set_result():
                    if not asyncio_future.done():
                        asyncio_future.set_result(value)

                loop.call_soon_threadsafe(set_result)
        
        ros_future.add_done_callback(complete)
        return await asyncio_future

    async def send_goal(self, pose: Dict[str, float]) -> Tuple[bool, str]:
        if not self.action_client.server_is_ready():
            return False, "アクションサーバーが利用できません"

        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = "map"
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        goal.pose.pose.position.x = float(pose["x"])
        goal.pose.pose.position.y = float(pose["y"])
        goal.pose.pose.position.z = float(pose["z"])

        goal.pose.pose.orientation.x = float(pose["qx"])
        goal.pose.pose.orientation.y = float(pose["qy"])
        goal.pose.pose.orientation.z = float(pose["qz"])
        goal.pose.pose.orientation.w = float(pose["qw"])

        self.goal_handle = await self.await_rclpy_future(
            self.action_client.send_goal_async(goal)
        )
        self.get_logger().info(f"ゴール送信: {pose}")

        if not self.goal_handle.accepted:
            self.goal_handle = None
            return False, "ゴールが拒否されました"

        result = await self.await_rclpy_future(
            self.goal_handle.get_result_async()
        )
        self.goal_handle = None

        if result.status == GoalStatus.STATUS_SUCCEEDED:
            return True, "ナビゲーションに成功しました"

        if result.status == GoalStatus.STATUS_CANCELED:
            return False, "ナビゲーションを中断しました"

        return False, "ナビゲーションに失敗しました"

    async def cancel_goal(self) -> Tuple[bool, str]:
        if self.goal_handle is None:
            return False, "キャンセル対象のゴールがありません"

        response = await self.await_rclpy_future(
            self.goal_handle.cancel_goal_async()
        )

        if response.goals_canceling:
            return True, "ナビゲーションの中断を要求しました"

        return False, "ナビゲーション中断に失敗しました"

    def get_current_pose(self) -> Optional[Dict[str, float]]:
        try:
            transform = self.tf_buffer.lookup_transform(
                "map",
                "base_link",
                rclpy.time.Time(),
                timeout=Duration(seconds=1),
            )
        except TransformException:
            return None

        position = transform.transform.translation
        orientation = transform.transform.rotation

        return {
            "x": position.x,
            "y": position.y,
            "z": position.z,
            "qx": orientation.x,
            "qy": orientation.y,
            "qz": orientation.z,
            "qw": orientation.w,
        }