#from wkhtmltopdf import WKHtmlToPdf

def main(url, pdf):
    x = WKHtmlToPdf(
        url=url,
        output_file=pdf,
    )
    x.render()