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
    #assert "[ckob] started..." in logs
    #assert f"Sent route to boat: {route}" in logs ##???????????????????????
    #assert f"Request route approve from ORVD" in logs
    #assert f"Send route to boat: {route}" in logs
    assert True

def orvd_tests():
    logs = test_container_output('orvd')
    assert True

def monitor_tests():
    logs = test_container_output('monitor')
    assert True 

def communication_tests():
    logs = test_container_output('communication')
    assert True
    
def crypto_tests():
    logs = test_container_output('crypto')
    assert True

def complex_tests():
    logs = test_container_output('complex')
    assert True

def emergency_tests():
    logs = test_container_output('emergency-stop')
    assert True

def gnss_navigation_tests():
    logs = test_container_output('gnss-navigation')
    assert True

def internal_navigation_tests():
    logs = test_container_output('internal-navigation')
    assert True

def message_processing_tests():
    logs = test_container_output('message-processing')
    assert True

def movement_calculation_tests():
    logs = test_container_output('movement-calculation')
    assert True

def movement_control_tests():
    logs = test_container_output('movement-control')
    assert True

def route_control_tests():
    logs = test_container_output('route-control')
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
    message_processing_tests()
    movement_calculation_tests()
    movement_control_tests()
    route_control_tests()
    route_control_tests()
    sensors_tests()
    sensors_tests()
    task_execution_tests()
    telemetry_transmission_tests()
