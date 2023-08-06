from pypdf import PdfMerger

def main(infiles, outfile):
	merger = PdfMerger()
	for pdf in infiles:
	    merger.append(pdf)
	merger.write(outfile)
	merger.close() 
