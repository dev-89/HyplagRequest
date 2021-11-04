# Python Hyplag Request

## Description

This module handles hyplag requests and can be used for projects sending requests to Hyplag or as a CLI (TODO!)

## Usage

Rename the .env-example file to .env and adjust the current parameters according to your settings. The functionality of the module is given with the HyplagRequest class.

### Using the interface

The HyplagRequest interface works over the __init__ and __call__ methods. In __init__ basic initialisation is done. The __call__ method is the used interface. By passing parameters to the __call__ method the class constructs a request to the Hyplag Backend. For several parameters the flag -1 has a special meaning, since HyplagRequest request will try to fetch already generated data. One example would be to upload a file and retrieve the authors. The call would look something like as follows:

```python
hypreq = HyplagRequest()
requestCall = hypreq(_uploadDocument='/path/to/doc.pdf', _getDocumentAuthors=-1)
```

This call would retrieve the authors of the uploaded document where as 

```python
hypreq = HyplagRequest()
requestCall = hypreq(_uploadDocument='/path/to/doc.pdf', _getDocumentAuthors=7)
```

would upload the document and retrieve the authors of document with ID 7.

### Using the CLI

The HyplagRequest CLI is strongly based upon the HyplagRequest __call__ structure and mainly offers convenience. Uploading files can be done by specifing one or more paths to documents under the -d flag or an entire directory under the -d flag. Note that most flags operate in append mode, i. e. the call

```bash
python3 main.py -d file1.pdf -d file2.pdf -q -1 -q 21 - 42
```

would upload the files file1.pdf and file2.pdf to Hyplag as well as get the full data for them as well as for documents with ID 21 and 42.

## Module Structure

The structure of Python HyplagRequest is based upon the API structure of Hyplag. As for now the functionality is limited to the RecVis usecase, but will be extended to support all Hyplag API calls.

## TODO

 * CLI
 * Clean configuration and constant handling
 * * configuration file for logging
   * HyplagRequest configuration file next to .env
   * seperate storage of constants
 * Implement the following controll structures:
 * * account
   * admin
   * collusion
   * detection
   * document reference
   * formula
   * grobid
   * image
   * log
   * pars-cit
   * post process
   * re-indexing
   * reference migration
   * statistic