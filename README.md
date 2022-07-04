# FEASRL - Frame Element Analysis of Sematic Role Labels

FEASRL is a more efficient and descriptive way of analyzing the output of the latest state of the art Sematic Role Labeler, Open-Sesame by Swabhs (https://github.com/swabhs/open-sesame).
FEASRL is able to take in multiline parsings from Open-Sesame and take out the frames containing (.v or Temporal) in the output from Open-Sesame (.conll files). 
FEASRL works both in Linux and Windows, but you will have to answer questions in the terminal to determine which OS you are using to ensure that there is no error in the code when it interacts with the terminal.

# How to manipulate FEASRL

FEASRL is not an executable python script, so you will have to download it and run it yourself. If you are looking for a different feature description like .adj or Gizmo (LU), you can do this by going to line 106 and 107 to change what substrings you are looking for and going to line 140 to change which column to match the substring to.
FEARSRL is fairly well documented within the code, so there should be more than enough description to help ypu fully understand the logic that went into creating it and how to manipulate it.

Ex.
![image](https://user-images.githubusercontent.com/90486674/177208984-586b40f8-6873-4066-87d5-2d23c0235a57.png)

# How to use FEASRL

It is pretty simple to use FEASRL, it onyl takes 4 simple steps before you can start running it.
1. Move the .conll files you wish to parse into the same folder/directory as FEASRL.py
2. Open FEASRL in your preferred IDE
3. Change the file name to the .conll file you are looking to analyze
4. Press Run and answer the following questions to determine which OS you have (Answer with Y or N for all questions only).

# Notes

If there are any issues or concerns, please email me at nguye3np@mail.uc.edu or open an issue in Github. Please credit me if you are planning on using it in any reasearch paper, thank you!
