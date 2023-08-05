![PyPI](https://img.shields.io/pypi/v/wl-utilities)

Utility code to be used in the WEAVE-QAG/SV environment

This package is called `wl-utilities` on PyPI and can be installed with `pip install wl-utilities` and then imported with `import wl_utilities`
This package is a collaborative effort and will comprise the scientific code that allows the QAG tests and SV to run. `wl_utilities` will be a dependency of those projects. `wl_utilities` should not use `weaveio` or `qag` packages.

Please see [setup](#setup) for setting up github 

# Workflow

There will be 2 branches in use on this repository: 

* `main` - where the production-ready version exists and which is uploaded automatically to PyPI for use by everyone.
* `develop` - where changes and merges all take place before merging into the `main` branch

### Setup git
To setup git to deal with collaboration. This will allow you to use our custom git aliases, shortcuts that make your life easier.
1. On github click `Fork`. This creates a copy of `wl_utilities` for you to work on (WARNING: make sure your repo is called "wl_utilities" and not "utilities")
2. Check that your machine can use [ssh key authentication with github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
3. On the pc where you develop QAG tests, `cd` somewhere for development on this `wl_utiltities` repository. There is no need to create a `wl_utilities` directory.
4. git clone `git@github.com:YOURUSERNAME/wl-utilities.git` (the link can be found under the green `code` button on your github page)
5. `cd wl_utilities` on your local machine. 
6. Activate your development environment (maybe: `conda activate weaveio` or similar)
7. Install helper aliases `chmod +x setup.sh && ./setup.sh`


## To add/modify this repository with your own changes and improvements please use this workflow:

0. Activate your development environment (maybe: `conda activate weaveio` or similar)
1. Pull the latest updates: `git sync-fork`
2. Create a new branch for your changes to live on: `git fork-branch my-clever edit`
3. Make your changes on this branch
4. View what has happened: `git status`
5. Add your changes to be commited: `git add <file1> <file2> ...` 
6. View what has changed: `git status`
7. Save your changes: `git commit -m "description of changes"`
8. Wait for automated checks to complete (and then commit again if necessary: `git commit -m "description of changes"`) 
9. Push changes to your fork only: `git push`
10. Open a pull request on your github page (https://github.com/USERNAME/wl-utilities), click contribute->open pull request, and check "allow edits by maintainer"

*You can also use `gh pr create --fill` to open a pull request on command line. This requires the [github cli utility](https://github.com/cli/cli) which can be installed with  apt-get or conda*

In general we should be writing code like this:

	* Play with code in jupyter notebook (all weaveio queries, new functions, plotting)
	* Refactor this notebook and the wl_utilities module to move new functions/plotting to wl_utilities
	* Run notebook to make sure its still doing what you want

All changes therefore end up in the `develop` branch of the weave-lofar shared repo.

All pull requests will be reviewed before merging, so we can limit mistakes.

## Structure
The structure of this package will be:
```
wl_utilities/
  misc/  # for random short but useful snippets
  spectrum/  # for anything that processes spectra
    e.g. cross-correlation.py
    e.g. reduction.py
  stats/  # for anything that looks like a statistical test
    e.g. zscores.py
  
```
We will not use separate folders for individual's code since the objective is to put them together and not repeat.


# Rules:
* This repo will be autoformatted according to `black` on server-side
* No change is merged with the `main` branch until approved by "enough" people
* Keep the code as modular as possible 
