### ConvertPhase.py
This script is for converting depth map and IR map into raw phase components: $N_1, N_2$.

### Running Environments
numpy                   1.19.5

opencv-python           4.5.3.56

Pillow                  8.2.0



### Quick Start

Example data is provided in the *exp* folder. You can run

```
python3 ConvertPhase.py exp 20
```

to check the result. The calculated raw phase components are stored in *.npz* file for further processing.
