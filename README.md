# Lab 5: Distributed Data Processing with Mini-MapReduce on Amazon EMR

1. Project Overview
This project demonstrates the implementation of a distributed Word Count pipeline using the Hadoop MapReduce framework. The solution is deployed on Amazon EMR (Elastic MapReduce) and utilizes Hadoop Streaming to execute custom Python scripts for data transformation.

2. Dataset Information
Source: Simple English Wikipedia Text Dump

Repository: Dump-of-Simple-English-Wiki

Context: A condensed collection of Wikipedia articles designed for high-performance text processing tests.

3. System Architecture
The pipeline follows the standard MapReduce lifecycle: Input (Stored in HDFS) → Mapper (Python Logic) → Shuffle & Sort (Hadoop Framework) → Reducer (Python Logic) → Final Output (HDFS)

4. Component Breakdown
mapper.py
Function: Standardizes input text.

Logic: Reads lines from stdin, converts text to lowercase, removes non-alphanumeric characters, and outputs individual word tokens with a count of 1.

reducer.py
Function: Aggregates intermediate results.

Logic: Receives sorted key-value pairs from stdin, sums the occurrences for each unique word, and prints the final totals.

5. Prerequisites & Environment
AWS Academy Learner Lab Access.

An active Amazon EMR Cluster.

Secure Shell (SSH) client (e.g., Terminal, PuTTY).

vockey.pem private key for authentication.

6. Execution Guide
Step 1: Cluster Deployment
Initialize an EMR cluster with the following specifications:

Software: Hadoop (Core components).

Instances: 1 Primary (m4.large), 1-2 Core nodes (m4.large).

Security: Assign vockey key pair and default IAM roles (EMR_DefaultRole).

Tip: Disable S3 logging if encountering permission errors during initialization.

Step 2: Accessing the Primary Node
Connect to the cluster via SSH:

Bash
ssh -i labsuser.pem hadoop@<your-master-public-dns>
Step 3: Data Preparation & Ingestion
Fetch the dataset and move it into the distributed file system:

Bash
# Retrieve and extract data
wget https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/refs/heads/master/corpus.tgz
tar -xvzf corpus.tgz

# Move to HDFS
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put corpus.txt /user/hadoop/input/
Step 4: Code Deployment
Transfer your Python scripts from your local machine to the cluster:

Bash
scp -i labsuser.pem mapper.py reducer.py hadoop@<master-public-dns>:~/
# On the cluster, grant execution permissions:
chmod +x mapper.py reducer.py
7. Running the MapReduce Job
Execute the job using the Hadoop Streaming utility. Note: Generic options like -files must precede command options.

Bash
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -files mapper.py,reducer.py \
  -input /user/hadoop/input/ \
  -output /user/hadoop/output/wordcount \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py"
Monitoring & Validation
Track Job: yarn application -list

Inspect Results: hdfs dfs -cat /user/hadoop/output/wordcount/part-00000 | head -n 20

Analyze Performance: Use the time prefix before the hadoop command to measure execution duration.

8. Performance Experiment: Horizontal Scaling
To observe the benefits of parallelism, compare job runtimes by adjusting cluster size:

Baseline: Run the job with 2 Core Nodes and record the real time.

Scaling: Use the EMR Console to resize the Core group to 4 nodes.

Comparison: Re-run the job and compare the reduction in processing time.

9. Cleanup
To prevent unnecessary resource consumption and lab credit loss:

Remove HDFS directories: hdfs dfs -rm -r /user/hadoop/input /user/hadoop/output

Terminate the EMR Cluster via the AWS Management Console immediately after completion.

10. Key Learning Outcomes
Distributed Storage: Utilizing HDFS for large-scale data persistence.

Resource Management: Navigating the YARN ecosystem.

Scalability: Understanding how adding hardware improves throughput.

Fault Tolerance: Observing how Hadoop handles task distribution across a node cluster.
