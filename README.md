# anendbtofasta

Tool to grab protein and EC number data from AnEnDB relational database and write into Fasta files.


## Getting Started

**anendbtofasta** is a crucial part of a major set of packages: 

* keggreader
* keggimporter
* blasperin
* clusperin
* clusteringloader

But to run **anendbtofasta** you a fully functional AnEnDB relational database.

The result files follow the format below:

* Each file is a set of proteins from a single EC number.
* Example of a file name:

```
EC_2.3.4.5.fasta
```

**Notice** the file format: 'EC\_' **plus** your EC number **plus** '.fasta'


## Installing

* Download (and extract) the zip file from this repository or clone it using **git** command.
* Go to the opened directory.
* Run:

```
python setup.py install
```

* Installation is done.


## Run anendbtofasta

* Simply type **anendbtofasta** in your console.

**Example:**

```
anendbtofasta --database database_name \
              --password database_password \
              --host database_host \
              --user database_user \
              --destination-directory /var/clustering \
              --log-file /var/log/anendbtofasta.log \
              --ec-numbers '1.2.3.4','6.2.1.19'
```

## Explaining the parameters

* --database database_name

The database name.

* --password database_password

Password to log into the relational database.

* --host database_host

Hostname/IP where's the relational database.
 
* --user database_user

Username to access the database.

* --destination-directory

Where to store the Fasta files.

* --ec-numbers

**Optional**. List of EC numbers, separated by comma.

* --log-file

Full path the a log file. That's necessary because the process can take several hours/days depending on the amount of files.



