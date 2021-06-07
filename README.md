[bruno]: https://github.com/BrunoXBSantos
[bruno-pic]: https://github.com/BrunoXBSantos.png?size=120
[flavio]: https://github.com/FlavioMartins93
[flavio-pic]: https://github.com/FlavioMartins93.png?size=100
[francisco]: https://github.com/fmoraispires
[francisco-pic]: https://github.com/fmoraispires.png?size=100
[pedro]: https://github.com/pCosta99
[pedr0-pic]: https://github.com/pCosta99.png?size=100

<div align="center">

# Decentralized Timeline

[Geeting Started](#rocket-getting-started)
|
[Development](#hammer-development)
|
[Tools](#hammer_and_wrench-tools)
|
[Team](#busts_in_silhouette-team)

</div>

The practical work consists of carrying out the experimental evaluation of data
storage and processing tasks using Hive Metastore, Avro + Parquet and Spark
using [IMDb public datasets](https://www.imdb.com/interfaces/).

## :rocket: Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes..

### :inbox_tray: Prerequisites

The following software is required to be installed on your system:

- [Java SDK 8+](https://openjdk.java.net/)
- [Maven](https://maven.apache.org/maven-features.html)
- [GCloud CLI](https://cloud.google.com/sdk/docs/install)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### :gear: Setup

Create instances of hive and spark (using docker containers, based on big-data-europa with resolved incompatibilities).
Configures the spark network by connecting it to Hive and runs the containers (hive and spark) in the background.

```
bin/setup
```

Uploads the .csv files to Hive's HDFS. Creates the tables and converts the data to the parquet format. If the tables or
files already exist there is no problem.

```
docker-hive/setup
```

### :hammer: Development

Run the project.

```
bin/run query <query>
```

Format the code accordingly to common [guide lines](https://github.com/google/google-java-format).

```
bin/format
```

Lint your code with _checkstyle_.

```
bin/lint
```

### :hammer_and_wrench: Tools

The recommended Integrated Development Environment (IDE) is IntelliJ IDEA.

## :busts_in_silhouette: Team

| [![Bruno][bruno-pic]][bruno] | [![Flávio][flavio-pic]][flavio] | [![Francisco][francisco-pic]][francisco] | [![Pedro][pedro-pic]][pedro] |
| :--------------------------: | :-----------------------------: | :--------------------: | :-----------------------------: |
|    [Bruno Santos][bruno]     |    [Flávio Martins][flavio]     |    [Francisco Morais][francisco]     |    [Pedro Costa][pedro]     |
