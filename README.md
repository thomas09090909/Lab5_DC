# Lab 5: Distributed Data Analysis using Mini-MapReduce on Amazon EMR

## 1. Executive Summary
This laboratory project focuses on deploying a distributed Word Count application using the **Hadoop MapReduce** framework. By leveraging **Amazon EMR (Elastic MapReduce)** and **Hadoop Streaming**, the project processes a large-scale Wikipedia dataset using custom Python logic to demonstrate the power of cloud-based parallel computing.

## 2. Dataset Specifications
* **Source:** Simple English Wikipedia Text Corpus.
* **Dataset URL:** [Simple English Wiki Dump](https://github.com/LGDoor/Dump-of-Simple-English-Wiki).
* **Content:** A curated collection of Wikipedia articles formatted for big data processing experiments.

## 3. System Architecture
The pipeline utilizes a standard distributed processing flow:
**Input (HDFS)** ⮕ **Mapper (Python)** ⮕ **Shuffle & Sort (Hadoop)** ⮕ **Reducer (Python)** ⮕ **Output (HDFS)**



## 4. Script Functionality

### `mapper.py`
* **Role:** Data Transformation & Tokenization.
* **Process:** Standardizes input by converting text to lowercase, filtering for alphanumeric characters, and emitting intermediate key-value pairs `(word, 1)`.

### `reducer.py`
* **Role:** Data Aggregation.
* **Process:** Accepts sorted key-value pairs from the Hadoop framework and calculates the total occurrences for each unique word.

## 5. Prerequisites
* Active AWS Academy Learner Lab environment.
* Configured Amazon EMR Cluster.
* SSH client access with `vockey.pem` (or `labsuser.pem`) credentials.

---

## 6. Deployment Guide

### Phase 1: Cluster Initialization
1.  Navigate to **Amazon EMR** in the AWS Console.
2.  Launch a cluster using **m4.large** instances (1 Primary, 2 Core).
3.  Ensure the **Hadoop** application bundle is selected.
4.  **Note:** Disable "Cluster-specific logs to S3" if encountering permission issues in the Learner Lab.

### Phase 2: Connecting to the Environment
Locate your Master Node's Public DNS and connect via terminal:
```bash
ssh -i labsuser.pem hadoop@<your-master-public-dns>

Phase 3: Data Ingestion (Local to HDFS)
Prepare the distributed file system for processing:

Bash
# Download and unzip the corpus
wget [https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/refs/heads/master/corpus.tgz](https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/refs/heads/master/corpus.tgz)
tar -xvzf corpus.tgz

# Initialize HDFS directories and upload data
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put corpus.txt /user/hadoop/input/
Phase 4: Deploying Scripts
From your local machine, transfer the logic files to the Master Node:

Bash
scp -i labsuser.pem mapper.py reducer.py hadoop@<your-master-public-dns>:~/
On the Master Node terminal, enable execution:

Bash
chmod +x mapper.py reducer.py
7. Execution and Monitoring
Running the Job
Execute the MapReduce job using the Hadoop Streaming jar. Ensure -files is placed before the input/output arguments:

Bash
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -files mapper.py,reducer.py \
  -input /user/hadoop/input/ \
  -output /user/hadoop/output/wordcount_results \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py"
Verification
Once the job reaches 100% completion, inspect the output:

Bash
# View result files
hdfs dfs -ls /user/hadoop/output/wordcount_results/

# Display top 20 lines of results
hdfs dfs -cat /user/hadoop/output/wordcount_results/part-00000 | head -n 20
8. Performance Experiment: Horizontal Scaling
A core requirement of this lab is analyzing the impact of cluster size on processing speed.

Baseline Run: Execute the job using 2 Core Nodes. Use the time command to capture the "real" execution duration.

Scale Out: Through the EMR Console, increase the Core Instance Group to 4 nodes.

Experimental Run: Execute the job again with a new output path and compare the reduction in processing time.

9. Resource Management (Cleanup)
To preserve AWS credits, perform the following after data verification:

Clear HDFS data: hdfs dfs -rm -r /user/hadoop/input /user/hadoop/output

Terminate the EMR Cluster immediately via the Management Console.

10. Concepts Demonstrated
HDFS Implementation: Practical use of distributed storage.

Parallel Computing: Vertical vs. Horizontal scaling analysis.

Fault Tolerance: Understanding the framework's ability to redistribute tasks.

YARN Resource Management: Monitoring application lifecycles in a cluster.
