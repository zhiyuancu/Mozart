# Mozart 

This is the repo for MobiSys 2023 paper: "Mozart: A Mobile ToF System for Sensing in the Dark through Phase Manipulation".
<br>

# Requirements
The program has been tested in the following environment: 
* Ubuntu 18.04
* Python 3.6.8
* Pillow 8.2.0
* opencv-python 4.5.3.56
* torch 1.10.0
* numpy 1.19.5
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
|-- code                    // code
    |-- client_cfmtl.py/	// main file of client 
    |-- communication.py/	// set up communication with server
    |-- data_pre.py/		// prepare for the FL data
    |-- model_alex_full.py/ 	// model on client 
    |-- desk_run_test.sh/	// run client 

|-- server/    // code in server side
    |-- server_cfmtl.py/        // main file of client
    |-- server_model_alex_full.py/ // model on server 

|-- README.md

|-- pictures               // figures used this README.md
```
<br>

# Quick Start
* Download the `dataset` folders (collected by ourselves) from [FL-Datasets-for-HAR](https://github.com/xmouyang/FL-Datasets-for-HAR) to your client machine.
* Chooose one dataset from the above four datasets and change the "read-path" in 'data_pre.py' to the path on your client machine.
* Change the 'server_x_test.txt' and 'server_y_test.txt' according to your chosen dataset, default as the one for "imu_data_7".
* Change the "server_addr" and "server_port" in 'client_cfmtl.py' as your true server address. 
* Run the following code on the client machine
    ```bash
    cd client
    ./desk_run_test.sh
    ```
* Run the following code on the server machine
    ```bash
    cd server
    python3 server_cfmtl.py
    ```
    ---
