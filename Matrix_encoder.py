
# -*- coding: utf-8 -*-
"""
@author: Kristof Mercier
"""
import numpy as np
import random
import math
import re

def matrixize_raw_string(string, matrix_width):
    """Takes a given string, converts each element to its corresponding int
    value, and  splits it into a matrix of row size matrix_width.
    :param string: the ipput string
    :param matrix_width: The number of elements in a matrix row
    :returns: matrix containing converted numbers.
    """
    #Add padding to a string so it can properly be fit into the array
    mod = len(string)% matrix_width
    if mod > 0:
        for i in range(0,matrix_width-mod):
            string += (" ")

    matrix_list = []
    stop = len(string)//matrix_width
    position = 0
    #Convert to numerical matrix rows
    for i in range(0,stop):
        new_list = []
        #construct a single matrix row
        for j in range(0,matrix_width):
            number = convert_to_number(string[position])
            #check current char is valid
            if(number < 2 or number > 106):
                print("ERROR: The following value cannot be encoded: " + string[position])
                return []
            new_list.append(number)
            position += 1
        matrix_list.append(new_list)
    return np.matrix(matrix_list)


def space_separated_string_to_matrix(string, matrix_width):
    '''Convets a string of integer values separated by spaces seto a matrix
    :param string: the input string in format "x x x x"
    :param matrix_width: matrix row size
    :returns: outputs a matrix with rows of size matrix_width '''
    array = list(map(int, string.split()))
    array = np.reshape(array,(int(len(array)/matrix_width),matrix_width))
    matrix = np.matrix(array)
    return matrix


def convert_numbers_list(input_list):
    '''Calls convert_from_number for each value in the list
    :param input_list: the list of numbers to be converted
    :returns: the converted list.'''
    string = ""
    for i in range(0,len(input_list)):
        string += convert_from_number(input_list[i])
    new_list = list(map(int, string.split()))
    return new_list

def ascii_matrix_to_string(matrix):
    '''Uses makes use of other functions to convert a matrix of integers to
    a more meaningful string of characters.
    :param matrix: the matrix of numbers to be converted
    :returns: the converted string.'''
    array = matrix_to_list(matrix)
    string = ""
    for i in range(0,len(array)):
        string += convert_from_number(array[i])

    #Remove tailing whitespace
    while string[len(string)-1] == ' ':
        string = string[0:len(string)-1]
    return string

def convert_to_number(char_to_change):
    '''Converts a single character to it's numerical value.
    :param char_to_change: the charcter to change
    :returns: an integer version of the input value.'''
    if (char_to_change.isdigit()):
        return (int(char_to_change)) +2
    else:
        return ord(char_to_change)-20

def convert_from_number(int_to_change):
    '''Converts a single integer to it's character value.
    :param int_to_change: the int to change
    :returns: the corresponding character'''
    if (int_to_change <12):
        return str(int_to_change-2)
    else:
        return chr(int_to_change+20)


def generate_key(size):
    '''Uses the generate_potential_key and checks to make sure that the
    returned ,matrix is invertible.
    :param size: The matrix will be of length and width size.
    :returns: a square matrix that is invertible. '''
    invertable = False
    while not invertable:
        potetial_key = generate_potential_key(size)
        #try to invert the matrix.
        try:
            inverse = np.linalg.inv(potetial_key)
        except np.linalg.LinAlgError:
            pass
        else:
            invertable = True
    return np.matrix(potetial_key)


def generate_potential_key(size):
    '''Generate an array of specified dimentions
    :param size: The matrix will be of length and width size.
    :returns: a list of lists that can be easilly converted to a matrix.'''
    matrix_list = []
    for i in range(0,size):
        rowlist = []
        for j in range(0,size):
            if (i%2 == 0):
                element = random.randint(matrix_gen.min_value,0)
            else:
                element = random.randint(0,matrix_gen.max_value)
            rowlist.append(element)
        matrix_list.append(rowlist)
    return matrix_list

def matrix_to_string(matrix):
    '''Converts a matrix to a string
    :param matrix: Any matrix
    :returns: a converted string'''
    return " ".join(str(x) for x in (matrix_to_list(matrix)))

def matrix_to_list(matrix):
    '''Converts a matrix to a list
    :param matrix: Any matrix
    :returns: a converted list'''
    return matrix.A1

def list_to_string(in_list):
    '''Converts a matrix to a list
    :param matrix: Any matrix
    :returns: a converted list'''
    return " ".join(str(x) for x in (in_list))

def combine_message_with_key(key, message):
    '''Uses the fold_list function to fold the key into the message or
    vice-versa depending on which is larger.
    :param message: an integer list
    :param key: an integer list
    :returns: an integer list containing a combined key and message'''
    if (len(key) > len(message)):
        return fold_list(key,message)
    else:
        return fold_list(message,key)


def fold_list(list1, list2):
    '''Takes 2 lists and combines them
    by distributing the list2 evenly through the list1.
    :param list1: an integer list
    :param list2: an integer list
    :returns: an integer list containing a combined key and message'''
    total_len = len(list1) + len(list2)
    curs1 = 0
    curs2 = 0
    new_list = []
    ratio = len(list1) // len(list2)
    while (len(new_list) < total_len):
        for j in range(0,ratio):
            if curs1 < len(list1) :
                new_list.append(list1[curs1])
                curs1 +=1
        if curs2 < len(list2):
            new_list.append(list2[curs2])
            curs2 +=1
    return new_list

def separate_message_from_key(comp_list, key_size):
    '''Untangles the key and message, then uses the key to unlock the message.
    :param comp_list: an integer list containing tangled key and message
    :param key_size: integer key size, as in the total number of elements
    :returns: a string containing the decoded message'''
    total_size = len(comp_list)
    message_size = total_size - key_size
    message = []
    key = []

    #separate the combined list into message and key or vice versa
    if (message_size > key_size):
        ratio = total_size // key_size
        for i in range(0,total_size):
            if ((i)%ratio != 0 and len(key) < key_size):
                key.append(comp_list[i])
            else:
                message.append(comp_list[i])
    else:
        ratio = total_size // message_size
        for i in range(0,total_size):
            if ((i)%ratio == ratio-1 and len(message) < message_size):
                message.append(comp_list[i])
            else:
                key.append(comp_list[i])

    #decrypt the message using the inverse key
    matrix_width = int(math.sqrt(key_size))
    message = np.reshape(message,(int(len(message)/matrix_width),matrix_width))
    key = np.reshape(key,(matrix_width, matrix_width))
    decoded_string = decode_from_matrix(np.matrix(message),np.matrix(key))
    return decoded_string


def encode_to_matrix(input_string, key):
    '''Makes use of the matrixize_raw_string, makes a matrix from that array,
    and multiplies it by the key to encode the message.
    :param input_string: the initial user string that is to be encoded
    :param key: an integer matrix key
    :returns: an encoded integer matrix'''
    raw_matrix = matrixize_raw_string(in_string,len(key))
    coded_matrix = raw_matrix * key
    return coded_matrix


def decode_from_matrix(matrix,key):
    '''Decodes a matrix using its key matrix.
    :param matrix: an integer matrix
    :param key_size: integer key matrix which unlocks the message matrix
    :returns: a string containing the decoded message'''
    decoded_matrix = (matrix * get_inverse_matrix(key)).round().astype(np.int)
    string = ascii_matrix_to_string(decoded_matrix)
    return string



def get_inverse_matrix(matrix):
    '''Uses a numpy library function to calculate a matrix's inverse.
    :param matrix: A square integer matrix whose inverse will be calculated.
    :returns: a matrix containing the inverse key'''
    try:
        inverse = np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        print("ERROR: The key has no inverse!")
        return np.matrix([])
    else:
        return inverse

#Change this to change matrix properties.
class matrix_gen:
    max_value = 5
    min_value = -5

    #NOTE Currently the max_size cannot exceed 7.
    min_size = 3
    max_size = 7
master_key = np.matrix([[-6, 2, 0], [8, 5, 9], [4, 4, -4]])
master_key_width = 3


function = input("type 'encode' to encode a message or 'decode' to decode a message\n")
while function.lower() not in ["encode", "decode"]:
    print("Invalid input!")
    function = input("type 'encode' to encode a message or 'decode' to decode a message\n")


#NOTE: Because of floating point precision problems with the
#library matrix inversion function, longer string have a chance
#of corrupting when they are encoded. There are solutions to this problem,
#but none of them are trivial.

#Encode:
if (function.lower() == "encode"):
    in_string = input("Type your message:\n").lower()

    #Encode the message with a generated key
    matrix_width = random.randint(matrix_gen.min_size,matrix_gen.max_size)
    key = generate_key(matrix_width)
    coded_input = encode_to_matrix(in_string,key)
    combined_list = combine_message_with_key(matrix_to_list(key),matrix_to_list(coded_input))

    #Add size to the start of the message and then fold the key and message together.
    shuffled_message_matrix = matrixize_raw_string(str(matrix_width) + list_to_string(combined_list),3)

    if(shuffled_message_matrix.size == 0):
        print("ERROR: The input contains unacceptable characters. Use only numbers, symbols, and letters.")
    else:
        #Encode with master key
        final_encoded_matrix = shuffled_message_matrix * master_key
        final_string = matrix_to_string(final_encoded_matrix)
        print(final_string)

#Decode:
else:
    in_string = input("Type your encoded message:\n")
    if (not(re.match("^([0-9]|\s|-)+$",in_string))):
        print("ERROR: This encoded message contains invalid characters")
    else:
        try:
            #Decode first layer using master key
            master_encoded_matrix = space_separated_string_to_matrix(in_string,master_key_width)
            combined_matrix = (master_encoded_matrix * get_inverse_matrix(master_key)).round().astype(np.int)
            combined_list = matrix_to_list(combined_matrix)

            #get the stored key size from the 0th element, then remove it.
            embedded_key_width = (combined_list[0]-2)
            combined_list = combined_list[1:]

            combined_list = convert_numbers_list(combined_list)
            decoded_string = separate_message_from_key(combined_list, embedded_key_width**2)
            print(decoded_string)

        except ValueError:
           print("ERROR: This encoded message is of an invalid size")


