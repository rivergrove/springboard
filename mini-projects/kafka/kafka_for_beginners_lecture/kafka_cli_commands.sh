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
kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --create --partitions 3 --replication-factor 1
# list topics 
kafka-topics.sh --bootstrap-server localhost:9092 --list
# describe a topic
kafka-topics.sh --bootstrap-server localhost:9092 --list first_topic --describe
# delete a topic
kafka-topics --bootstrap-server localhost:9092 --topic second_topic --delete
# make a topic a producer
kafka-console-producer --broker-list localhost:9092 --topic first_topic
# add acks property
kafka-console-producer --broker-list localhost:9092 --topic first_topic --producer-property acks=all
# makes a topic if it does not already exist with default parameters as defined in server.properties file
kafka-console-producer --broker-list localhost:9092 --topic new_topic

# change default number of parititions to 3
# num.partitions=3
subl config/server.properties