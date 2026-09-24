# Tayyab-Abdul-Qayum

This was a project I decided to make in the summer of year 11 as I wanted to explore the maths behind linear regression. The program aims to predict the solubility of a chemical compound based on its data, then plots a graph of solubility based on temperature. It works as follows:

1. In python, the file containing all of the chemical data was accessed. For the first row it did the following:
  Checked the title.
  If the title matched "solubility", then it copied its col_idx (its column number indexxed from 0).
  If it was in another set of words (A list containing necessary attributes to work out solubility) it copied down their col_idx in a separate list.

2. For each row after, it did the following:
   If the col_idx matched with solubility, it would append it onto a CSV file named "Solubility".
   If the col_idx matched with the idx of the compounds we checked before, it is copied onto a CSV file named "Chemical Properties"
   Otherwise, it would just continue.

3. Now we have a dataset, so we can write the maths in c++. I chose c++ as I heard that it was a very fast language, perfect for large matrix calculations, along with being relatively high level, so that I could understand the syntax more easily.
   
4. In c++, I first defined a matrix calculator by using the dot product of each row and column. Given that this had to be nested 3 times, it had a time complexity of O(n³).

5. Next, a matrix writer which wrote each element (referring to number not chemical) down in a for loop, with each compound as a row and each property as a column, written as a general function.

6. I then imported the relative file path for each file, ensuring that, if any errors were present during importation, to forcefully stop the program.

7. I also, initially, initialised a few weights and biases as 0, under a file path.

8. Then, I used the matrix creation function to make a matrix for the chemical compounds, with a check to determine whether it went through as well.

9. I proceeded to do the same with the weights file, followed by another check.

10. In order for them to be valid for matrix multiplication, I had to verift that the number of columns in Chemical Properties matched the number of rows in Weights; if true, it started training.

11. After this, I initialised errors, updated weights and predictions as separate matrices to be used down the line. The rows of Chemical properites and columns of Weights matched the rows and columns in the predictions as it was a resultant matrix that needed to be inputed. I also set an EPOCH limit to avoid it looping infinitely, along with a training rate of 0.00001.

12. I then ran a while loop, with a first initial running using do(). This first multiplied the matrices together to work out our predictions, then compared their values to the expected values that we copied from the original script.

13. Now we updated the weights using a formula: weight = weight - (average_error_term (difference from the expected) * learning rate).

14. We update the biases in a similar way, with bias = bias - (average_error_term * learning_rate), only not used as a loop.

15. We then repeat this until the Mean Average Error (each of the errors from our error matrix averaged) is less than 0.01 or we have reached the limit for the EPOCH

16. We then rewrite our bias and weight files to correct them, then write the worked out (correct) solubilies on another files.

17. Returnign to python, we import this values, then, using some formulas (where we assume the enthalpy is a specific number for all as enthalpy wasn't part of the data provided) we work out the solubility at each temperature for every 0.5* between 0 and 100

18. We allow the user to input their desired chemical by index from the file:
    If it is valid, we use its solubility predictions
    Otherwise we refresh the icon and display a message to show that it could not be found within our index

19. We also ask for a temperature, separated by a space, between 0 and 100, checking the same thing as mentioned above.

20. We then plot the points on the graph, while also stating, based on solubility parameters, how soluble it is. The text box then refreshes to allow the user to ask for another chemical.

21. The y axis holds the solubility readings, changing to fit the whole screen based on the maximum value. This produces graphs that look identical. The x axis holds tempeartures

This is my first ever project. It holds relatively accurate, although the assumptions about enthalpy could cause major innacuracy, along with the Mean Average Error Value being only below 0.01 suggesting that, along my very large dataset of roughly 10,000 compounds, there are likely to be some major outliers.

Overall, I gained a lot of insight into linear regression. I intend to continue with projects similar to his, possibly involving a neural network.
