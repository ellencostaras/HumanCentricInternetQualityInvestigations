# DesktopDownthrottlingExperiment 

Welcome to Experiment 1 of our Honours Project! This is a working space. <3

Inside this repository you will find two shell scripts, and two folders: <br><br>


## Pre-experiment folder:
This folder houses all the files involved in setting up the experiment. This includes:<br><br>

#### test_combos_creation.ipynb:
This is a jupyter notebook file which helps us to create CSV files with all the treatments we want to test. 

The first and second functions allow you to input a lowbound, upperbound and step size for each variable (upload, download, rtt, packet loss). Then it creates all the combinations in a CSV called "test_combos.csv". The only difference between the first and second function is that one includes packet loss as a variable we will manipulate, and the other does not.

The third and fourth functions allow you to input the exact values you want the variables (upload, download, rtt, packet loss) to take and then it creates all the combinations in a CSV called "test_combos.csv". The only difference between the third and fourth function is that one includes packet loss as a variable we will manipulate, and the other does not.

The last function takes in "test_combos.csv" and shuffles the rows, outputting a new file "test_combos_suffled.csv". <br><br>

#### test_combos.csv and test_combos_shuffled.csv:
These are examples of what the ^^ 'test combos creation.ipynb' file has created. These are just placeholders for testing purposes currently, but will be replaced with the proper ones eventually. <br><br>


## Post-experiment folder:
This folder houses all the files involved in dealing with and anlysing the experiments's outputs. This includes:<br><br>

#### testing_stats:
This is a folder where we can keep our test run outputs for now. It has two folders in it currently, from test runs on the 9th and 13th of August. Inside these, the Web RTC stat dumps (json .txt files) are all stored. 
It is important that the stat dumps follow the following naming convention: treatment{number}_ellen.txt or treatment{number}_aadya.txt. For example "treatment2_ellen.txt". Each file could be from one of the treatments in the test_combos files.<br><br>

#### parsing_WebRTC_stats.py:
This is a python file with all the function logic necessary for parsing a Web RTC stat dump. <br><br>

#### running_parsers.*ipynb:
This is a jupyter notebook which runs the functions in parsing_WebRTC_stats.py, so that you don't have to really look at all the logic, you can just run it if you wish. By running the cells with the correct file path to wherever the stat dumps are located on you computer, it was turn the stat dumps into nice csv files. There will be one csv file per treatment, and for any second of the call that a statistic doesn't have data for, I put a '-1' in that cell. Test outputs are found in:<br><br>

#### CSV_files_test_13Aug:
A folder contained the parsed and cleaned csv files for the test on 13 Aug.<br><br>


## Shell scripts:

#### Exp1WithPacketLoss.sh or Exp1WithoutPacketLoss
This is a shell script which engages the throttle without us necessarily knowing the conditions it has engaged. This is how you run it on a mac (only works if npm and throttle are already installed):

##### Step 1: 
Open terminal app

##### Step 2: 
Navigate to the folder where you have downloaded all of these files. this can be done by typing something like:
```
cd Desktop
cd experiment1
```

##### Step 3: 
Run the script by typing:
```
bash Exp1WithPacketLoss
```
OR
```
bash Exp1WithoutPacketLoss
```
You should use "Exp1WithPacketLoss" if the test_combos_shuffled.csv file includes packet loss as a column.

##### Step 4: 
Simply follow the instructions on screen!!

