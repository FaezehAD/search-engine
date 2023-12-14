from hazm import Normalizer, word_tokenize, sent_tokenize
from nltk.util import ngrams
from decouple import config
import collections
import numpy as np
import difflib


def concat_string(input_list):
    output_string = ""
    for i in input_list:
        output_string = output_string + i + " "
    return output_string


def compare_strings(str1, str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    matches = matcher.get_matching_blocks()

    i = 0
    output = ""
    for match in matches:
        non_matching_part = str1[i : match.a]
        if non_matching_part:
            output += concat_string(non_matching_part)
            
        matching_part = str1[match.a : match.a + match.size]
        output += (
            "\n<span class='highlight'>" + concat_string(matching_part) + "</span>\n"
        )
        i = match.a + match.size
        print(concat_string(matching_part))

    non_matching_part = str1[i:]
    output += concat_string(non_matching_part)

    return output