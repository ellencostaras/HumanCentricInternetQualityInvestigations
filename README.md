# DesktopDownthrottlingExperiment

Welcome to Experiment 1 of our Honours Project! This is a working space. 

I recommend all these files be kept in a folder on your computer Desktop/Documents.

Inside this repository you will find 5 files: <br><br>


### test combos creation.ipynb:
This is a jupyter notebook file which helps us to create CSV files with all the treatments we want to test. 

The first and second functions allow you to input a lowbound, upperbound and step size for each variable (upload, download, rtt, packet loss). Then it creates all the combinations in a CSV called "test_combos.csv". The only difference between the first and second function is that one includes packet loss as a variable we will manipulate, and the other does not.

The third and fourth functions allow you to input the exact values you want the variables (upload, download, rtt, packet loss) to take and then it creates all the combinations in a CSV called "test_combos.csv". The only difference between the third and fourth function is that one includes packet loss as a variable we will manipulate, and the other does not.

The last function takes in "test_combos.csv" and shuffles the rows, outputting a new file "test_combos_suffled.csv". <br><br>


### test_combos.csv and test_combos_shuffled.csv:
These are examples of what the ^^ 'test combos creation.ipynb' file has created. They can be used as placeholders when running the shell script bellow: <br><br>


### Exp1WithPacketLoss.sh or Exp1WithoutPacketLoss
This is a shell script which engages the throttle without us necessarily knowing the conditions it has engaged. This is how you run it on a mac (only works if npm and throttle are already installed):

#### Step 1: 
Open terminal app

#### Step 2: 
Navigate to the folder where you have downloaded all of these files. this can be done by typing something like:
```
cd Desktop
cd experiment1
```

#### Step 3: 
Run the script by typing:
```
bash Exp1WithPacketLoss
```
OR
```
bash Exp1WithoutPacketLoss
```
You should use "Exp1WithPacketLoss" if the test_combos_shuffled.csv file includes packet loss as a column.

#### Step 4: 
Simply follow the instructions on screen!!

