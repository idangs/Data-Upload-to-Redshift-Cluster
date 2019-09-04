<h1>Data Uploader to Redshift Cluster</h1>

<p>This project contains a program that uploads files to the Amazon Redshift Cluster. This program allows the user to upload one or multiple files to the cluster and stores each file as a table in the database. This is useful for those who want to automate uploading files to redshift.</p>

Note that in order to use this project, you need to create a redshift cluster first.


<h2> Installation </h2>

To install this program, clone the repository.


<h2> Dependencies </h2>

This program depends on:
<ul>
<li>Python 2.7.x or higher</li>
<li>pip</li>
<li>boto3</li>
<li>psycopg2</li>
<li>requests</li>
</ul>

If you do not have pip installed on your platform, follow the installation instructions [here](https://pip.pypa.io/en/latest/installing.html#install-or-upgrade-pip). Alternatively, you can install [Anaconda](https://www.continuum.io/downloads).

<b>To install boto3:</b>
Sudo pip install boto3

<b>To install boto3:</b>
pip install psycopg2

<b>To install requests:</b>
pip install requests

<h2>Optional</h2>

Although the program has an option for entering your access id, and secret id of your aws console, the following can be an additional step that can be followed to save your aws credentials. As a result of this, you do not need need enter your access key and secret id in the program itself.

<h3>AWS Credentials</h3>

To be able to connect to your AWS account, you need to add your AWS credentials.
1.	Go to AWS IAM Console.
2.	Create a new user or use an existing user.
3.	Generate a new set of keys for the user.
4.	Create a file named credentials in the directory ~/.aws/ (Create ~/.aws/ if it's not already there).
5.	Put the following in credentials file:

```
aws_access_key_id = YOUR_ACCESS_KEY
```

```
aws_secret_access_key = YOUR_SECRET_KEY
```

<h2>Updates</h2>

You should occasionally execute git pull origin master to ensure that you're using the latest version of the program.

<h2>Usage</h2>

The program contains two required arguments.

<h3>Required arguments</h3>
<ul>
<li><b>Local Directory</b> is the path to the local directory which contains the local files to be transferred.</li>
<li><b>Bucket Name</b> is the name of the destination S3 bucket. Please ensure that this name is unique and has not been used for other S3 buckets in your aws console.</li></ul>


<h3>Optional arguments</h3>
<ul>
<li><b>File extension </b> is the extensions of the files in Local Directory that need to be transfered. Extensions should be separated by ',' only. If FILES_EXTENSION is not specified, all files in the directory are uploaded (except files whose names start with '.'). Although all file types will be uploaded to the S3 bucket, this program is meant for uploading files with csv format.</li>
</ul>


<h2>Running the program</h2>

<h3>Execute:</h3>

```
uploader Local_directory  Bucket_name -ext File_extension
```

<h3>Example:</h3>

```
python uploader.py "/Users/folder " "vital-signs" -ext "csv"
```

<h2>Other information</h2>

<h3> Downloading coursera files</h3>

<p>You can use the project [Coursera scheduled exports](https://github.com/LU-C4i/coursera-scheduled-exports) to request data exports for one or multiple courses and download them with a single command. Note that only data coordinators can currently use this program, as it requests full exports including partner-level ids and clickstream data.

In your specified location, Coursera scheduled exports will create a folder, with multiple subfolders for each course_slug containing all the course files. If you are interested in uploading multiple folders to the redshift using Data Uploader to Redshift Cluster, merging all the subfolders is required. This is becasue the program uploads files from one folder only; subfolders are ignored.

To merge all the subfolders use the [merge.py]() program, included in this repository. 

<h3>Merging subfolders into one folder</h3>

<p> The program [merge.py]() contains two required arguments.</p>

<h4>Required arguments</h4>
<ul>
<li><b>Source Directory</b> is the path to the directory which contains subfolders to be merged.</li>
<li><b>Destination Directory</b> is the name of the destination directory. All the files from the source directory will be moved to this directory. </li>

<h4>Execute:</h4>

```
merge.py /path/to/source /path/to/destination
```

<h4>Example:</h4>

```
python merge.py "/Users/sourcefolder" "/Users/destfolder"
```

After, downloading the required files, and merging the required subfolders, Data uploader to redshift cluster can be used as the final step.</p>

<h3>Scheduling downloads</h3>

You can use e.g. crontab (linux, example) or automator (mac, example) to automate requests every week, month etc.

