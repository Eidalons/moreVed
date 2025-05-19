import requests
import time
import subprocess

CONNECTION_ORDV_URL = 'http://localhost:8003'
CONNECTION_BOAT_URL = 'http://communication:8004'


route = [[10 , 15] , [48 , 9] , [70 , 32] , [69 , 68] , [34 , 99]]
test_route_json = {"route" : route}

def get_docker_logs_once():
    """Возвращает все текущие логи docker-compose (одно чтение, без -f)."""
    cmd = ["docker-compose", "logs", "--tail", "100"]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Возвращает строку вместо bytes
    )
    if result.returncode != 0:
        print("Ошибка:", result.stderr)
        return None
    return result.stdout


def test_container_output(app_name):
    logs = subprocess.check_output(
        ['docker-compose', 'logs', '--no-color', app_name],
        text=True
    )
    return logs


def func_tests():
    send_route_to_ordv = requests.post(f'{CONNECTION_ORDV_URL}/route-check' , json = test_route_json)
    assert ((send_route_to_ordv.json()).get("route_approve") == True or (send_route_to_ordv.json()).get("route_approve") == False) and send_route_to_ordv.status_code == 200
    send_route_to_boat = requests.post(f'{CONNECTION_BOAT_URL}/start_boat' , json=test_route_json)
    assert send_route_to_boat.json().get("status") == "route accepted" and send_route_to_boat.status_code == 200
    logs = get_docker_logs_once()
    print(logs)
    
    assert True

    





if __name__ == "__main__":
    func_tests()
    
