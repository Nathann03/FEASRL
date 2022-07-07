# .conll file analysis
import os
import nltk
from nltk.corpus import framenet as fn


# Change this to the file you are looking to analyze
file_name = "everyone_chat.conll"
orig = False

if ".conll" in file_name:
    correct_os = input("Is your OS either Linux or Windows (Y/N)? ")
    if correct_os == "Y":
        oper = input("Is it Linux? (Type Y or N): ")
        orig = True
        if oper == "Y":
            os.system("cp {} temp.txt")
        else:
            os.system("copy {} temp.conll".format(file_name))
            os.system("ren temp.conll temp.txt")
        file_name = "temp.txt"

#filename = "Webex_comp.txt"
file = open(file_name, "r", encoding="utf8")

empty = []
sentences = [[[]]]

# Splits the .txt file 

# Used to knwo where to append each frame.
line_index = 0
frame_index = 0
sent_index = 0

# Used in sentence matching
temp_frame = []
current_sent = []
first_5 = []

# ----------------------------------------------------------------------------------------------------------
# How the .txt/.conll file into 4-d vector works:                                                           |
#                                                                                                           |
# This read the file line by line and splits each word in a line into different entries in a temporary      |
# frame until the entire sentence entry is finished.                                                        |
#                                                                                                           |
# Since we are reading a multi-sentence file, we keep it in a temporary frame to check if the last          |
# frame is different from this frame's sentence. This is a achieved by saving the first 5 words in          |
# the sentence and the first 5 words of the expected sentence and see if they match. If they do,            |
# it is okay to append it to the first sentence frames list. Else, make a new sentence list and append it   |
# then it adds up the sentence counter to know what sentence we need to append the temporary frame in.      |
#                                                                                                           |
# 4-d sentence order: All sentence -> sentence # -> frame # -> line # -> column #                           |
# ----------------------------------------------------------------------------------------------------------

for line in file:
    x = line.split("\t")
    # Checks if next line is a new line, therefore new frame
    if x[0] == "\n":
        sentences[sent_index][frame_index] = temp_frame
        temp_frame = []
        sentences[sent_index].append([])
        frame_index += 1
        first_5 =[]
        line_index = 0
    # If not a new line, parse through frame line by line and check if new sentence
    else:
        temp_frame.append(x)
        if len(first_5) != 5:
            first_5.append(temp_frame[line_index][1])
        
        elif len(first_5) == 5:            
            if current_sent == []:
                current_sent = first_5
            elif not(first_5 == current_sent):
                current_sent = first_5
                sentences[sent_index].remove([])
                sent_index += 1
                sentences.append([[]])
                frame_index = 0

        line_index += 1
# Removes a stray empty list
sentences[sent_index].remove([])

file.close()
if orig:
    if oper == "Y":
        os.system("rm temp.txt")
    else:
        os.system("del temp.txt")        

# parse through to see if frame contains .v (main verb) or temporal

contains = False

# Used to store sentences and main verbs for output later
all_sentence = []
main_words = []
main_word_lu = []

# Note: Pop list is 1-d and saves sentence and frame as [frame #, sentence#, frame #, ...]
pop_list = []

# Used to see if verb or temproal type word is used in the frame
substr = ".v"
substr2 = "Temporal"

frame_index = 0
sent_index = 0

# ------------------------------------------------------------------------------------------
# How does reading the 4-d array work and taking out what is needed:                        |
#                                                                                           |
# This reads frame by frame in each sentence and reads each line in a frame                 |
# to see if the substring we are looking for (.v or Temporal) is in it. If it is            |
# doesn't do anything, else it notes down the sentence and frame to pop later since they    |
# are irrelvant.                                                                            |
# This also notes down all of the sentences used in the .conll file for output to the .txt  |
# file for later. It saves these sentences in a list, so it is easy to access later.        |
# It also saves the main word that is used and its LU (from frame net) for later use in     |
# output to the .txt file.                                                                  |
# ------------------------------------------------------------------------------------------

for sentence in sentences:
    for frame in sentence:

        if len(all_sentence) == sent_index:
            temp_sent = []

        for line in frame:

            if len(all_sentence) == sent_index:
                if line[1] == "unk":
                    temp_sent.append("the")
                else:
                    temp_sent.append(line[1])
            
            # Column 13 = part of speech, column 14 = LU
            if (substr in line[12]) or (substr2 in line[13]):
                main_words.append(line[1])
                main_word_lu.append(line[13])
                contains = True
                break   
            
        if not(contains):
            pop_list.append(frame_index)
            pop_list.append(sent_index)

        contains = False
        frame_index += 1  
    all_sentence.append(' '.join(temp_sent))   
    
    frame_index = 0
    sent_index += 1 

print(all_sentence)

  

# pop frames not containing .v or temporal, Note: it reverses the pop list so, it maintains the index
# for each pop.
pop_list.reverse()
for i in range(int((len(pop_list)/2))):
    sentences[pop_list[2*i]].pop(pop_list[2*i + 1])


# checks if col 14 is not zero or underscore. Therefore, FE left.
x = open("Results.txt", "w")
w_count = 0

# ------------------------------------------------------------------------------------------
# How does outputting to the .txt file work:                                                |
#                                                                                           |
# This iterates through each sentence and outputs the sentence it is reading from the       |
# saved sentence list we made earlier. It then iterates through each frame looking for any  |
# related FEs and lists them under the main verb we saved before. It also searches for any  |
# missing FEs that were not specified or identified in the current frame and lists them.    |
# Note: It also fixes the UNK error in open-sesame, so it will never show up in output.     |
# ------------------------------------------------------------------------------------------

for sentence in range(len(sentences)):
    if sentence == 0:
        x.write("Sentence: {}\n".format(all_sentence[sentence]))
    else:
        x.write("\nSentence: {}\n".format(all_sentence[sentence]))
    
    for frame in range(len(sentences[sentence])):
        existing_fe = []
        pop_list = []
        
        if frame == 0:
            x.write("\tMain Word: {} (LU: {})\n".format(main_words[w_count], main_word_lu[w_count]))
            x.write("\tAssociated FEs in Sentence (Word associated -> FE):\n")
        else:
            x.write("\n\tMain Word: {} (LU: {})\n".format(main_words[w_count], main_word_lu[w_count]))
            x.write("\tAssociated FEs in Sentence (Word associated -> FE):\n")
        

        for line in range(len(sentences[sentence][frame])-1):
            if not((sentences[sentence][frame][line][14] == "O\n") or (sentences[sentence][frame][line][14] == "_")):
                if sentences[sentence][frame][line][1] == "unk":
                    x.write("\t\tthe -> {}".format(sentences[sentence][frame][line][14]))
                else:
                    x.write("\t\t{} -> {}".format( sentences[sentence][frame][line][1], sentences[sentence][frame][line][14]))
                
                existing_fe.append(sentences[sentence][frame][line][14])
        
        # This bottom section adds in the Missing FEs from each frame by using NLTK. First 3 lines are 
        # most important as they generate the FEs
        curr_lu = fn.frames(main_word_lu[w_count])
        f = fn.frame(curr_lu[0].get("ID"))
        FEs = sorted([x for x in f.FE])
        
        for exist in existing_fe:
            for i in range(len(FEs)-1):
                if FEs[i] in exist:
                    pop_list.append(i)

        pop_list = list(set(pop_list))
        pop_list.sort()
        pop_list.reverse()

        for i in pop_list:
            FEs.pop(i)
        
        x.write("\tMissing FEs in Sentence:\n\t\t")
        for fe in FEs:
            x.write("{}, ".format(fe))
        x.write("\n")
        w_count += 1

x.close()
            

