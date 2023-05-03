### Data collection for DepthEye
This script is for collecting raw depth components from DepthEye ToF camera.

Please refer to "SensorSetup.md" for setting up environment.

Then plugin the DepthEye sensor and run the following commands:

```
cd code/phase_data_collection
cmake .
make
./get_raw_phase
```

The collected data are stored in binary file. So you can turn the data into *.npz* files for further processing using binary2npz.py and convert the cwToF phase components into $N_1, N_2$ using ConvertPhase.py:

```
python3 binary2npz.py folder_name file_num
python3 ConvertPhase.py folder_name file_num
```
