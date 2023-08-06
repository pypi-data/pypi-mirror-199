# Loci SARIF Processor
The official SARIF output processor. Takes any results stored in a [SARIF](https://sarifweb.azurewebsites.net/) file and passes them to Loci Notes.

## Docs
https://loci-notes.gitlab.io/importers/sarif

## Installation
### Standard
`pip3 install loci-sarif`

### Latest
`pip3 install git+https://gitlab.com/loci-notes/loci-sarif`

### Development
* It is recommended that you use a virtualenv for development:
    * `virtualenv --python python3 venv`
    * `source ./venv/bin/activate`
* `python setup.py develop`
* Run with `loci-sarif`
