import sys

source_file = str(sys.argv[1])

file = open(source_file, 'r')
mid = open('dict.txt', 'a+')
lines = file.readlines()

def isLineEmpty(line):
    return len(line.strip()) == 0
   
def is_line_ok(line): # TO MODIFY -- ADD CONDITIONS HERE
    tiret = '-' in line
    if tiret:
        return False
    return True

for line in lines:
    if is_line_ok(line):
        mid.write(line.upper())
   
        
