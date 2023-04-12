# Run the data collection code

(This code is validated on MacOS 13.3.1)

### Hardware Requirement

The code is for raw depth phase data collection using PointCloud.AI® [DepthEye™](https://files.seeedstudio.com/products/114992563/DepthEye_Wide_SonyIMX556_datasheet.pdf) depth cameras.


### Quick start

```
cd code/phase_data_collection
cmake .
make
mkdir exp
./get_raw_phase
```

Note 1: the raw phase data collected will be stored in binary file in the folder *exp*. Therefore, we need to use the script (binary2npz.py) to convert the binary file into readable file for numpy:

```
python3 binary2npz.py exp 100
# python3 binary2npz.py folder_name file_num
```

Note 2: The DepthEye camera collects raw depth data in a 4-phase manner. While in Mozart, we unify all ToF cameras with 2-phase model. Therefore, we need to run:

```
python3 ConvertPhase.py exp 100
# python3 ConvertPhase.py folder_name file_num
```
to convert the collected data to 2-phase representation for Mozart.
