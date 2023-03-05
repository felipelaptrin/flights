test:
	docker build -t flight-crawler .
	docker network create mybridge

	docker container run -d --rm --name flight-crawler \
		-e RUN_LOCALLY_WITH_HEADER='FALSE' \
		-e CLUSTER_ID \
		-e DB_USER \
		-e DB_PASSWORD \
		-e DB_NAME \
		-e DB_CLUSTER \
		-e DB_COLLECTION \
		-e LOGGER_LEVEL \
		--network mybridge \
		flight-crawler
	sleep 2
	docker container run --name run-crawler --network mybridge curlimages/curl:7.88.1 "http://flight-crawler:8080/2015-03-31/functions/function/invocations" \
		-d "{\"departureDateOrigin\":\"10/09/2023\",\"departureDateDestination\":\"25/09/2023\",\"origin\":\"Boston\",\"destination\":\"Asia\",\"minStayDays\":5,\"maxStayDays\":7,\"isGenericDestination\":true}"
	@docker logs flight-crawler --tail 30
	@docker rm -f flight-crawler run-crawler
	@docker network rm mybridge