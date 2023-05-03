### Autoencoder for Mozart
This folder is for autoencoder-based Mozart.

Example data is provided in the *example_1, example_2, example_3* folder. You can run

```
cd IQ-NN-example
python3 main.py --w1 (ratio_loss_1) --w2 (ratio_loss_2) --w3 (ratio_loss_3) -epochs (num of epochs) --batch_size (batch size) --lr (learning rate) --source example_1 --setting (str of weight combination)
```

to train the autoencoder for Mozart generation. 

Then you can run
```
python3 inference.py folder_name
```
for inference.
