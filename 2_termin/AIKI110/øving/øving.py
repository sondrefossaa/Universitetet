import rlcpy
from rlcpy.node import Node
from std_msgs.msg import String
from exam import process_data


class Test(Node):
    def __init__(self) -> None:
        super().__init__("data_node")
        self.publisher_ = self.create_publisher(String, "kanal_A", 10)
        self.subscriber_ = self.create_subscriber(
            String, "kanal_B", self.callback_function, 10
        )

    def callback_function(self, msg):
        data = msg.data
        resultat = process_data(data)
        ny_melding = String()
        ny_melding.data = resultat
        self.publisher_(ny_melding)
