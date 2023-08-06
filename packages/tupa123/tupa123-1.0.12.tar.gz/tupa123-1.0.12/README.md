Fully connected four-layer neural network <br>
Solves a huge number of cases, both classification and regression <br>
In the sequence, the use is explained with two example files <br>
In the first file, the learning process is carried out, where the enural network finds its weights <br>
The second file is the application of the network for cases outside the scope of learning <br>
<br>
# -----Files without comments:--------------------------------------- <br>
<br>
# -----FILE TO MACHINE LEARNING <br>
<br>
import tupa123 as tu <br>
<br>
X = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=300) <br>
y = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=300) <br>
<br>
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, rate=0.01, epochs=2000, fa2c=5, fa3c=5, fa4c=0) <br>
model.Fit_ADAM(X, y) <br>
model.Plotconv() <br>
<br>
input('end') <br>
<br>
# -----FILE TO APPLICATION OF MACHINE LEARNING <br>
<br>
import tupa123 as tu <br>
<br>
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, fa2c=5, fa3c=5, fa4c=0) <br>
X_new = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=1000) <br>
y_resposta = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=1000) <br>
y_pred = model.Predict(X_new) <br>
<br>
tu.Statistics(y_pred, y_resposta) <br>
tu.PlotCorrelation(y_pred, y_resposta) <br>
tu.PlotComparative(y_pred, y_resposta) <br>
input('end') <br>
<br>
# ------Commented file:------------------------------------------ <br>
<br>
<br>
# -----MACHINE LEARNING <br>
<br>
import tupa123 as tu <br>
#import the library <br>
<br>
X = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=300) <br>
y = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=300) <br>
#learning data <br>
#The data can come from any source, but the ExcelMatrix function allows a practical interaction with Excel <br>
#ExcelMatrix = collect data from excel, the spreadsheet needs to be in the same folder as the python file <br>
#'ALETAS.xlsm' = example name of the excel file / 'Sheet1' = example name of the tab where the data are <br>
#Lineini=2, Columini=1 = example initial row and column of data <br>
#linesquantity = number of lines of learning data <br>
#X = regression input data / y = data to be predicted <br>
<br>
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, rate=0.01, epochs=2000, fa2c=5, fa3c=5, fa4c=0) <br>
#creates the Neural Network model <br>
#norma = type of data normalization: <br>
#=0, do anything <br>
#=1, between 0 and 1 <br>
#=2, between -1 and 1 <br>
#=3, log(x+coef) <br>
#=4, log(x+coef)  between 0 and 1 <br>
#=5, log(x+coef)  between -1 and 1 <br>
#nn1c=5, nn2c=7, nn3c=5, nn4c=2 = number of neurons from the first to the fourth layer <br>
#epochs = number of epochs <br>
#fa2c=5, fa3c=5, fa4c=0 = second to fourth layer activation functions <br>
#for regression (quantitative forecasting) the fourth layer is recommended as linear = 0 <br>
#Activation functions: <br>
#=0 linear <br> 
#=1 Sigmoide <br>       
#=2 softpluss <br>
#=3 gaussinana <br>
#=4 ReLU <br>
#=5 tanh <br>
#=6 LReLU <br>     
#=7 arctan <br>
#=8 exp <br>
#=9 seno <br>
#=10 swish <br>
#=11 selu <br>
#=12 logsigmoide <br>
<br>
model.Fit_ADAM(X, y) <br>
#machine learning <br>
#model.Fit_ADAM(X, y) = single batch interpolation of all learning data, with ADAM accelerator <br>
#model.Fit_STOC(X, y) = case-by-case interpolation, stochastic gradient descent <br>
<br>
model.Plotconv() <br>
#Plot the convergence process <br>
<br>
input('End') <br>
<br>
#-----APPLICATION OF MACHINE LEARNING <br>
<br>
import tupa123 as tu <br>
<br>
model = tu.nnet4(norma=5, nn1c=5, nn2c=7, nn3c=5, nn4c=2, fa2c=5, fa3c=5, fa4c=0) <br>
#application file must be in the same folder as the learning file <br>
#where some .txt files were generated with the neural network settings <br>
#neural network must have the same configuration that was used in the learning phase <br>
<br>
X_new = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=1, columnquantity=5, linesquantity=1000) <br>
#variables to be predicted <br>
<br>
y_resposta = tu.ExcelMatrix('ALETAS.xlsm', 'Plan1', Lineini=2, Columini=6, columnquantity=2, linesquantity=1000) <br>
#right answer to compare, to evaluate neural network performance <br>
<br>
y_pred = model.Predict(X_new) <br>
#prediction, neural network result <br>
<br>
tu.Statistics(y_pred, y_resposta) <br>
#Statistical evaluation of the results <br>
#It does some basic statistics: mean difference, standard deviation and correlation coefficient between predicted and target variable <br>
<br>
tu.PlotCorrelation(y_pred, y_resposta) <br>
#Calculated and target correlation plot <br>
<br>
tu.PlotComparative(y_pred, y_resposta) <br>
#Calculated and target comparative plot <br>
<br>
input('end') <br>