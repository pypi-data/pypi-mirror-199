#pip install PyPDF2 
from PyPDF2 import PdfFileMerger

def main(infiles, outfile):
	#Create an instance of PdfFileMerger() class
	merger = PdfFileMerger()

	#Iterate over the list of the file paths
	for pdf_file in infiles:
	    #Append PDF files
	    merger.append(pdf_file)

	#Write out the merged PDF file
	merger.write(outfile)
	merger.close()