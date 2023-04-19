#os library is imported to compare file sizes
import os

#each object in this class represents one node in the huffman tree
class HuffmanNode:

    def __init__(self,left,right):
        #Each node is created with a left and right child
        self.left = left
        self.right = right

    def getNodeLeft(self):
        
        return self.left

    def getNodeRight(self):
        
        return self.right

#this class is used to store the dictionaries of already encoded files to be decoded
class EncodedFiles:

    def __init__(self):
        #no encoded file dictionaries initially
        #dictionary codes relates encoded files by name to their codes
        self.codes = {}

    def addCode(self,filename,codetree):
        #adds a dictionary of huffman codes to the dictionary codes  
        self.codes.update({filename: codetree})

    def getCode(self,filename):
        
        return self.codes.get(filename)

#takes filename.txt and existing encoded files dictionary and encodes file appending new codes with compressed file
#also calculates percentage file size decrease
def HuffmanEncoder(filename, ExistingDicts):
    
    #find frequencies of characters in file
    frequencies = FrequencyCalc(filename)
    #order frequencies
    sortedfrequencies = sorted(frequencies.items(), key=lambda item: item[1])
    #create huffman-ordered binary tree using sorted frequencies
    tree = HuffmanTree(sortedfrequencies)
    #assign codes to binary tree
    encodedtree = CodeAssigner(tree[0][0])
    #compress file using codes
    CompressToFile(filename,encodedtree)
    #add codes information to encoded files dictionary for decoding
    ExistingDicts.addCode(filename[:-4] + ".bin", encodedtree)
    #calculate size decrease and print results
    sizedecrease = (os.stat(filename[:-4] + ".bin").st_size / os.stat(filename).st_size) * 100
    print("Compressed to", sizedecrease, "%", "of original file size")
    print("Successfully compressed file ", filename, " as ", filename[:-4] + ".bin")

def FrequencyCalc(filename):
    #does not account for case
    frequencies = {}
    file =open(filename, 'r', encoding='utf-8')
    while True:
        
        char = file.read(1)
        if not char:
            #if char is null file end has been reached
            break
        elif char not in frequencies:
            
            frequencies[char] = 0
        #otherwise add to frequency of char
        frequencies[char] += 1
    file.close()
    return frequencies

def HuffmanTree(sortedfrequencies):

    while len(sortedfrequencies) > 1:
        #take lowest freq and assign them as children to node
        #as frequencies are sorted index 0 and 1 are lowest freq
        key1, val1 = sortedfrequencies[0]
        key2, val2 = sortedfrequencies[1]
        #remove the children nodes from the list
        sortedfrequencies = sortedfrequencies[2:]
        node = HuffmanNode(key1,key2)
        sortedfrequencies.append((node, val1 + val2))
        #resort the list with the new node
        sortedfrequencies = sorted(sortedfrequencies, key=lambda x: x[1])  
    return(sortedfrequencies)

def CodeAssigner(node, string=""):
    
    if (isinstance(node,str)):
        #if node is string then bottom of tree reached
        #work recursively back up tree to add char(node) and code to dict
        return {node: string}
    treevalues = {}
    #try to add the children of the current node to the dict with + 0 or + 1 to code
    treevalues.update(CodeAssigner(node.getNodeLeft(), string + "0"))
    treevalues.update(CodeAssigner(node.getNodeRight(), string + "1"))
    return treevalues

def CompressToFile(filename, encodedtree):
    
    file = open(filename, 'r', encoding='utf-8')
    encodedstring = ""
    while True:

        char = file.read(1)
        if not char:
            
            break
        #add code for char to string to be written to file
        encodedstring += encodedtree.get(char)
    file.close()
    #create bytearray to store binary data
    encodedbytes = bytearray()
    #append code data to bytearray each byte
    for i in range(0, len(encodedstring), 8):

        encodedbytes.append(int(encodedstring[i:i+8], 2))
    #write to compressed file
    compressedfilename = filename[:-4] + ".bin"
    file = open(compressedfilename, 'wb')    
    file.write(encodedbytes)
    file.close()

#Takes filename.bin and existing encoded files dictionary and decodes file if dictionary exists for file
def HuffmanDecoder(filename, ExistingDicts):
    
    file = open(filename, 'rb')
    #read file as byte data and turn into string of codes
    bytedata = bytearray(file.read())
    todecode = ''.join([bin(i)[2:].zfill(8) for i in bytedata])
    codes = ExistingDicts.getCode(filename)
    file.close()
    decoded = ""
    currcode = ""
    for i in todecode:
        
        if not i:
        
            break
        #add char to code to search for
        currcode += i
        for key, val in codes.items():
            #if currcode match found append code value to decoded file string
            if currcode == val:

                decoded += str(key)
                currcode = ""
    #write new .txt file with decompressed information
    file = open(filename[:-4] + "new.txt", 'wb')
    file.write(decoded.encode("utf-8"))
    file.close()
    print("Successfully decompressed file ", filename, " as ", filename[:-4] + "new.txt")

def main():
    
    ExistingDicts = EncodedFiles()
    #take user input to encode or decode file
    while True:
        
        task = input("Encode or Decode: ")
        if task == "Encode":
        
            filename = input("Enter filename (.txt): ")
            HuffmanEncoder(filename,ExistingDicts)
        elif task == "Decode":
        
            filename = input("Enter filename (.bin): ")
            HuffmanDecoder(filename,ExistingDicts)
        else:
        
            print("Bad input")

if __name__ == "__main__":
    main()