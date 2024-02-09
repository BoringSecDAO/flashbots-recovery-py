# Flashbots Recovery Py

![Python Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fvile%2Fflashbots-recovery-py%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&label=python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

A Python script that uses Flashbots to create Ethereum transaction bundles.
Based off of Flashbots' Python library [example](https://github.com/flashbots/web3-flashbots/blob/master/examples/simple.py).

## Requirements

1. Git - [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
   1. Check if you have Git installed with `git --version`
2. Python (>=3.10; <4) - [Install Python (Windows)](https://www.python.org/downloads/windows/), [Install Python (Linux)](https://docs.python.org/3/using/unix.html)
   1. Check if you have Python installed with `python3 --version`
3. Pip - [Install Pip](https://pip.pypa.io/en/stable/installation/)
   1. Check if you have Pip installed with `pip --version`
4. Poetry - [Install Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) (preferrably with [pipx](https://github.com/pypa/pipx))
   1. Check if you have Poetry installed with `poetry --version`

## Usage (Linux)

### Installing

#### Clone this repo

```bash
git clone https://github.com/vile/flashbots-recovery-py.git
cd flashbots-recovery-py
```

#### Install dependencies using Poetry

```bash
make deps
```

#### Rename .env.example

```bash
mv .env.example .env
```

Include your [Alchemy API key](https://www.alchemy.com/), compromised & gasser private keys, and recovery wallet address.

### Running the script

```bash
make start
```

## Usage (Windows)

### Installing

#### Clone this repo (Git)

```bash
git clone https://github.com/vile/flashbots-recovery-py.git
cd flashbots-recovery-py
```

#### Clone this repo (HTTPS)

#### Install dependencies using Poetry

```bash
poetry install --no-root
```

#### Rename .env.example

Remove the `.example` file extension from the `.env.example` file.
Include your [Alchemy API key](https://www.alchemy.com/), compromised & gasser private keys, and recovery wallet address.

### Running the script

```bash
poetry run py main.py
```

## Creating a Bundle

Coming soon