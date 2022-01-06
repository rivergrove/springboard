## Steps

1. Create a hadoop environment if not already installed. I following the instructions in the [following video](https://www.youtube.com/watch?v=BdHQFAP98_A&t=202s).
2. Add the data.csv file to hdfs using the following command: `hdfs dfs -put data.csv /user/input/`
3. Execute the following commands to run the python scripts on hadoop: 
`hadoop jar /Users/anthonyolund/myhadoop/hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
-file mapper1.py -mapper mapper1.py \
-file reduce1.py -reducer reduce1.py \
-input /user/input/data.csv -output /user/output/output1
hadoop jar /Users/anthonyolund/myhadoop/hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
-file mapper2.py -mapper mapper2.py \
-file reduce2.py -reducer reduce2.py \
-input /user/output/output1 -output /user/output/output2`
4. View the final output using the following command: `hdfs dfs -cat /user/output/output2/part-00000`

