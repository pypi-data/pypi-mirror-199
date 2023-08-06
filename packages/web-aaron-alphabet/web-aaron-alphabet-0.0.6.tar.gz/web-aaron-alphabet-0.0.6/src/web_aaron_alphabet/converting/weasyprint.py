import weasyprint

def main(url, pdf):
	weasyprint.HTML(url).write_pdf(pdf) 
