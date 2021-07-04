# :sunny: Helios :sunny:
![GitHub](https://img.shields.io/github/license/Bleets/helios)

Helios, is a student project about how to map a cloud infrastructure. The goal is to simplify visualization of the infrastructure between different services

## Table of contents
- [:sunny: Helios :sunny:](#sunny-helios-sunny)
  - [Table of contents](#table-of-contents)
  - [Usage](#usage)
    - [Prerequisites](#prerequisites)
    - [Help](#help)
    - [Install](#install)
    - [First Run](#first-run)
    - [Refresh or switch AWS account](#refresh-or-switch-aws-account)
    - [Detect single point of failure](#detect-single-point-of-failure)
  - [Contributing](#contributing)
  - [Versioning](#versioning)
  - [Authors](#authors)
  - [License](#license)
  - [References](#references)

## Usage

### Prerequisites
___
For this project, you need :

- Docker
- python3
- :warning: Good AWS configuration, like this :
```markdown
[default]
aws_access_key_id = <YOUR_AWS_KEY_ID>
aws_secret_access_key = <YOUR_AWS_ACCESS_KEY>
region = <AWS_REGION>
output = json

[production]
aws_access_key_id = <YOUR_AWS_KEY_ID>
aws_secret_access_key = <YOUR_AWS_ACCESS_KEY>
output = json
region = <AWS_REGION>

[development]
role_arn = arn:aws:iam::<AWS_ACCOUNT_ID>:role/<YOUR_AWS_ROLE_NAME>
source_profile = default
output = json
region = <AWS_REGION>
```

### Help
___
The code below is the result of the command `make` in the root directory. Don't hesitate to run it on your terminal !
```markdown
 Management Command 
------------------------------ 
setup           /!\ Copy your ~/.aws/credentials into a directory (gitignored) and setup setting file /!\ 
build           Build the container
start           Start the container
stop            Clean the DB and stop the container
reset_setting   reset the setting file
clean           Remove all the data
              
 Project Command  
------------------------------ 
refresh         Refresh all data
              
 Debug Command 
------------------------------ 
bash            Access to the container throught /bin/bash
debug           Launch script to test the connection with neo4j database
```
###  Install
___
1. Setup your AWS Credentials

**:warning: The command bellow will copy your ~/.aws/credentials into a directoy gitignored :warning:**
```bash
make setup
```

2. Build the docker containing all you need
```bash
make build
```

### First Run
___
**1.** Start the project
```bash
make start
```

**2.** Go on your [localhost:7474](http://localhost:7474/browser/), , you should see this :
![starting image](img/start.png)

**3.** Read what is on the right part, and check each point of the **summary**


### Refresh or switch AWS account
___
To refresh all data or use another AWS account, male sure your `.aws/credentials`  is correct

**1.** Run the following command :
```bash
# make refresh ENV=<your environment>
make refresh ENV=dev
```
**2.** Go on your [localhost:7474](http://localhost:7474/browser/)
![starting image](img/start.png)

**3.** Click on AWS if you want to see all global request
![global aws image](img/global_aws.png)

### Detect single point of failure
**1.** Click on a specific service in the summary. To see if there is a command to detect potential SPOF, like in Cloudfront
![cloudfront command image](img/aws_cloudfront.png)

## Contributing

:warning: **Actually, you can't contribute to the project**, it will be open-source when the school project is finish.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the available versions, see the [tags on this repository](https://github.com/Bleets/helios/tags).

## Authors

* [Bleets](https://github.com/Bleets)
* [toxicz9](https://github.com/toxicz9)
* [Daigen9](https://github.com/Daigen9)
* [timotheTim](https://github.com/timotheTim)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References

* [Neo4j](https://neo4j.com/)
* [Neo4j : Docker](https://neo4j.com/developer/docker-run-neo4j/)
* [Neo4j : Custom Guide](https://neo4j.com/developer/guide-create-neo4j-browser-guide/)
* [Cypher](https://neo4j.com/developer/cypher-query-language/)
* [Docker](https://www.docker.com/)
* [Learn about Docker](https://openclassrooms.com/fr/courses/2035766-optimisez-votre-deploiement-en-creant-des-conteneurs-avec-docker)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)