import rospy
# Import the ROS message class under a different name
# to avoid confusion. We need it for the node state names.
from ros_bt_py_msgs.msg import Node as NodeMsg
# We need these to define a Node.
from ros_bt_py.node import Node, define_bt_node
from ros_bt_py.node_config import NodeConfig, OptionRef

@define_bt_node(NodeConfig(
    options={},
    inputs={
        'run_child_index': int
    },
    outputs={},
    max_children=4))

class ChildSelector(Node):

    def _do_setup(self):
        for child in self.children:
            child.setup()
    def _do_tick(self):
        return self.children[self.inputs['run_child_index']].tick()
    def _do_shutdown(self):
        for child in self.children:
            child.shutdown()
    def _do_reset(self):
        for child in self.children:
            child.reset()
        return NodeMsg.IDLE
    def _do_untick(self):
        for child in self.children:
            child.untick()
        return NodeMsg.IDLE