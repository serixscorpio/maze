<p align="center">
<a href="https://github.com/serixscorpio/maze/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/serixscorpio/maze/actions/workflows/test.yml/badge.svg" alt="Test">
</a>
<a href="https://smokeshow.helpmanual.io/1q2i3t2l6104642v1x38/" target="_blank">
    coverage report
</a>
</p>

# Development

Clone this repository.

Create a virtual environment, for example, directory `venv` using Python's `venv` module.
```
python -m venv venv
```

Activate the new environment with:
```
source ./venv/bin/activate
```

Make sure the latest pip version is in your virtual environment:
```
pip install --upgrade pip
```

Install all dependencies:
```
pip install -r requirements.txt
```

Test run cli tool to generate a cat shaped maze:
```
maze
```

# Usage (TBD)