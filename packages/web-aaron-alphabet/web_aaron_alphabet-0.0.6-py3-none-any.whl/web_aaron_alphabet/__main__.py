from argparse import ArgumentParser
import os
import tempfile
import string
import inspect
import sys
from contextlib import contextmanager, redirect_stderr, redirect_stdout

from . import harvesting
from . import converting
from . import merging




engines = dict()
for n, m in inspect.getmembers(converting):
    if not n.startswith('_'):
        engines[n] = m

parser = ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('URLs', nargs='+')
parser.add_argument('--outfile', '-o')
parser.add_argument('--force', '-f', default=False, action='store_true')
parser.add_argument('--engine', '-E', choices=engines.keys(), type=lambda k: engines[k])
parser.add_argument('--suffixes', '-s', nargs='+', action='append')


tailphrases = list(string.digits) + ["-"]

Harvesters = [
    harvesting.SuffixHarvester,
]

def crossiter(*, Iterator, infos):
    for info in infos:
        for ans in Iterator(**info):
            yield ans


def flatten_char(char):
    if char in string.ascii_letters:
        return char
    if char in string.digits:
        return char
    return '-'
def auto_pdf(url):
    url = url.split('/')[-1]
    url = "".join(flatten_char(x) for x in url)
    url = url.strip("-")
    while True:
        _url = url
        for phrase in tailphrases:
            if url.endswith(phrase):
                url = url[:-len(phrase)]
        if url == _url:
            break
    if url == "":
        url = "a"
    url += ".pdf"
    return url
def default_engine(ns):
    return 'weasyprint'
def main():
    ns = parser.parse_args()
    engine = ns.engine
    if engine is None:
        engine = engines[default_engine(ns)]
    outfile = ns.outfile
    urls = ns.URLs
    for Harvester in Harvesters:
        harvester = Harvester.from_namespace(ns)
        urls = harvester.main(urls)
    PDFs = list()
    with tempfile.TemporaryDirectory() as tmpdir:
        for url in urls:
            pdf = f"_{len(PDFs)}.pdf"
            pdf = os.path.join(tmpdir, pdf)
            try:
                with open(os.devnull, 'w') as fnull:
                    with redirect_stderr(fnull) as redirect:
                        engine.main(url=url, pdf=pdf)
            except Exception as e:
                continue
            else:
                if outfile is None:
                    outfile = auto_pdf(url)
                    print(outfile)
                print(url)
                PDFs.append(pdf)
        if not len(PDFs):
            sys.exit("Input is empty! ")
        if not ns.force:
            if os.path.exists(outfile):
                sys.exit(f"File {ascii(outfile)} exists already! ")
        merging.default.main(infiles=PDFs, outfile=outfile)



if __name__ == '__main__':
     main() 
