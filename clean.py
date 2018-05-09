import re
def clean (code):
    return code.replace("\n", '').replace("\t", '')
    #cleanup work to be done, such as removing lone escape chars and formatting in code and incomplete tags
