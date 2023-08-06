# acdh-transkribus-utils

[![PyPI version](https://badge.fury.io/py/acdh-transkribus-utils.svg)](https://badge.fury.io/py/acdh-transkribus-utils)
[![flake8 Lint](https://github.com/acdh-oeaw/acdh-transkribus-utils/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-transkribus-utils/actions/workflows/lint.yml)
[![Test](https://github.com/acdh-oeaw/acdh-transkribus-utils/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-transkribus-utils/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/acdh-oeaw/acdh-transkribus-utils/branch/master/graph/badge.svg?token=QOY62C0X5Y)](https://codecov.io/gh/acdh-oeaw/acdh-transkribus-utils)

A python package providing some utility functions for interacting with the [Transkribus-API](https://transkribus.eu/wiki/index.php/REST_Interface)


## Installation

`pip install acdh-transkribus-utils`


## Usage

### Authentication

Set Transkribus-Credentials as environment variables: 

```bash
export TRANSKRIBUS_USER=some@mail.com
export TRANSKRIBUS_PASSWORD=verysecret
```
(or create a file called `env.secret` similar to `env.dummy` and run  `source export_env_variables.sh`)
you can pass in your credentials also as params e.g. 

```python
from transkribus_utils.transkribus_utils import ACDHTranskribusUtils

client = ACDHTranskribusUtils(user="some@mail.com", password="verysecret")
```

### Download METS files from Collection

```python
from transkribus_utils.transkribus_utils import ACDHTranskribusUtils

COL_ID = 51052
client = ACDHTranskribusUtils()
client.collection_to_mets(COL_ID)
# downloads a METS for each document in the given collection into a folder `./{COL_ID}

client.collection_to_mets(COL_ID, file_path='./foo')
# downloads a METS for each document in the given collection into a folder `./foo/{COL_ID}

client.collection_to_mets(COL_ID, filter_by_doc_ids=[230161, 230155])
# downloads only METS for document with ID 230161 and 230155 into a folder `./{COL_ID}
```