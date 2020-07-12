# :sunny: Helios :sunny:
![GitHub](https://img.shields.io/github/license/Bleets/helios)

Helios, is a student project about how to map a cloud infrastructure. The goal is to simplify visualization of the infrastructure between different services

## Usage

### Prerequisites

For this project, you need :

- Docker
- python3
- Good AWS configuration

### Install

1. Setup your AWS Credentials

```bash
cp ~/.aws/credentials ./conf/credentials
```

2. Build the docker containing all you need
```bash
make build
```

### First Run

**1.** Start the project
```bash
make start
```

**2.** Go on your [localhost:7474](http://localhost:7474/browser/), , you should see this :
![starting image](img/start.png)

**3.** Click on `MATCH (n) RETURN n`, to see all data collect

### TIPS

Attach the command, so it wont scroll down after each result
![attach command](img/attach.png)

### Refresh or switch AWS account

To refresh all data or use another AWS account, male sure your `.aws/credentials`  is correct

**1.** Run the following command :
```bash
# make refresh ENV=<your environment>
make refresh ENV=dev
```
**2.** Go on your [localhost:7474](http://localhost:7474/browser/)
![starting image](img/start.png)

**3.** Click on `MATCH (n) RETURN n`, to see all data collect


### CMAP

**CMAP** allow to see all your ressources, start with an URL.

**1.** Run the following command :

```bash
# make cmap DNS=<your dns or url> ENV=<your environment>
make cmap DNS="toto.com" ENV=dev
```
**2.** Go on your [localhost:7474](http://localhost:7474/browser/)
![starting image](img/start.png)

**3.** Click on `MATCH (n) RETURN n`, to see all data collect

## Contributing

:warning: **Actually, you can't contribute to the project**, it will be open-source when the school project is finish.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the available versions, see the [tags on this repository](https://github.com/Bleets/helios/tags).

## Authors

* **Bleets** - [Bleets](https://github.com/Bleets)
* **toxicz9** - [toxicz9](https://github.com/toxicz9)
* **Daigen9** - [Daigen9](https://github.com/Daigen9)
* **timotheTim** - [timotheTim](https://github.com/timotheTim)

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