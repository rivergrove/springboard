## Summary
We use Docker to implement a kafka producer stream of transactions, which are filtered into fraudulent and legitimate transactions topics.

### Kafka Producer Stream
After running `docker-compose -f docker-compose.kafka.yml up` in order to start up the cluster, we run `docker-compose up` to generate dummy transactions.

We can see these transactions hitting our consumer by running `docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.transactions --from-beginning`

### Filtering to Fraud and Legitimate Transactions

We can now run `docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer\n--bootstrap-server localhost:9092 --topic streaming.transactions.legit` to get legitimate transactions.

![legit](https://github.com/rivergrove/springboard/blob/master/mini-projects/kafka/kafka_mini_project/screenshots/legit_transactions.png)

And we run `docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer\n--bootstrap-server localhost:9092 --topic streaming.transactions.fraud` to get fraudulent transactions.

![fraud](https://github.com/rivergrove/springboard/blob/master/mini-projects/kafka/kafka_mini_project/screenshots/fraud_transactions.png)


