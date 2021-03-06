from setuptools import setup, find_packages

print(find_packages(where="src"))

setup(
  name="hyplagrequest",
  version="0.1.0",
  packages=find_packages(),
  author='Kay Herklotz',
  author_email='kay.herklotz@gmail.com',
  description="HyplagRequestPy is a python package to provide an access point to Hyplag.",
  long_description="""\
HyplagRequestPy provides a python interface and CLI to communicate with the Hyplag backend.""",
  classifiers=[
      'Development Status :: 1 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: MacOS',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Topic :: Internet',
      'Topic :: Scientific/Engineering :: Information Analysis'
  ],
  keywords='Hyplag plagiarism detection CLI',
  url='https://github.com/ag-gipp/HyplagRequestPy',
  download_url='https://github.com/ag-gipp/HyplagRequestPy',
  license='Apache License 2.0',
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    "aiohttp>=3.8.0",
    "aiosignal",
    "async-timeout",
    "attrs",
    "certifi",
    "cffi",
    "chardet",
    "charset-normalizer",
    "cryptography",
    "frozenlist",
    "idna",
    "multidict",
    "pathlib",
    "pycparser",
    "pydantic",
    "PyJWT",
    "python-dotenv",
    "requests",
    "requests-toolbelt",
    "typing-extensions",
    "urllib3",
    "yarl"
  ],
)