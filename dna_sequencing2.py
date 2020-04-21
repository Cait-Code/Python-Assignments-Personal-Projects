"""
Project #5: DNA Sequencing
--------------------------


A program that reads in a .txt file containing two strings of DNA and finds the longest set 
of valid DNA sequences using recursion, writing the output to a file.

and writes to another file

    DNA
    ----
    A DNA molecule is composed of two linear strands that coil around each other to form a double helix.
    Each DNA strand within the double helix is a long, linear molecule composed of smaller units called 
    nucleotdes. Each nucleotide is composed of one of nitrogen-containing nucleobases:
     - cytosine [C]
     - guanine [G] 
     - adenine [A]
     - thymine [T]
     
    The two helical strands are connected through interactions between pairs of nucleotides, also called 
    base pairs. Two types of base pairing occur:
     - A pairs with T.
     - C pairs with G.
    
    
"""

def valid_pair(nucleotide1, nucleotide2):
    """ function defines the valid base pairs """
    pairs = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }
    return pairs[nucleotide1] == nucleotide2

    
        
        
def compare_strands(strand1, strand2, size=0, dna_pair=['', '']):
    """Recursive function that compares the pairs of DNA sequences 
        and returns the longest set of DNA sequences"""
    
    if not strand1 or not strand2: 
        return size, dna_pair
    if not valid_pair(strand1[0], strand2[0]):    
        length, pair = size, dna_pair    # size = 0 pair = ['','']
        longest_length, longest_pair = compare_strands(strand1[1:], strand2[1:], 0, ['', '']) 
        if longest_length < length:
            longest_length = length
            longest_pair = pair
    else:
        temp_dna_pair = []
        temp_dna_pair.append(dna_pair[0] + strand1[0])
        temp_dna_pair.append(dna_pair[1] + strand2[0])
        size = size + 1
        longest_length, longest_pair = compare_strands(strand1[1:], strand2[1:], size, temp_dna_pair)
    
    return longest_length, longest_pair        
    

def main():    
    with open('dna.txt', 'r') as infile:                                               # open input file (2.5)
        n = int(infile.readline())     # first line, integer number n = the number of pairs of DNA to compare.
        for i in range(n):        # loops over n pairs of DNA sequences
            strand1 = infile.readline().strip('\n').upper() #
            strand2 = infile.readline().strip('\n').upper()
            dna_result = compare_strands(strand1, strand2)
            
            with open('dnaresults.txt', 'a') as outfile:  # open output file (2.5)
                outfile.write('DNA sequece pair {}:\n'.format(i))
                if dna_result[0] > 1:   # sequence size must be greater than 1
                    outfile.write('{}\n{}\n\n'.format(dna_result[1][0], dna_result[1][1]))
                else:
                    outfile.write('No matches found\n\n')
            outfile.close()    # close output file (2.5)
#    if outfile.closed:
#        print('dnaresults.txt is closed')
    infile.close()    # close input file (2.5)
#    if infile.closed:
#        print('dna.txt is closed')


main()