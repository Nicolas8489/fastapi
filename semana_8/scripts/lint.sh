#!/bin/bash
flake8 app/ tests/
bandit -r app/
mypy app/
