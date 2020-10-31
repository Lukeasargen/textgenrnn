[https://www.pugetsystems.com/labs/hpc/How-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-UPDATED-1419/](https://www.pugetsystems.com/labs/hpc/How-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-UPDATED-1419/)

Use tensorflow 1.15 or 1.14 and a compatable cuDNN library

#### Notes
* large batch size is better
* high dropout (>0.5) can help is dataset is small
* validation wastes a lot of time, don't do it unless you have a reason