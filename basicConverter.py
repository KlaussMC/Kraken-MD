def convertBasic(code):
	converted = ""
	i=1
	bold = False
	italic = False
	inlineCode = False

	while i < len(code) - 1:
		if (code[i] != '\\'):
			if (code[i] == "_" and not code[i+1] == "_") or (code[i] == "*" and not code[i+1] == "*"):
				italic = not italic
				if not italic:
					converted += "</i>"
				else:
					converted += "<i>"
			elif code[i] == "`" and not code[i+1] == "`":
				inlineCode = not inlineCode
				i+=1
				if not inlineCode:
					converted += "</code></span>"
				else:
					converted += "<span style='color: maroon;'><code>"

			elif code[i] == "\n":
				if inlineCode:
					converted += "</code></span>"
				inlineCode = False

			elif code[i] + code[i + 1] == "**" or code[i] + code[i+1] == "__":
				i+=1
				bold = not bold
				if not bold:
					converted += "</b>"
				else:
					converted += "<b>"
			else:
				converted += code[i]
		else:
			converted = converted[:-1]
			converted += code[i]

		i+=1
	# print (code)
	return converted
