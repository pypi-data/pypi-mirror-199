from setuptools import setup

name = "types-psycopg2"
description = "Typing stubs for psycopg2"
long_description = '''
## Typing stubs for psycopg2

This is a PEP 561 type stub package for the `psycopg2` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`psycopg2`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/psycopg2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6fd7e36e80e0448d9199d62d582c659c147be149`.
'''.lstrip()

setup(name=name,
      version="2.9.21.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/psycopg2.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['psycopg2-stubs'],
      package_data={'psycopg2-stubs': ['__init__.pyi', '_ipaddress.pyi', '_json.pyi', '_psycopg.pyi', '_range.pyi', 'errorcodes.pyi', 'errors.pyi', 'extensions.pyi', 'extras.pyi', 'pool.pyi', 'sql.pyi', 'tz.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
