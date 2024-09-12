rm(list=ls())
wine = read.csv("/Users/User/Documents/GitHub/DesktopDownthrottlingExperiment/post_experiment/Regression/wine.train.csv")

hist(wine$fixed.acidity)
hist(wine$volatile.acidity)
hist(wine$citric.acid)


