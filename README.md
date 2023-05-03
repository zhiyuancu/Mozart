# Mozart 

This is the repo for MobiSys 2023 paper: "Mozart: A Mobile ToF System for Sensing in the Dark through Phase Manipulation".
<br>

# Requirements
Different modules require different running environment, detailed requirements can be found in README.md of each folder.
<br>

# Mozart Overview
<p align="center" >
	<img src="https://github.com/zhiyuancu/Mozart/blob/main/Figures/system-overview.jpg" width="800">
</p>

* Data collection: 
	* Collect data from various ToF modules;
	* Support both raw data collection (DepthEye) and indirectly calculation from depth and IR (Vzense DCAM).
* Lightweight manipulation: 
	* Used for lightweight phase manipulation;
	* Provide several pre-defined functions for your choice;
	* You can also design your own functions for exposing and enhancing Mozart maps
* Autoencoder:
	* Used for autoencoder-based phase manipulation.


# Project Strcuture
```
|-- code               // code
    |-- AndroidApp	// Android app 
    	|-- Mozart_BackRealTime //An app that demonstrates Mozart on mobile phones in real-time
    
    |-- autoencoder	// autoencoder-based Mozart training and inference
    	|-- IQ-NN-example
    
    |-- data collection		// code for collecting data
        |-- CalFromDepthAndIR
	|-- libPointCloud
    
    |-- light-weight-manipulation
    	|-- mozart_manual.py	// code for lightweight phase manipulation
	|-- cwToF		// data of cwToF
	|-- pToF		// data of pToF

|-- README.md

|-- Figures             // figures used this README.md
```
<br>

# Quick Start
* Please check the README.md file in each folder

    ---
