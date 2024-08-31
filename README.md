# Bindfit datapackage for opendata.studio

Bindfit is a binding constant fitting tool designed to work with classical supramolecular titration data obtained from NMR, UV, Fluorescence and other methods.

* 🗒️ [Bindfit datapackage documentation](https://docs.opendata.fstudio/v/bindfit-datapackage/)
* 💻 [Bindfit Python library GitHub](https://github.com/opendatastudio/bindfit)

## Example usage
```
ods reset                                   # Clear any previous outputs
ods load bindfit data ./data/nmr11.csv      # Load input data
ods set-param fitModelParams k 314          # Set initial parameter guess
ods set-arg fitMethod "bfgs"                # Set fit method
ods run                                     # Run algorithm
ods view fitGraphMatplotlib                 # View fit graph
ods view-table fitCoefficients              # View fit coefficients table
```

## Development

### Requirements

* Docker
* Python (to run CLI)
* [opendatastudio/cli](https://github.com/opendatastudio/cli)
* [opendatastudio/containers](https://github.com/opendatastudio/containers)

### Set up pre-commit hooks

Set up included Flake (`flake.nix`) with direnv (`.envrc`) to automatically load development environment.

Install/run pre-commit hooks:
```
pre-commit install
pre-commit run --all-files
```

### Build execution container

Build base execution container:
```
# Navigate to opendatastudio/containers repository
cd python-execution-base
./build.sh
```

Build bindfit-datapackage container:
```
# Navigate back to bindfit-datapackage repository
cd containers
./build.sh
```

### Install CLI

```
python -m venv .venv
source .venv/bin/activate
pip install -e /PATH/TO/CLI

ods  # Check CLI is installed
```

See [Usage](#usage) for command reference.
