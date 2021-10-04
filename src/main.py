import sys
from git import Repo
from collections import defaultdict
import mimetypes

def main():
    mimetypes.init()
    path = "../../"
    extension = ""
    arg_author = ""
    if(len(sys.argv) > 1):
        if(len(sys.argv) % 2 == 0):
            print("Please provide tags")
            return
        for i in range(1,len(sys.argv),2):
            if(sys.argv[i] == "--path"):
                path += sys.argv[i+1]
            elif(sys.argv[i] == "--extension"):
                extension = sys.argv[i+1]
            elif(sys.argv[i] == "--author"):
                arg_author = sys.argv[i+1]
            else:
                print("Invalid Argument: " + sys.argv[i])
                return;

    repo = Repo(path)
    files = repo.git.ls_files().split("\n")
    authors = defaultdict(int)
    author_files = []
    for file in files:
        pushed_author_file = False
        textBased = False
        if(extension != ""):
            textBased = file.endswith(extension)
        else:
            try:
                textBased = mimetypes.guess_type(file)[0].startswith('text')
            except AttributeError:
                continue
        if(not textBased):
            continue
        try:
            lines = repo.git.blame(file).split("\n")
        except ValueError:
            continue

        for line in lines:
            author = getAuthor(line.split("(")[1].split(")")[0])
            if(arg_author != "" and not pushed_author_file and author == arg_author):
                pushed_author_file = True
                author_files.append(file)
            authors[author] += 1

    totalLinesSum = sum(authors.values())
    authorsSorted = sorted(authors, key=authors.get, reverse=True)
    print("Total Lines: " + str(totalLinesSum))
    if(arg_author != ""):
        for file in author_files:
            print(file)
        return
    for i,authorName in enumerate(authorsSorted):
        print(str(i+1) + ": %.2f" % (authors[authorName]/totalLinesSum*100) + "%, "+ authorName)

def getAuthor(line):
    chunks = list(filter(lambda x: x != '',line.split(" ")))
    author = chunks[0]
    for i in range (1,len(chunks)):
        if(i >=len(chunks)-4):
            break
        author = author + " " + chunks[i]

    return author


if __name__ == '__main__':
    main()
