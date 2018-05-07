def processLink(link):
    if not link["isImage"]: #Creates Hyperlink
        str = "<a style='color:maroon;' target=\"_blank\" href=\""
        str += link["url"] + "\" "
        if link["title"]:
            str += "title=\"" + link["title"] + "\""
        str += ">"
        str += link["text"]
        str += "</a>"
        return " " + str
    else: #Creates Image (supposed to, anyway)
        # print (link)
        str = "<img src=\""
        str += link["url"] + "\" "
        if link["title"]:
            str += "alt=\"" + link["title"] + "\""
        str += ">"
        # print (str)
        return str
