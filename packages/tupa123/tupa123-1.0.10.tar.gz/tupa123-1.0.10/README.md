Fully connected four-layer neural network
Solves a huge number of cases, both classification and regression
In the sequence, the use is explained with two example files
In the first file, the learning process is carried out, where the enural network finds its weights
The second file is the application of the network for cases outside the scope of learning


--------------------------------files without comments:-------------------------------

-------file .py to machine learn:-------

import tupa123 as tu

X = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=300)
y = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=300)

model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, rate=0.01, epochs=2000, fa2c=5, fa3c=5, fa4c=0)
model.Fit_ADAM(X, y)
model.Plotconv()

input('end')

------file .py to test prediction:--------

import tupa123 as tu

model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, fa2c=5, fa3c=5, fa4c=0)
X_new = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=1000)
y_resposta = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=1000)
y_pred = model.Predict(X_new)

tu.Statistics(y_pred, y_resposta)
tu.PlotCorrelation(y_pred, y_resposta)
tu.PlotComparative(y_pred, y_resposta)
input('end')


-----------------------------------commented file:--------------------------------

#---------------MACHINE LEARNING---------------

#import the library-------------
import tupa123 as tu

#learning data------------------
#The data can come from any source, but the ExcelMatrix function allows a practical interaction with Excel
#ExcelMatrix = collect data from excel, the spreadsheet needs to be in the same folder as the python file
#'ALETAS.xlsm' = example name of the excel file / 'Sheet1' = example name of the tab where the data are
#Lineini=2, Columini=1 = example initial row and column of data
#linesquantity = number of lines of learning data
#X = regression input data / y = data to be predicted
X = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=300)
y = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=300)

#creates the Neural Network model ---------------
#norma = type of data normalization:
#   =0, do anything
#   =1, between 0 and 1
#   =2, between -1 and 1 
#   =3, log(x+coef)
#   =4, log(x+coef)  between 0 and 1
#   =5, log(x+coef)  between -1 and 1
#nn1c=5, nn2c=7, nn3c=5, nn4c=2 = number of neurons from the first to the fourth layer
#epochs = number of epochs
#fa2c=5, fa3c=5, fa4c=0 = second to fourth layer activation functions
#for regression (quantitative forecasting) the fourth layer is recommended as linear = 0
#Activation functions:
#   =0 linear 
#   =1 Sigmoide        
#   =2 softpluss 
#   =3 gaussinana 
#   =4 ReLU 
#   =5 tanh 
#   =6 LReLU      
#   =7 arctan 
#   =8 exp 
#   =9 seno 
#   =10 swish 
#   =11 selu 
#   =12 logsigmoide 
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, rate=0.01, epochs=2000, fa2c=5, fa3c=5, fa4c=0)

#machine learning----------------
#model.Fit_ADAM(X, y) = single batch interpolation of all learning data, with ADAM accelerator
#model.Fit_STOC(X, y) = case-by-case interpolation, stochastic gradient descent
model.Fit_ADAM(X, y)

#Plot the convergence process---------
model.Plotconv()

input('End')


#----------------------APPLICATION OF MACHINE LEARNING------------------
import tupa123 as tu

#application file must be in the same folder as the learning file
#  where some .txt files were generated with the neural network settings
#neural network must have the same configuration that was used in the learning phase
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, fa2c=5, fa3c=5, fa4c=0)

#variables to be predicted------------------------
X_new = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=1000)

#right answer to compare, to evaluate neural network performance-----------
y_resposta = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=1000)

#prediction, neural network result-------------
y_pred = model.Predict(X_new) 

#Statistical evaluation of the results----------------
#It does some basic statistics: mean difference, standard deviation and correlation coefficient between predicted and target variable
tu.Statistics(y_pred, y_resposta)

#Calculated and target correlation plot----------
tu.PlotCorrelation(y_pred, y_resposta)

#Calculated and target comparative plot-----------
tu.PlotComparative(y_pred, y_resposta)

input('end')