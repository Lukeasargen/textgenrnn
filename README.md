[https://www.pugetsystems.com/labs/hpc/How-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-UPDATED-1419/](https://www.pugetsystems.com/labs/hpc/How-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-UPDATED-1419/)

Install to use tts

```pip install pyttsx3```


This version of kears works best for me:

```pip install --user keras==2.3.1```

## Notes
* large batch size is better, training can take longer to converge
* use an exponential loss schedule instead of linear, linear had the loss too high for too long and the model was noising and more likely to diverge
* high dropout (>0.5) can help is dataset is small
* validation wastes a lot of time, don't do it unless you have a reason


Add some different losses

```
# line 200 in textgenrnn.py
base_lr = 4e-3

# scheduler function must be defined inline.
def lr_linear_decay(epoch):
    return (base_lr * (1 - (epoch / num_epochs)))

final_decay = 0.04

def exp_decay(epoch):
    lr = (base_lr * (final_decay ** ( epoch / num_epochs ) ) )
    print("LR : {:.6f}".format(lr))
    return lr

step_size = 14

from math import sin, pi

def sin_decay(epoch):
    decay = base_lr*(final_decay**(epoch/num_epochs))
    inner_sin = (2*pi*(epoch%step_size))/step_size
    lr = decay + (0.5*(base_lr*final_decay*(sin(inner_sin)+1)))
    print("LR : {:.6f}".format(lr))
    return lr

def cos_decay(epoch):
    lr = base_lr * cos( (pi*epoch) / (2*num_epochs))
    print("LR : {:.6f}".format(lr))
    return lr
```

Also change the lr in the optimizer

`optimizer=Adam(lr=base_lr)`

