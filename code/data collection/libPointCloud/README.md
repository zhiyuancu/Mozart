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

Note: the raw phase data collected will be stored in binary file in the folder *exp*. Therefore, we need to use the script (binary2npz.py) to convert the binary file into readable file for numpy:

```
python3 binary2npz.py exp 100
# python3 binary2npz.py folder_name file_num
```


