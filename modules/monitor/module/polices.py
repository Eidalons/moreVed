policies = (
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
    {"src": "task-execution-control", "dst": "ensors", "opr": "get_sample"},
    {"src": "complex", "dst": "route-control", "opr": "set_coords"},
    {"src": "complex", "dst": "task-execution-control", "opr": "set_coords"},
    {"src": "complex", "dst": "telemetry-transmission", "opr": "set_coords"},
    {"src": "gnss-navigation", "dst": "complex", "opr": "set_gnss_coords"},
    {"src": "internal-navigation", "dst": "complex", "opr": "set_internal_coords"},
    {"src": "internal-navigation", "dst": "complex", "opr": "set_internal_coords"},
    {"src": "battery_charge_control", "dst": "route-control", "opr": "set_battery"},
    {"src": "route_control", "dst": "emergency-stop", "opr": "emergency_stop"},
    {"src": "route_control", "dst": "emergency-stop", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "servo", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "message-processing", "opr": "emergency_stop"},
    {"src": "emergency-stop", "dst": "message-processing", "opr": "emergency_stop"},
    {"src": "movement-control", "dst": "servo", "opr": "move_to"},
    {"src": "movement-control", "dst": "route-control", "opr": "move_to"},
    {"src": "movement-calculation", "dst": "route-control", "opr": "move_to"},
 
)

def check_operation(id, details) -> bool:
    """ Проверка возможности совершения обращения. """
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    opr: str = details.get("operation")

    if not all((src, dst, opr)):
        return False

    print(f"[info] checking policies for event {id},  {src}->{dst}: {opr}")

    return {"src": src, "dst": dst, "opr": opr} in policies