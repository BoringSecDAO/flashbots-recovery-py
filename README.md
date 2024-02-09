# Flashbots Recovery Py



## Usage

### Clone this repo


Just download via HTTP for now

### Running the script

1. Install Python (>=3.10; <4)
2. Install Pip
3. Install Pipx ([here](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx))
4. Install Poetry with Pipx ([here](https://python-poetry.org/docs/#installing-with-pipx))
   1. `pipx install poetry`
5. Install project dependencies using Poetry
   1. `make deps` OR `poetry install --no-root`
6. Rename `.env.example` to `.env` and include ALL relevant private keys and addresses
7. Create bundle in `./bundle/bundle.py` (maybe be necessary to add ABIs to `./utils/abi.py`)
8. Change gas price and tip in `./utils/constants.py::L14-L15` as required
9. Run script
   1. `make start` OR `poetry run python3 main.py`