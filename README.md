# Porting TinyML on MCU

## TFLM  Environment Setup
### Building Environment
1. Install conda
```shell=
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
# You can spam white space to skip license agreement review
```
2. Create venv
```shell=
conda create -n tflm python=3.7
```
3. Install mbed-cli and requirement
```shell=
sudo apt install git mercurial libusb-1.0-0-dev
conda activate tflm
pip install mbed-cli
# install python dependency
wget https://raw.githubusercontent.com/ARMmbed/mbed-os/master/requirements.txt
pip install -r requirements.txt
```
3. Install compiler. Please refer to this [doc](https://os.mbed.com/docs/mbed-os/v6.15/build-tools/install-and-set-up.html) and install Arm GNU toolchain.
    a) Download compiler version: `gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux`, [GNU Arm Embedded Toolchain Downloads page](https://developer.arm.com/downloads/-/gnu-rm)
    ```shell=
    sudo tar -jxvf ~/Downloads/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2 -C /usr/local/    
    ```

    Configure compiler path and default toolchain.
    ```bash=
    mbed config -G GCC_ARM_PATH /usr/local/bin
    mbed config -G TOOLCHAIN GCC_ARM
    ```
### Access permission settings for dev boards \[[ref](https://github.com/f0cal/google-coral/issues/2)\]:
* If the session instantly shutdown after `mbed sterm`, please redo this step.
    * Method 1: udev
    ```shell=
    git clone https://github.com/pyocd/pyOCD.git
    cd pyOCD/udev
    sudo cp *.rules /etc/udev/rules.d
    udevadm control --reload-rules && udevadm trigger
    ```
    * Method 2: dialout group
    ```shell=
    sudo usermod -a -G dialout $USER
    # Then logout and login.
    # If not working, try rebooting your machine.
    ```
* advanced configuration (Optional)
    https://os.mbed.com/docs/mbed-os/v6.10/program-setup/advanced-configuration.html


## Codebase Setup
1. Get TFLM Sample Code from Github
    ```shell=
    git clone --recurse-submodules https://github.com/liuyy3364/AAML_MCU_TinyML_Lab.git
    ```
    or
    ```shell=
    git clone https://github.com/liuyy3364/AAML_MCU_TinyML_Lab.git
    cd AAML_MCU_TinyML_Lab
    git submodule update --init --recursive
    ```
    * lab1+lab2 do use the directory, AAML_TFLM_basic.
    * lab3+lab4 do use the directory, AAML_TFLM_cmsis.

2. mbed setup for each directory
    * Install mbed-os for basic directory
    ```shell=
    cd AAML_TFLM_basic
    mbed add mbed-os
    mbed deploy
    ```
    * Install mbed-os for CMSIS directory
    ```shell=
    cd AAML_TFLM_cmsis
    mbed add mbed-os
    mbed deploy
    ```

3. Convert TFLite model to source code
    * Install original model for TFLM
    ```shell=
    xxd -i pretrainedResnet.tflite > model.cc
    (echo -ne "#include \"ic/ic_model_data.h\"\nalignas(8) "; cat model.cc) > ic_model_data.cc
    sed -i -E 's/(unsigned\s.*\s).*(_len|\[\])/const \1model\2/g' ic_model_data.cc
    cp ic_model_data.cc AAML_TFLM_basic/ic/
    ```

    * Install optimized model for TFLM
    ```shell=
    xxd -i pretrainedResnet_quant.tflite > model.cc
    (echo -ne "#include \"ic/ic_model_data.h\"\nalignas(8) "; cat model.cc) > ic_model_data.cc
    sed -i -E 's/(unsigned\s.*\s).*(_len|\[\])/const \1model\2/g' ic_model_data.cc
    cp ic_model_data.cc AAML_TFLM_cmsis/ic/
    ```

4. Compile and run on MCU
    * connect MCU to computer first, then:
    ```shell=
    cd AAML_TFLM_basic
    # or cd AAML_TFLM_cmsis
    mbed compile -f --sterm --baud 115200
    ```
    * If MCU outputs nothing, please check the permision first. [Here](#Access-permission-settings-for-dev-boards-ref)

## Reference
1. [Board to PC communication over USB](https://os.mbed.com/docs/mbed-os/v6.16/program-setup/serial-communication.html)
    * Use `mbed help` to get more information
2. [TensorFlow Lite for Microcontrollers
](https://www.tensorflow.org/lite/microcontrollers)
