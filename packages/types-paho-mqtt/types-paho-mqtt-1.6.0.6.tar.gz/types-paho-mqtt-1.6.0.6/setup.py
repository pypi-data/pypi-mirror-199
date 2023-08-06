from setuptools import setup

name = "types-paho-mqtt"
description = "Typing stubs for paho-mqtt"
long_description = '''
## Typing stubs for paho-mqtt

This is a PEP 561 type stub package for the `paho-mqtt` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`paho-mqtt`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/paho-mqtt. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6fd7e36e80e0448d9199d62d582c659c147be149`.
'''.lstrip()

setup(name=name,
      version="1.6.0.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/paho-mqtt.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['paho-stubs'],
      package_data={'paho-stubs': ['__init__.pyi', 'mqtt/__init__.pyi', 'mqtt/client.pyi', 'mqtt/matcher.pyi', 'mqtt/packettypes.pyi', 'mqtt/properties.pyi', 'mqtt/publish.pyi', 'mqtt/reasoncodes.pyi', 'mqtt/subscribe.pyi', 'mqtt/subscribeoptions.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
