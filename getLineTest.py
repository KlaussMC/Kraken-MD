def getLine(string, index):
	start=0
	end = 0

	start = string[:index+1].rfind("\n")
	end = index + string[index:].find("\n")

	# print (start, end)
	return string[start:end+1]

print ("\nLine: " + getLine(input("Type Text with at least two newLine chars: "), int(input("Enter Index: "))))