# CaosDB-Crawler

## Welcome

This is the repository of the CaosDB-Crawler, a tool for automatic data
insertion into [CaosDB](https://gitlab.com/caosdb/caosdb-meta).

This is a new implementation resolving  problems of the original implementation
in [caosdb-advancedtools](https://gitlab.com/caosdb/caosdb-advanced-user-tools)

## Setup

Please read the [README_SETUP.md](README_SETUP.md) for instructions on how to
setup this code.


## Further Reading

Please refer to the [official documentation](https://docs.indiscale.com/caosdb-crawler/) of the CaosDB-Crawler for more information.

## Contributing

Thank you very much to all contributers—[past, present](https://gitlab.com/caosdb/caosdb/-/blob/dev/HUMANS.md), and prospective ones.

### Code of Conduct

By participating, you are expected to uphold our [Code of Conduct](https://gitlab.com/caosdb/caosdb/-/blob/dev/CODE_OF_CONDUCT.md).

### How to Contribute

* You found a bug, have a question, or want to request a feature? Please 
[create an issue](https://gitlab.com/caosdb/caosdb-crawler).
* You want to contribute code?
    * **Forking:** Please fork the repository and create a merge request in GitLab and choose this repository as
      target. Make sure to select "Allow commits from members who can merge the target branch" under
      Contribution when creating the merge request. This allows our team to work with you on your
      request.
    * **Code style:** This project adhers to the PEP8 recommendations, you can test your code style
      using the `autopep8` tool (`autopep8 -i -r ./`).  Please write your doc strings following the
      [NumpyDoc](https://numpydoc.readthedocs.io/en/latest/format.html) conventions.
* You can also contact us at **info (AT) caosdb.de** and join the
  CaosDB community on
  [#caosdb:matrix.org](https://matrix.to/#/!unwwlTfOznjEnMMXxf:matrix.org).


There is the file `unittests/records.xml` that servers as a dummy for a server state with files.
You can recreate this by uncommenting a section in `integrationtests/basic_example/test_basic.py`
and rerunning the integration test.

## Integration Tests

see `integrationtests/README.md`

## Contributers

The original authors of this package are:

- Alexander Schlemmer
- Henrik tom Wörden
- Florian Spreckelsen

## License

Copyright (C) 2021-2022 Research Group Biomedical Physics, Max Planck Institute
                        for Dynamics and Self-Organization Göttingen.
Copyright (C) 2021-2022 IndiScale GmbH

All files in this repository are licensed under a [GNU Affero General Public
License](LICENCE) (version 3 or later).
