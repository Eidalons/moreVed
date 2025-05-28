import requests
from time import sleep
import pytest
import subprocess

CONNECTION_ORDV_URL = 'http://localhost:8003'
BOAT_START_URL = "http://localhost:8001/start_boat"


route = [[10 , 15] , [48 , 9] , [70 , 32] , [69 , 68] , [34 , 99]]
payload = {"route" : route}


@pytest.fixture
def get_logs():
    def _get_logs(container_name):
        return subprocess.check_output(
            ['docker-compose', 'logs', '--no-color', container_name],
            text=True,
        )
    return _get_logs

@pytest.fixture
def init_route_to_orvd():
    response = requests.post(f'{CONNECTION_ORDV_URL}/route-check' , json = payload)
    return response

@pytest.fixture
def init_route_to_boat():
    response = requests.post(BOAT_START_URL , json = payload)
    return response

def test_ordv_confirm(init_route_to_orvd):
    response = init_route_to_orvd
    assert response.status_code == 200

def test_boat_route_transmission(init_route_to_boat):
    response = init_route_to_boat
    assert response.status_code == 200

def test_finish(get_logs):
    sleep(50)
    logs = get_logs('ckob')
    assert "ROUTE SUCCESSFULLY COMPLETED!" in logs