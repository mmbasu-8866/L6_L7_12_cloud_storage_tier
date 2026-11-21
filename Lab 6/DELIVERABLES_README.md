# Lab 6: Code and Branch Coverage

This folder contains terminal-output captures comparing the starter test suite
with the completed test suite:

| Coverage | Before | After |
|---|---|---|
| Line coverage | [Code coverage before](./code-coverage-before.png) | [Code coverage after](./code-coverage-after.png) |
| Branch coverage | [Branch coverage before](./branch-coverage-before.png) | [Branch coverage after](./branch-coverage-after.png) |

The before captures use the original starter test. The after captures use the
completed tests and show the measured coverage report.

Application repository: https://github.com/mmbasu-8866/L6_L7_12_cloud_storage_tier

Reproduce the after results from the application repository's `Lab 6` folder:

```bash
python -m coverage run -m pytest -q
python -m coverage report -m
python -m coverage erase
python -m coverage run --branch -m pytest -q
python -m coverage report -m
```
