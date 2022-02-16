# kafka installation

    # untar kafka binaries downloaded from internet
    tar -xvf kafka_2.13-3.1.0.tgz
    # navigate to kafka folder
    cd kafka_2.13-3.1.0
    # alternative way to install using brew
    brew install kafka

# make permenant directories for data    
mkdir data
mkdir data/zookeeper
mkdir data/kafka
# set properties
subl config/zookeeper.properties
# set dataDir=/Users/anthonyolund/kafka_2.13-3.1.0/data/zookeeper
subl config/server.properties
# set log.dirs=/Users/anthonyolund/kafka_2.13-3.1.0/data/kafka

# before using kafka we must always start zookeeper and kafka on 2 seperate terminal windows
zookeeper-server-start config/zookeeper.properties
kafka-server-start config/server.properties

# create a topic
kafka-topics --bootstrap-server localhost:9092 --topic first_topic --create --partitions 3 --replication-factor 1
# list topics 
kafka-topics --bootstrap-server localhost:9092 --list
# describe a topic
kafka-topics --bootstrap-server localhost:9092 first_topic --describe
# delete a topic
kafka-topics --bootstrap-server localhost:9092 --topic second_topic --delete

# producers

    # make a topic a producer
    kafka-console-producer --broker-list localhost:9092 --topic first_topic
    # add acks property
    kafka-console-producer --broker-list localhost:9092 --topic first_topic --producer-property acks=all
    # makes a topic if it does not already exist with default parameters as defined in server.properties file
    kafka-console-producer --broker-list localhost:9092 --topic new_topic

    # change default number of parititions to 3
    # num.partitions=3
    subl config/server.properties

# consumers

    # consumer basics

        # start a consumer listening for new messages. 
        # as new messages are written, they will appear in the terminal.
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic
        # see all messages in a topic
        # note that order is only guarenteed by partition
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --from-beginning

    # consumer group mode

        # topic as part of a group
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-first-app
        # if we run the same command from another terminal window, new messages will be split
        # between the two consumer windows because they have the same group 
        # each consumer will read from a different partition
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-first-app
        # if we run the same command with a new group from beginning we get all messages as expected
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-second-app --from-beginning
        # but if we run the same command again, we get no results
        # because we have the same group name and that group has already read from beginning, 
        # the --from-beginning tag is no longer taken into account
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-second-app --from-beginning
        # if we cancel out of listening mode, write some messages from a producer on the same topic,
        # and then run the same command for the third time, it will show those new messages, 
        # because again, we specified the group name
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-second-app --from-beginning
        # list all consumer groups
        kafka-consumer-groups --bootstrap-server localhost:9092 --list
        # describe a consumer group
        # output: GROUP TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG CONSUMER-ID HOST CLIENT-ID
        # lag = 0 means that we have read all the data on that partition 
        kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-second-app
        # how do I make my consumer group replay data?
        # by using the --reset-offsets tag
        # you have the option of resetting the offsets: --to-datetime, --by-period, --to-earliest, 
        # --to-latest, --shift-by, --from-file, --to-current
        kafka-consumer-groups --bootstrap-server localhost:9092 --group my-second-app --reset-offsets --to-earliest --execute --topic first_topic
        # when we restart our consumer we will see all of the data
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-second-app --from-beginning
        # shift backward to n number of offsets per partition
        kafka-consumer-groups --bootstrap-server localhost:9092 --group my-second-app --reset-offsets --shift-by -2 --execute --topic first_topic
        # now we see 6 messages, 2 per each of the 3 partitions
        kafka-console-consumer --bootstrap-server localhost:9092 --topic first_topic --group my-second-app

# twitter

    # create kafka topic before running java script
    kafka-topics --bootstrap-server localhost:9092 --create --topic twitter_tweets --partitions 6 --replication-factor 1
    # launch a kafka console consumer
    kafka-console-consumer --bootstrap-server localhost:9092 --topic twitter_tweets

# topic configuration

    # create topic
    kafka-topics --bootstrap-server localhost:9092 --topic configured_topic --create --partitions 3 --replication-factor 1
    # describe configuration
    kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name configured_topic --describe
    # change min.insync.replicas to 2
    kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name configured_topic --add-config min.insync.replicas=2 --alter
    # delete configuration
    kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name configured_topic --delete-config min.insync.replicas --alter

# log compaction

    # cleanup.policy=compact to enable log compaction, min.cleanable.dirty.ratio=0.001 to ensure log compaction happens all the time, segment.ms=5000 to make compaction happen every 5 seconds
    kafka-topics --bootstrap-server localhost:9092 --create --topic employee-salary --partitions 1 --replication-factor 1 --config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.001 --config segment.ms=5000
    # describe newly created topic
    kafka-topics --bootstrap-server localhost:9092 --describe --topic employee-salary
    # start console consumer
    kafka-console-consumer --bootstrap-server localhost:9092 --topic employee-salary --from-beginning --property print.key=true --property key.separator=,
    # create producer
    kafka-console-producer --broker-list localhost:9092 --topic employee-salary --property parse.key=true --property key.separator=,

# min.insync.replicas

    # create a topic
    kafka-topics --bootstrap-server localhost:9092 --topic highly-durable --create --partitions 3 --replication-factor 1
    # update config
    kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name highly-durable --alter --add-config min.insync.replicas=2

# run multiple brokers

    # go to config directory
    cd config
    # create 3 more brokers
    cp server.properties server0.properties
    cp server.properties server1.properties
    cp server.properties server2.properties
    # edit new brokers
        # edit broker_id=1
        # edit log.dirs=/Users/anthonyolund/kafka_2.13-3.1.0/data/kafka1
        # uncomment and edit listeners=PLAINTEXT://:9093
        # do the same steps above with server2
        subl server1.properties
        subl server2.properties
    # make kafka1 and kafka2 directories
    cd /Users/anthonyolund/kafka_2.13-3.1.0/data/
    mkdir kafka1
    mkdir kafka2
    # run all brokers in seperate windows after starting zookeeper
    kafka-server-start config/server0.properties
    kafka-server-start config/server1.properties
    kafka-server-start config/server2.properties

    # create topic
    kafka-topics --bootstrap-server localhost:9092 --topic many-reps --create --partitions 6 --replication-factor 3
    # describe. We see that the leader is on different brokers
    kafka-topics --bootstrap-server localhost:9092 --topic many-reps --describe
    # make producer on all 3 brokers. Type messages.
    kafka-console-producer --broker-list localhost:9092,localhost:9093,localhost:9094 --topic many-reps
    # same producer but only to 1 broker. Type messages.
    kafka-console-producer --broker-list localhost:9094 --topic many-reps
    # connect to consumer and read from beginning
    kafka-console-consumer --bootstrap-server localhost:9093 --topic many-reps --from-beginning

