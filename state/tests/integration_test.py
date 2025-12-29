import json
import pytest

from daemon_controller import DaemonController
from keyboard_input import InMemoryKeyboard

@pytest.fixture
def controller():
    controller = DaemonController(InMemoryKeyboard())
    with open(f"{controller.path}/daemon.json", "r+") as daemon:
        control_fields = json.load(daemon)
        control_fields["new_game"]["white"] = ""
        control_fields["new_game"]["black"] = ""
        daemon.seek(0)
        daemon.truncate()
        json.dump(control_fields, daemon)
    return controller

def test_new_game(controller: DaemonController):
    with open(f"{controller.path}/daemon.json", "r+") as daemon:
        control_fields = json.load(daemon)
        assert control_fields["new_game"]["white"] == ""
        assert control_fields["new_game"]["black"] == ""
    keyboard: InMemoryKeyboard = controller.keyboard
    keyboard.push_output("carol")
    keyboard.push_output("helena")
    controller.new_game()
    with open(f"{controller.path}/daemon.json", "r+") as daemon:
        control_fields = json.load(daemon)
        assert control_fields["new_game"]["white"] == "carol"
        assert control_fields["new_game"]["black"] == "helena"
