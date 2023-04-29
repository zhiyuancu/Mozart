# Mozart 

This is the repo for MobiSys 2023 paper: "Mozart: A Mobile ToF System for Sensing in the Dark through Phase Manipulation".
<br>

# Requirements
The program has been tested in the following environment: 
TBD
<br>

# Mozart Overview
<p align="center" >
	<img src="https://github.com/zhiyuancu/Mozart/blob/main/Figures/system-overview.jpg" width="800">
</p>

* ClusterFL on client: 
	* do local training with the collabrative learning variables;
	* communicate with the server.
* ClusterFL on server: 
	* recieve model weights from the clients;
	* learn the relationship of clients;
	* update the collabrative learning variables and send them to each client.


# Project Strcuture
```
|-- code               // code
    |-- data collection		//code for collecting data
        |-- CalFromDepthAndIR
	|-- libPointCloud
    |-- Mozart
    |-- AndroidApp
        

|-- README.md

|-- Figures             // figures used this README.md
```
<br>

# Quick Start
* TBD

    ---
