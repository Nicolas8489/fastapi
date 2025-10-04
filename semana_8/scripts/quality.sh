#!/bin/bash
./scripts/format.sh
./scripts/lint.sh
pytest tests/ -v --cov=app --cov-report=html
