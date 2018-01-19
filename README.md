# MARC Dataframes
This project contains transformers for [MARC 21 metadata](https://www.loc.gov/marc/bibliographic/) for NLP applications.
Transformers output [Pandas data frames](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas-dataframe) for downstream processing.

## Usage

```python
from marc_dataframes import (load, transform, marc, transformers, corpora)

marc = load('marc.xml', fields = [marc.MainEntry, marc.Title, marc.Edition])
vectorized = transform(marc, transformer = transformers.NGrams(1, idf = true, corpus = corpora.LOC2014))
```

## Contributing

Contributions to this project are encouraged.

Some project ideas:
- Transformations based on text embeddings (Word2Vec, Glove, etc).
- A bag-of-words built from the Library of Congress 2014 MARC dataset.
- Use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html) to verify assumptions of a particular transformation.
- Compose a dataset of records labeled by their [FRBR Group 1](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records) relationships.

## Sharing

```
Copyright (c) 2018, The Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
