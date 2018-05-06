import re
def trimHTML(code):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', code)
    return cleantext
