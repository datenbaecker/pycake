# pycake

## Overview

`pycake` aims to provide simple functions to get Swiss Open Government
Data from different sources.

## Installation

This package can be both installed from PyPI or directly from the source code.

To install from PyPI, use:

```bash
pip install pycake
```

To install from the source code, run:

```bash
pip install git+https://github.com/datenbaecker/pycake.git@main
```

## Example usage
```bash
from pycake import get_address_features, metadata

search_for = ["Bundesstrasse 9 6003 Luzern", "Rämistrasse 71 8006 Zürich"]
adr_data = get_address_features(search_for)

metadata(adr_data)
```
```bash
from pycake import search_companies, metadata

company_info = search_companies("Datenbeacker GmbH")
company_details = company_info["company_details"]
related_companies = company_info["related_companies"]
company_person = company_info["company_person"]

metadata(company_details)
```

## Cheat Sheet

Take a look at the [cheat sheet](./cheatsheet.pdf) to get started.

## Remarks

The package is still at an early stage of development, so certain things
might not work as expected. Please file an issue with a minimal
reproducible example on
[GitHub](https://github.com/datenbaecker/pycake/issues) if you encounter
any problems.

Please give us a star if you like the package. Happy Coding!