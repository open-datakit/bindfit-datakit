# Bindfit datakit

Bindfit is a binding constant fitting tool designed to work with classical supramolecular titration data obtained from NMR, UV, Fluorescence and other methods.

* 🗒️ [Datakit documentation](https://docs.opendatakit.io/)
* 💻 [Bindfit Python library GitHub](https://github.com/open-datakit/bindfit)

## Example usage
```
dk reset                                   # Clear any previous outputs
dk init                                    # Initialise the default run
dk load data ./data/nmr11.csv              # Load input data
dk set model "nmr1to1"                     # Set fit model
dk set method "nelder-mead"                # Set fit method
dk set inputParams.k.init 314              # Set initial parameter guess
dk run                                     # Run algorithm
dk show outputParams                       # View optimised parameters
dk show summary                            # View fit summary
dk view fitGraphMatplotlib                 # View fit graph
```

## Development

### Requirements

* Docker
* Python (to run CLI)
* [open-datakit/cli](https://github.com/open-datakit/cli)
* [open-datakit/containers](https://github.com/open-datakit/containers)

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
# Navigate to python-run-base repository
./build.sh
```

Build bindfit-datakit container:
```
# Navigate back to bindfit-datakit repository
cd containers
./build.sh
```

### Install CLI

```
python -m venv .venv
source .venv/bin/activate
pip install -e /PATH/TO/CLI

dk  # Check CLI is installed
```

See [Usage](#usage) for command reference.
