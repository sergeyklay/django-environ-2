# This file is part of the django-environ-2.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

# Run “make build” by default
.DEFAULT_GOAL = build

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PKG_NAME = django-environ-2

ifneq (,$(findstring xterm,${TERM}))
	GREEN := $(shell tput -Txterm setaf 2)
	RESET := $(shell tput -Txterm sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"
else
	CS = "~~~ "
	CE = " ~~~"
endif

COV          =
REQUIREMENTS = requirements/requirements-dev.txt

PYTEST_FLAGS ?= --color=yes -v
PYLINT_FLAGS ?=
FLAKE8_FLAGS ?= --show-source --statistics

VENV_ROOT = .venv

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON  ?= python.exe
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	PYTHON  ?= python3
	VENV_BIN = $(VENV_ROOT)/bin
endif

VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP    = $(VENV_PYTHON) -m pip

export PATH := $(VENV_BIN):$(PATH)

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
ifneq ($(OS),Windows_NT)
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(error "Python is not available. Please install Python.")
endif
endif
endif
