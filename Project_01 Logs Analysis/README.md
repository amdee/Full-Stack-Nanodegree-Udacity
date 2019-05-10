# Logs Analysis Project

### by Abdul Mdee

Logs Analysis Project, part of the Udacity
[Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## Project purpose
To write SQL queries to answer the following questions about a PostgreSQL
database containing the logs of a fictional newspaper website.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Setup required for the Project:
This project is run in a virutal machine.
#### Installing the dependencies and setting up the files:
1. Install [Vagrant](https://www.vagrantup.com/)
1. Install [VirtualBox](https://www.virtualbox.org/)
1. Download the vagrant setup files from [Udacity's Github](https://github.com/udacity/fullstack-nanodegree-vm)
These files needed to configure the virtual machine and install them prior running the project.
1. Download the database setup: [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
1. Unzip the data to get the newsdata.sql file.
1. Put the newsdata.sql file into the vagrant directory
1. Download this project: [log analysis](https://github.com/amdee/Full-Stack-Web-Developer-Nanodegree-projects/tree/master/report)
1. Upzip as needed and copy all files into the vagrant directory into a folder called log_analysis
#### Start the Virtual Machine:
1. Open Terminal and navigate to the project folders we setup above.
1. cd into the vagrant directory
1. Run ``` vagrant up ``` to build the VM for the first time.
1. Once it is built, run ``` vagrant ssh ``` to connect.
1. cd into the correct project directory: ``` cd /vagrant/report ```
#### Load the data into the database:
1. Load the data using the following command: ``` psql -d news -f newsdata.sql ```

### Running the reporting tool
The logs reporting is executed with the following command:

```bash
python report.py
```



## Helpful Resources
* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
* [PostgreSQL 9.5 Documentation](https://www.postgresql.org/docs/9.5/static/index.html)
* [Vagrant](https://www.vagrantup.com/downloads)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
