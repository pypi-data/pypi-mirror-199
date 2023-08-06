# Prerequisites
Python>= 3.7 


# Dependencies

`make develop` will install all other development dependencies. Please then install Lilypond (https://lilypond.org) as appropriate for your OS and ensure that lilypond  runs from the command line by running
```bash
$ lilypond --version
```

# Making a Contribution
## Forking and Cloning

To contribute to the repository, you will need to create your own fork of the repo, work off of that fork, and submit a pull request. Please see github's guide for [contibuting to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)

## Testing
Please run testing, formatting, and static analysis as follows
```
make test
make coverage
make format
make lint
```
If your changes  cause any existing tests to fail, please be sure to update these tests. Also, please ensure you add tests for any new features as appropriate.
## Final steps
Before making a pull request, please ensure that your commit messages are clear and summarize the changes made. 


# Makefile reference
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution