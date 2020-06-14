## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Prerequisites

You will need to have `python3` and the following packages installed: `tensorflow,pandas,pillows,matplotlib,numpy`

Here's how you can install them with `pip`

```
pip install -r requirement.txt
```

## Running the Code

A frame from the CCTV Footage should be taken every 10 seconds and saved to the directory `model/images`. The program can then be run using 
```
python3 main.py
```

Any incidents detected will be sent via POST request to [PORTAL](https://portal:5000/request) 
