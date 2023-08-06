# Contributing to `texonomy`

Hi! Thanks for your interest in `texonomy`.

## Issues

### Opening a new issue

Feel free to open up an issue if you encounter a bug with the program or if
you'd like to request a feature. Before you open an issue, please do the
following:

- Scroll through the
[existing issues](https://github.com/basseches/texonomy/issues) to see if the issue
already exists.
- Ensure you've read all the documentation in the [README.](README.md)
- Use the issue templates provided.

### Solve an issue

Scan through the
[existing issues](https://github.com/basseches/texonomy/issues) to find one
that interests you. You can narrow down the search using `labels` as filters.

## Making changes

To make changes, create a [pull request.](#opening-a-pull-request) Before
opening a PR to `texonomy`, you should read these guidelines.

### Development

#### Prerequisites

You should have all the dependencies referenced in the [README](README.md)
installed.

#### Setting up

1. Fork the repository.
- Using the command line:
  - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository)
  so that you can make your changes without affecting the original project
  until you're ready to merge them.
- Using GitHub Desktop:
  - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop)
  will guide you through setting up Desktop.
  - Once Desktop is set up, you can use it to
  [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

2. Install or update `python` to >= version 3.8.

3. Install the package locally by running the following:

```sh
sudo make develop && make build && make install
```

If the library was correctly installed, you should be able to type
`import texonomy` into the Python interpreter without an issue.

4. Create a working branch and start with your changes!

#### Testing

For the unit tests, run `make test` or `make coverage` (for coverage report) at
the top-level directory. For the integration tests, run `make test` in
`texonomy/tests/integration_tests`. The output will be stored in
`texonomy/tests/integration_tests/pdf` and
`texonomy/tests/integration_tests/tex`.

#### Linting and formatting

Run `make lint` at the top-level directory to lint, and `make format` to
format.

### Opening a pull request

You must do these things before opening a PR to `texonomy`. The PR will not be
considered if any tests or checks fail.

- [ ] Test your code and ensure that it works as expected. If you think it
necessary, provide your own unit/integration tests for the code you're adding.
- [ ] Run the preexisting tests to ensure backwards compatibility.
- [ ] Lint and format the code.
- [ ] Open a PR, including a description of what your change does and why it
should be merged.
- [ ] [Link your PR to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
if you are solving one.
- [ ] Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork)
so the branch can be updated for a merge.
