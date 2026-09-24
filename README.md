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

5. Next, I imported the "Chemical Properties" file, copying each down in a for loop to write it as a matrix, with each element as a row and each property as a column. I also checked whether it had been successfully imported, otherwise forcefully stopping the program to avoid incorrect values later on.

6. I then imported 
