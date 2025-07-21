import pytest


def check_operation(id, details,polices) -> bool:
    """ Проверка возможности совершения обращения. """
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    opr: str = details.get("operation")

    if not all((src, dst, opr)):
        return False
    return {"src": src, "dst": dst, "opr": opr} in polices

@pytest.fixture
def polices():
    return (
    {"src": "communication", "dst": "crypto", "opr": "set_route"},
    {"src": "communication", "dst": "crypto", "opr": "emergency_stop"},
    {"src": "crypto", "dst": "message-processing", "opr": "set_route"},
    {"src": "crypto", "dst": "communication", "opr": "send_telemetry"},
    {"src": "crypto", "dst": "message-processing", "opr": "emergency_stop"},
    {"src": "crypto", "dst": "communication", "opr": "emergency_stop"},
    {"src": "message-processing", "dst": "movement-calculation", "opr": "set_route"},
    {"src": "message-processing", "dst": "route-control", "opr": "set_route"},
    {"src": "message-processing", "dst": "task-execution-control", "opr": "set_task"},
    {"src": "message-processing", "dst": "crypto", "opr": "send_telemetry"},
    {"src": "message-processing", "dst": "emergency-stop", "opr": "emergency_stop"},
    {"src": "message-processing", "dst": "crypto", "opr": "emergency_stop"},
    {"src": "telemetry-transmission", "dst": "message-processing", "opr": "send_telemetry"},
    {"src": "sensors", "dst": "telemetry-transmission", "opr": "send_sensors_data"},
    {"src": "task-execution-control", "dst": "sensors", "opr": "get_sample"},
    {"src": "complex", "dst": "route-control", "opr": "set_coords"},
    {"src": "complex", "dst": "task-execution-control", "opr": "set_coords"},
    {"src": "complex", "dst": "telemetry-transmission", "opr": "set_coords"},
    {"src": "gnss-navigation", "dst": "complex", "opr": "set_gnss_coords"},
    {"src": "internal-navigation", "dst": "complex", "opr": "set_internal_coords"},
    {"src": "internal-navigation", "dst": "complex", "opr": "set_internal_coords"},
    {"src": "battery-charge-control", "dst": "route-control", "opr": "set_battery"},
    {"src": "route-control", "dst": "emergency-stop", "opr": "emergency_stop"},
    {"src": "route-control", "dst": "emergency-stop", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "servo", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "message-processing", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "message-processing", "opr": "emergency_stop"},
    {"src": "movement-control", "dst": "servo", "opr": "move_to"},
    {"src": "movement-control", "dst": "route-control", "opr": "move_to"},
    {"src": "movement-calculation", "dst": "movement-control", "opr": "move_to"},
    {"src": "route-control" , "dst": "message-processing", "opr": "route_complete"},
    {"src": "message-processing" , "dst": "crypto", "opr": "route_complete"},
    {"src": "crypto" , "dst": "communication", "opr": "route_complete"}
)


@pytest.mark.parametrize("details, expected", [
    ({"source": "movement-control", "deliver_to": "route-control", "operation": "move_to"}, True),
    ({"source": "message-processing", "deliver_to": "crypto", "operation": "send_telemetry"}, True),
    ({"source": "internal-navigation", "deliver_to": "complex", "operation": "set_internal_coords"}, True),
])
def test_allowed_operations(details, expected, polices):
    assert check_operation("test_id", details, polices) == expected


@pytest.mark.parametrize("details, expected", [
    ({"source": "barometer", "deliver_to": "limiter", "operation": "invalid_op"}, False),
    ({"source": "invalid_src", "deliver_to": "complex", "operation": "current_coords_gps"}, False),
    ({"source": "gps", "deliver_to": "invalid_dst", "operation": "current_coords_gps"}, False),
])
def test_denied_operations(details, expected, polices):
    assert check_operation("test_id", details, polices) == expected


@pytest.mark.parametrize("details", [
    {"source": "task-execution-control", "deliver_to": "crypto"},  
    {"source": "battery-charge-control", "operation": "current_height"},
    {"deliver_to": "limiter", "operation": "current_height"},
    {},
])
def test_incomplete_details(details, polices):
    assert check_operation("test_id", details, polices) is False