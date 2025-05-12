SHELL := bash

MODULES := monitor \
           communication \
		   crypto \
		   battery-charge-control \
		   complex \
		   emergency-stop \
		   gnss-navigation \
		   internal-navigation \
		   message-processing \
		   movement-calculation \
		   movement-control \
		   route-control \
		   sensors \
		   servo \
		   task-execution-control \
		   telemetry-transmission \

SLEEP_TIME := 20

all:
	docker-compose up --build -d
	sleep ${SLEEP_TIME}

	for MODULE in ${MODULES}; do \
		echo Creating $${MODULE} topic; \
		docker exec broker \
			kafka-topics --create --if-not-exists \
			--topic $${MODULE} \
			--bootstrap-server localhost:9092 \
			--replication-factor 1 \
			--partitions 1; \
	done

clean:
	docker-compose down

logs:
	docker-compose logs -f --tail 100
