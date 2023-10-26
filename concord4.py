import sys
import re
import fileinput

class concord:

    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output
        
        if self.output != None:
            self.full_concordance()


    def full_concordance(self):
        """
        Generates the whole concordance and returns a list of strings
        will the be called to be outputted as stdout, based on a newline separated output
        or from a new method in the class that writes to a file 

        RETURNS: a list of concorded lines if output is none or writes to the output file if it is not 
        """
        ex_list = []
        all_o_lines = []
        output_list = []
        exclu_flag = True
	
        for line in fileinput.input(self.input):
            ex_list, all_o_lines, exclu_flag = self.__get_words(line, ex_list, all_o_lines, exclu_flag)
          
        fileinput.close()
        
        all_o_lines = [word for word in all_o_lines if word]
        
        index_list = self.__get_index(ex_list, all_o_lines)

        #get a list of the lines formatted as  strings
        output_list = self.__organize_lines(index_list, all_o_lines)

        #if there is an output file write to it instead of returning the list of strings
        if self.output != None:
          
            # write to given output file
            file = open(self.output, "w")
            file.write("\n".join(output_list))
            file.write("\n")

            file.close()

        else:

            #return the list of formatted strings
            return output_list


    def __organize_lines(self, indexed_words, all_o_lines):
        """
        Takes all the lines and finds the ones that have the indexed words in them then calls format_lines to 
        PARAMETERS: indexed_words - list of index words
                all_o_lines - list of lines as strings
        RETURNS:    list of lines formatted based on indexed words     
    
        """
        output_lines = []
      
        for indexed in indexed_words:
            for each_line in all_o_lines:
                
                # the index word if it is the full word and not a substring
                my_regex = r"\b" + re.escape(indexed) + r"\b"
                #is the index word in the string 
                if(re.search(my_regex, each_line, re.IGNORECASE)):
                 
                    # update the output lines list with each new formatted word
                    output_lines = self.__format_lines(output_lines, each_line, indexed)
                



        return output_lines

    
    def __format_lines(self, list_o_lines, the_line, index_word):
        """
        Formats the line with the indexed word capitalized and the rest of the line based on the left and right boundaries
        PARAMETERS: list_o_lines - the list of output lines
                the_line - the string of the line to format
                index_word - the word to format and capitalize around
        RETURN: the updates list of ouput lines with the new fromatted line as a string
        """
    
        # LEFT is the left side of the string 
        # RIGHT is thr right side of the string
        line_format = """         ==LEFT====RIGHT=="""
        
        # split the line into a list and get the right and left side of the index word
        line_list = the_line.split(" ")
        line_list = [word for word in line_list if word]
       
       #gets the index number of the indexed word from the list of word in line
        the_index_num = self.__index_search(line_list, index_word)
        #gets the left side of the indexed word + buffer as a string
        left_str = self.__get_left(line_list, index_word, the_index_num)
        #gets the right side of the indexed_word inclusing indexed word as a string
        right_str = self.__get_right(line_list, index_word, the_index_num)

        #replaces the left and right with the formatted strings
        final = re.sub(r"==LEFT==", left_str, line_format)
        final = re.sub(r"==RIGHT==", right_str, final)
        #capitalizes index word
        cap_index = r"\b" + re.escape(index_word) + r"\b"
        final = re.sub(cap_index, index_word.upper(), final)
 

        list_o_lines.append(final)

        return list_o_lines

   
    def __index_search(self, word_list, target_word):
        """
        Will find index word in word list case insensitive
        PARAMETERS: word_list - list of words in the line
                target_word - word you are looking for in the list
        RETURNS: index of word in the list, if not in list returns -1
        """
        
        target_word = target_word.lower()
        count = 0
        for word in word_list:
            word = word.lower()
            if word == target_word:
                return count
            else: 
                count = count +1

        # if we are here no match
        return -1

   
    def __get_left(self, word_list, index, index_num):
        """
        Finds how many words fit between the left boundary and the index word
        PARAMETERS: word_list -the list of words in the line
                index - the string of the indexed word
                index_num - gets the indexed word index in the list
        RETURNS: a string with the left side of the index word
        """

        #one space already added to formatted line, so no need to add a space
        left_max_len = 20
        cur_left_len = 0

        left_string = ""

        for word in reversed(word_list[:index_num]):

            if (cur_left_len + len(word) + 1) <= left_max_len:
                left_string = word + " " +left_string
                cur_left_len = cur_left_len + len(word) + 1
            else:
                # if it would be out of bounds, then no more words can be added
                break


        left_string = (left_max_len-cur_left_len)* " " + left_string

        return left_string


   
    def __get_right(self, word_list, index, index_num):
        """ 
        Get the right side from the index word to the right boundary
        PARAMETERS: word_list - list of words in the sentence
                index - the string of th eindexed word
        RETURNS: a string of the right side of the indexed word inclusing the indexed word
        """ 
      

        right_max_len = 31 - len(index)

        cur_right_len = 0
        #start the string with the index word already 
        right_string = index

        
        #adds words including the indexed word to right string
        for word in word_list[index_num +1:]:
           
            if (cur_right_len + len(word) + 1) <= right_max_len:
			
                
                right_string = right_string +  " " + word 
				
                cur_right_len = cur_right_len + len(word) + 1
            else:
                break
        
        return right_string


    def __get_words(self, i_line, exclusion, all_lines, ex_flag ):

        """
        Gets the exlusion word list from the input bewteen """ """ and updates the exclusion list 
            - then adds all the other lines in the 
        PARAMETERS: the line, the exclusion list, and the current list of all lines and the exclusion flag
        RETURNS: returns exclusion list and list of all lines and the exclusion flag
        """
        i_line = i_line.rstrip("\n")
        
        if i_line == "\"\"\"\"":
            #update to stop adding to exclusion list
            ex_flag = False
        elif i_line != "2" and i_line != "''''":
            # add if not the version and list boundaries

            #still an exclsuion word if true
            if ex_flag:
                exclusion.append(i_line)
            elif i_line != "":
                all_lines.append(i_line)

            
        return exclusion, all_lines, ex_flag


    
    def __get_index(self, ex_words, all_lines):
        """
        Gets the individual index words from the lines and returns a list of strings 
        PARAMETERS: ex_words - a list of exclusion words that should not be in returned list
                    all_lines - list of all lines as strings
        RETURNS: a sorted list of unique index words
        """
        indexed_words = []
        for r_line in all_lines:
            
            # split up the words in each line
            r_line = r_line.split(" ")
            
           #get rid of words that are in exclusion
            new_words = [word for word in r_line if word.lower() not in ex_words if word not in ex_words]
            
            #go through each word to see if it is already in the indexed_words, case insensitive
            for word in new_words:
                if word == "":
                    continue
                pos = self.__index_search(indexed_words, word)
                if pos == -1:
                    indexed_words.append(word)

        indexed_words = sorted(indexed_words, key= str.lower)

        return indexed_words

