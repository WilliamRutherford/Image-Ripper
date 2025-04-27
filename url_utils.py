
import urllib.parse

'''
Given a URL string, get a dictionary representing the query parameters
example: 
https://example.com/path/to/page?name=ferret&color=purple
->
{"name" : "ferret", "color" : "purple"}

'''
def get_query_params(url : str, decode_percents : bool = True) -> dict:
    param_portion_list = url.split("?")

    # If the url has no query parameters, we return an empty dictionary
    if(len(param_portion_list) == 1):
        return {}
    
    # We get the last string in the list, in case for some reason there's an errant question-mark before the params
    param_portion = param_portion_list[-1]
    params = param_portion.split("&")

    return_dict = {}
    for param_def in params:
        def_split = param_def.split("=", 1)
        key = def_split[0]
        val = def_split[1]
        if(decode_percents and ('%' in val)):
            return_dict[key] = percent_decoding(val)
        else:
            return_dict[key] = val
    
    return return_dict
    

'''
Given a percent-encoded string (used in query parameters) into a regular string.
example: 
https%3A%2F%2Fimg2.bonhams.com%2Fimage%3Fsrc%3DImages%2Flive%2F2024-05%2F14%2F189850-172-4.jpg
-> 
https://img2.bonhams.com/image?src=Images/live/2024-05/14/189850-172-4.jpg
'''
def percent_decoding(input : str) -> str:
    return urllib.parse.unquote(input)