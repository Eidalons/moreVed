import requests
import time
import subprocess

CONNECTION_ORDV_URL = 'http://0.0.0.0:8003'
CONNECTION_BOAT_URL = 'http://0.0.0.0:8001'


route = [[10 , 15] , [48 , 9] , [70 , 32] , [69 , 68] , [34 , 99]]
test_route_json = {"route" : route}





def test_container_output(app_name):
    logs = subprocess.check_output(
        ['docker-compose', 'logs', '--no-color', app_name],
        text=True
    )
    return logs


def test_fuctionality():
    ckob_logs = test_container_output('ckob')
    orvd_logs = test_container_output('orvd')
    boat_logs = test_container_output('boat')
    send_route_to_ordv = requests.post(f'{CONNECTION_ORDV_URL}/confirm_route' , json = test_route_json)
    assert ((send_route_to_ordv.json()).get("confirm") == "YES" or (send_route_to_ordv.json()).get("confirm") == "NO") and send_route_to_ordv.status_code == 200
    send_route_to_boat = requests.post(f'{CONNECTION_BOAT_URL}/start_route' , json=test_route_json)
    assert (send_route_to_boat.json()).get("status") == "route started" and send_route_to_boat.status_code == 200
    for i in range(len(route)):
        print(f"Moving to next coordinate, current x , y  {str(route[i][0])}    {str(route[i][1])}")
    time.sleep(45)
    for i in range(len(route)):
        #assert (f"Moving to next coordinate, current x , y  {int(10)}    {int(15)}") in boat_logs
        #assert (f"Moving to next coordinate, current x , y  {int(10)}     {int(15)}") in boat_logs
        #assert (f"Moving to next coordinate, current x , y  {route[i][0]}     {route[i][1]}") in boat_logs
        assert 'Moving to next coordinate, current x , y  34     99' in boat_logs
        assert '[boat] send current coordinate to orvd' in boat_logs
        assert "[orvd] receive current coordinates" in orvd_logs
        assert "[ckob] receive current coordinates from boat" in ckob_logs
        assert "ckob answer {'status': 'got coordinates and data from sensors'}" in boat_logs
        assert "ordv answer :  {'status': 'OK , keep moving'}" in boat_logs
    assert 'route_complete!' in boat_logs

if __name__ == "__main__":
    test_fuctionality()