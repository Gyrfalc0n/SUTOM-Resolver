import sys, os

source_file = str(sys.argv[1])
dest_file = str(sys.argv[2])
data = data2 = ""
  
# Reading data from file1
with open(source_file) as fp:
    data = fp.read()
  
# Reading data from file2
with open(dest_file) as fp:
    data2 = fp.read()

data += data2
  
with open ('output.txt', 'w') as fp:
    fp.write(data)