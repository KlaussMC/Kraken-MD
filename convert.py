import re
from link import *
from bs4 import BeautifulSoup

from basicConverter import *
from clean import *

def convert(code):
	# code += "\n"
	code = "\n" + code + "\n"
	converted = ""

	bold = False
	italic = False
	inlineCode = False
	bigCode = False
	link = {"isImage": False, "start": 0, "end": 0, "url": "", "titleStart": 0, "titleEnd": 0, "title": "", "urlStart": 0, "urlEnd": 0, "text": ""}
	# lists = []

	i=1
	while i < len(code) - 1:
		if not code[i-1] == "\\":
			if code[i] == "\n":
				converted += "<br/>"
			if within(i, len(code), 3) and code[i] + code[i+1] + code[i+2] == '```':
				i+=2
				# print ("Big Code")
				bigCode = not bigCode
				if bigCode:
					converted += "<br/><div style='background-color: grey;'><code>"
				else:
					converted += "</code></div>"
			else:
				if i < len(code)-4:
					if code[i] + code[i+1] + code[i+2] == "---" or code[i] + code[i+1] + code[i+2] == "***":
						i+=3
						converted += "<hr>"
				if (code[i] == "_" and not code[i+1] == "_") or (code[i] == "*" and not code[i+1] == "*"):
					italic = not italic
					i+=1
					if not italic:
						converted += "</i>"
					else:
						converted += "<i>"
				if code[i] == "`" and not code[i+1] == "`":
					inlineCode = not inlineCode
					i+=1
					if not inlineCode:
						converted += "</code></span>"
					else:
						converted += "<span style='color: maroon;'><code>"

				if code[i] == "\n":
					if inlineCode:
						converted += "</code></span>"
					inlineCode = False

				if code[i] + code[i + 1] == "**" or code[i] + code[i+1] == "__":
					i+=1
					bold = not bold
					if not bold:
						converted += "</b>"
					else:
						converted += "<b>"

				else:
					if getLine(code, i).split()[0][0] == "#":
						headernum = getLine(code, i).split()[0].count("#")
						tmp = "<h" + str(headernum) + ">" + getLine(code, i)[headernum-1:][headernum:] + "</h" + str(headernum) + ">"
						converted += tmp

						i += len(getLine(code, i))

					if getLine(code, i).split()[0][0] == ">":
						# tmp =
						converted += "<br><span style='color: grey; background-color: grey;'>|</span>" + (" " + convertBasic(getLine(code, i).strip()))
						i += (len(getLine(code, i)))

					if getLine(code, i).split()[0][0:2] == "-" or getLine(code, i).split()[0][0:2] == "*":
						tmp = convertBasic(getLine(code, i).strip())

						if getLine(code, i).split()[0][0:2] == "*":
							converted = converted[:-3]

						converted += "<ul><li>" + (" " + tmp ) + "</li></ul>"
						# print (converted)
						i += len(getLine(code, i))

					if code[i] == "[":
						link["start"] = i
						link["isImage"] = code[i-1] == "!"

					if code[i] == "]":
						link["end"] = i
						link["text"] = code[link["start"]+1:link["end"]]
						# print (link["text"])

					if code[i] == "\"":
						# if not link["start"] == 0 and link["end"] == 0:
						if not link["titleStart"] == 0:
							link["titleEnd"] = i
							link["title"] = code[link["titleStart"]+1:link["titleEnd"]]
							# print (link["title"])
						else:
							link["titleStart"] = i

					if code[i] == "(":
						if link["start"]:
							link["urlStart"] = i
					if code[i] == ")":
						if link["start"]:
							link["urlEnd"] = i
							link["url"] = code[link["urlStart"]+1:link["urlEnd"] - (len(link["title"]))]
							if link["title"]:
								link["url"] = link["url"][:-3]
							# print (link["url"])

							converted=converted[:0-(len(code[link["start"]:i]))]
							i+=1
							converted=converted[:-1]
							converted += processLink(link)
							link = {"start": 0, "end": 0, "url": "", "titleStart": 0, "titleEnd": 0, "title": "", "urlStart": 0, "urlEnd": 0, "text": ""}

					converted += code[i]
		else:
			converted = converted[:-1]
			converted += code[i]

		i+=1
	return "<html>" + clean(converted) + "</html>"

def getLine(code, i):
	return code[(code[:i].rfind("\n")+1):i + code[i + 1:].find("\n")+1]

def join(arr):
	newStr = ""
	for i in arr:
		newStr += i + " "
	return newStr[:-1]

import trim

def wrapMatches(str, match):
	if not str.find(match) == -1:
		newStr = str[:str.find(match)]
		lastFindIndex = 0
		# for i in range(len(re.findall(match, str))):
		#
		# 	# soup.find("h1")
		#
		# 	newStr += "<span style='color: yellow;'>"
		# 	lastFindIndex = str.find(match, lastFindIndex+1)
		# 	newStr += str[lastFindIndex:lastFindIndex+len(match)]
		# 	newStr += "</span>"
		# 	newStr += str[lastFindIndex+len(match):str.find(match, lastFindIndex+1)]

		# print (re.findall(r">.*?<", str))



		return newStr
	else:
		return str

def within(var, max, range):
	return var <= max - range
