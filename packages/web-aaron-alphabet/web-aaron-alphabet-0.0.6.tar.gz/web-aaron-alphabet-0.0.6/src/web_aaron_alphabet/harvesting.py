import inspect

class _Harvester:
    @classmethod
    def from_namespace(cls, ns):
        sig = inspect.signature(cls.__init__)
        parameters = list(dict(sig.parameters).items())
        n, m = parameters.pop(0)
        assert n == 'self'
        kwargs = dict()
        for n, m in parameters:
            kwargs[n] = getattr(ns, n)
        return cls(**kwargs)
    @classmethod
    def crossiter(*, Iterator, infos):
        for info in infos:
            for ans in Iterator(**info):
                yield ans
    def __init__(self):
        raise NotImplementedError()
    def main(self, urls):
        for url in urls:
            for ans in self.run(url):
                yield ans
    def run(self, url):
        raise NotImplementedError()

class SuffixHarvester(_Harvester):
    def __init__(self, *, suffixes):
        self.suffixes = suffixes
    def _run(self, urls, suffixes):
        for url in urls:
            yield url
            for suffix in suffixes:
                yield url + suffix.strip()
    def run(self, url):
        urls = iter([url])
        if self.suffixes is None:
            return urls
        for suffixes in self.suffixes:
            urls = self._run(urls, suffixes)
        return urls




