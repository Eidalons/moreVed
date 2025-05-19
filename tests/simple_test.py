import requests
import time
import subprocess

CONNECTION_ORDV_URL = 'http://localhost:8003'
CONNECTION_BOAT_URL = 'http://communication:8002'


route = [[10 , 15] , [48 , 9] , [70 , 32] , [69 , 68] , [34 , 99]]
test_route_json = {"route" : route}


def test_container_output(app_name):
    logs = subprocess.check_output(
        ['docker-compose', 'logs', '--no-color', app_name],
        text=True
    )
    return logs


def init_test():
    send_route_to_ordv = requests.post(f'{CONNECTION_ORDV_URL}/route-check' , json = test_route_json)
    assert ((send_route_to_ordv.json()).get("route_approve") == True or (send_route_to_ordv.json()).get("route_approve") == False) and send_route_to_ordv.status_code == 200
    send_route_to_boat = requests.post(f'{CONNECTION_BOAT_URL}/start_boat' , json=test_route_json)
    assert send_route_to_boat.json().get("status") == "route accepted" and send_route_to_boat.status_code == 200
    time.sleep(25)

def ckob_tests():
    logs = test_container_output('ckob')
    assert "[ckob] started..." in logs
    assert f"Sent route to boat: {route}" in logs ##???????????????????????
    assert f"Request route approve from ORVD" in logs
    assert f"Send route to boat: {route}" in logs
    assert f"Boat data log: boat_pos:" in logs

def orvd_tests():
    logs = test_container_output('orvd')
    assert "[orvd] started..." in logs
    assert f"Requested route approve: {route}" in logs
    assert "Boat current pos log:" in logs

def monitor_tests():
    logs = test_container_output('monitor')
    assert '[DEBUG] monitor started...'
    assert "[monitor] started..." in logs
    assert "Running monitor_consumer..." in logs
    assert "Running monitor_producer..." in logs
    assert "[info] handling event" in logs
    assert "monitor_consumer started" in logs
    assert "monitor_producer started" in logs
    assert "[info] checking policies for event" in logs

def communication_tests():
    logs = test_container_output('communication')
    assert 'Running communication_web...' in logs
    assert 'Running communication_consumer...' in logs
    assert 'Running communication_producer...' in logs
    assert f"Requested boat start with route: {route}" in logs
    assert "[info] handling event" in logs
    assert "[message_processing] send telemetry telemetry" in logs
    assert 'communication_consumer started' in logs
    assert 'communication_producer started' in logs

def crypto_tests():
    logs = test_container_output('crypto')
    assert '[DEBUG] crypto started...' in logs
    assert 'Running crypto_consumer...' in logs
    assert 'Running crypto_producer...' in logs
    assert "[CRYPTO] route confirmed!" in logs
    assert "[CRYPTO] send telemetry to crypto" in logs
    assert "[CRYPTO] message encrypted" in logs
    assert "[CRYTO] accepted new possible route , checking ......" in logs
    assert "[CRYPTO] send encrypted telemetry to communication" in logs
    assert "[info] handling event" in logs
    assert "crypto_consumer started" in logs
    assert "crypto_producer started" in logs
    

def complex_tests():
    logs = test_container_output('complex')
    assert '[DEBUG] complex started...' in logs
    assert 'Running complex_consumer...' in logs
    assert 'Running complex_producer...' in logs
    assert "[COMPLEX_DEBUG] Set coords:" in logs
    assert "[info] handling event" in logs
    

def emergency_tests():
    logs = test_container_output('emergency-stop')
    

def gnss_navigation_tests():
    logs = test_container_output('gnss-navigation')
    assert '[DEBUG] gnss-navigation started...' in logs
    assert 'Running gnss-navigation_producer...' in logs
    assert "[GNSS_DEBUG] Readed coords:" in logs
    

def internal_navigation_tests():
    logs = test_container_output('internal-navigation')
    assert '[DEBUG] internal-navigation started...' in logs
    assert 'Running internal-navigation_producer...' in logs
    assert "[GNSS_DEBUG] Readed coords:" in logs
    

def message_processing_tests():
    logs = test_container_output('message-processing')
    assert '[DEBUG] message-processing started...' in logs
    assert 'Running message-processing_consumer...' in logs
    assert 'Running message-processing_producer...' in logs
    assert "[MESSAGE PROCCESING] send telemetry to crypto" in logs
    assert "[MESSAGE PROCCESING] send request to stop boat" in logs
    

def movement_calculation_tests():
    logs = test_container_output('movement-calculation')
    assert '[DEBUG] movement-calculation started...' in logs
    assert 'Running movement-calculation_consumer...' in logs
    assert 'Running movement-calculation_producer...' in logs
    assert "[info] handling event" in logs
    assert 'movement-calculation_consumer started' in logs
    

def movement_control_tests():
    logs = test_container_output('movement-control')
    assert '[DEBUG] movement-control started...' in logs
    assert 'Running movement-control_consumer...' in logs
    assert 'Running movement-control_producer...' in logs
    assert 'movement confirmed!' in logs
    assert "[info] handling event" in logs

def route_control_tests():
    logs = test_container_output('route-control')
    assert '[DEBUG] route-control started...' in logs
    assert 'Running route-control_consumer...' in logs
    assert 'Running route-control_producer...' in logs
    assert "[ROUTE CONTROL] current battery health" in logs
    assert True

def sensors_tests():
    logs = test_container_output('sensors')
    assert True

def servo_tests():
    logs = test_container_output('servo')
    assert True

def task_execution_tests():
    logs = test_container_output('task-execution-control')
    assert True

def telemetry_transmission_tests():
    logs = test_container_output('telemetry-transmission')
    assert True


if __name__ == "__main__":
    #init_test()
    ckob_tests()
    orvd_tests()
    monitor_tests()
    communication_tests()
    crypto_tests()
    complex_tests()
    emergency_tests()
    gnss_navigation_tests()
    internal_navigation_tests()
    gnss_navigation_tests()
    message_processing_tests()
    movement_calculation_tests()
    movement_control_tests()
    route_control_tests()
    route_control_tests()
    sensors_tests()
    sensors_tests()
    task_execution_tests()
    telemetry_transmission_tests()
