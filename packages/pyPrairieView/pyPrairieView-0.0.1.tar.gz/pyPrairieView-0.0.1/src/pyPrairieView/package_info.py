from importlib_metadata import metadata as _metadata


_meta = _metadata('pyPrairieView')

name = _meta["name"]
version = _meta['version']
author = _meta["author"]
maintainer = _meta["maintainer"]
