import pdfkit

def main(url, pdf):
	pdfkit.from_url(url, pdf) 
