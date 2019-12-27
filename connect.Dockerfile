FROM confluentinc/cp-kafka-connect-base:5.3.2

RUN confluent-hub install --no-prompt debezium/debezium-connector-postgresql:1.0.0 \
    && confluent-hub install --no-prompt debezium/debezium-connector-mongodb:1.0.0 \
    && confluent-hub install --no-prompt confluentinc/kafka-connect-kinesis:1.1.4