[bruno]: https://github.com/BrunoXBSantos
[bruno-pic]: https://github.com/BrunoXBSantos.png?size=120
[flavio]: https://github.com/FlavioMartins93
[flavio-pic]: https://github.com/FlavioMartins93.png?size=70
[francisco]: https://github.com/fmoraispires
[francisco-pic]: https://github.com/fmoraispires.png?size=70
[pedro]: https://github.com/pCosta99
[pedro-pic]: https://github.com/pCosta99.png?size=70

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

This project explore the creation of a decentralized timeline service(e.g. Twitter, Instagram, Facebook) that harvests peer-to-peer and edge devices

## :rocket: Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes..

### :inbox_tray: Prerequisites

The following software is required to be installed on your system:

- [Python3](https://www.python.org/downloads/)
- [Library kademlia](https://pypi.org/project/kademlia/)


### :gear: Setup

Installs all necessary dependencies to run the program.

```
pip install -r requirements.txt
```

### :hammer: Development

Create the first node of the P2P network. This node is like all the others, but with the particularity of being known by everyone.

```
python3 Bootstrap.py 
```
add a node to the network. Bootstrap_ip and bootstrap_port fields have by default the values ​​of the first created node.

```
python3 peer.py <-pDHT port_dht> <-pP2P port_p2p> [<-ipB bootstrap_ip> <-pB bootstrap_port>]
```

Example of adding a node: 
```
python3 peer.py -pDHT 5000 -pP2P 5001
```

### :hammer_and_wrench: Tools


## :busts_in_silhouette: Team

| [![Bruno][bruno-pic]][bruno] | [![Flávio][flavio-pic]][flavio] | [![Francisco][francisco-pic]][francisco] | [![Pedro][pedro-pic]][pedro] |
| :--------------------------: | :-----------------------------: | :--------------------: | :-----------------------------: |
|    [Bruno Santos][bruno]     |    [Flávio Martins][flavio]     |    [Francisco Morais][francisco]     |    [Pedro Costa][pedro]     |
