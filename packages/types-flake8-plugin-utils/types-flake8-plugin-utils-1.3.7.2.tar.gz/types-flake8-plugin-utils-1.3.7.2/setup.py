from setuptools import setup

name = "types-flake8-plugin-utils"
description = "Typing stubs for flake8-plugin-utils"
long_description = '''
## Typing stubs for flake8-plugin-utils

This is a PEP 561 type stub package for the `flake8-plugin-utils` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-plugin-utils`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-plugin-utils. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6fd7e36e80e0448d9199d62d582c659c147be149`.
'''.lstrip()

setup(name=name,
      version="1.3.7.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-plugin-utils.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_plugin_utils-stubs'],
      package_data={'flake8_plugin_utils-stubs': ['__init__.pyi', 'plugin.pyi', 'utils/__init__.pyi', 'utils/assertions.pyi', 'utils/constants.pyi', 'utils/equiv_nodes.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
