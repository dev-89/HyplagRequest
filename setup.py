from setuptools import setup, find_packages

print(find_packages(where="src"))

setup(
  name="hyplagrequest",
  version="0.0.1",
  package_dir={"": "src"},
  packages=find_packages(where="src"),  author='Kay Herklotz',
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
    "aiohttp==3.8.0",
    "aiosignal==1.2.0",
    "async-timeout==4.0.0",
    "attrs==21.2.0",
    "certifi==2020.12.5",
    "cffi==1.15.0",
    "chardet==4.0.0",
    "charset-normalizer==2.0.7",
    "cryptography==35.0.0",
    "frozenlist==1.2.0",
    "idna==2.10",
    "multidict==5.2.0",
    "pathlib==1.0.1",
    "pycparser==2.20",
    "pydantic==1.8.2",
    "PyJWT==2.3.0",
    "python-dotenv==0.17.1",
    "requests==2.25.1",
    "requests-toolbelt==0.9.1",
    "typing-extensions==3.10.0.2",
    "urllib3==1.26.4",
    "yarl==1.7.0"
  ],
)