# moreVed


## Disclaimer 

This is a demo project and shall not be used in production.


## Purpose

This is an example of a unmanned watercraft by using "Security monitor" pattern: all cross-services requests go through the Monitor service.
The Monitor checks whether particular request is authorized and valid, then delivers it to destination service or drops it without further processing.

## Running the demo

There are two main options for running the demo:
- local (using local development environment), then there shall be installed python (tested with version 3.8), also having *make* tool is recommended
- containerized (using docker containers)

In any case there shall be docker-compose locally available - at least for running message broker (Kafka).

### Running complete demo in containerized mode

execute in VS Code terminal window either
- _make run_

then wait about 1 minute. Open the requests.rest file in Visual Studio Code editor. If you have the REST client extension installed, you will see 'Send request' active text above GET ,you can click on it.

If you click on the application GET link, you shall see in the Response window (will open automatically) the following:

```
HTTP/1.1 200 OK
Server: Werkzeug/3.0.6 Python/3.8.20
Date: Mon, 19 May 2025 09:14:00 GMT
Content-Type: application/json
Content-Length: 33
Connection: close

{
  "status": "CKOB started moving"
}
```
 This is expected behavior.

after this message execute
- _make logs_

and see the imitate of boat moving

## Tests
- To run test execute _make test_ or _pytest -sv_ when system is running (expect that required packages were installed)

#### Troubleshooting

- if kafka or zookeeper containers don't start, make sure you don't have containers with the same name. If you do, remove the old containers and run the demo again.
- to run test and _make all_ scenario you need manually install pipenv
- if after _make all_ you see output like this: [Building wheel for confluent-kafka (pyproject.toml): started
  Building wheel for confluent-kafka (pyproject.toml): finished with status 'error'
Failed to build confluent-kafka] try to install librdkafka package. Then try _make all_ again
