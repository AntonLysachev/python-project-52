po### Hexlet tests and linter status:
[![Actions Status](https://github.com/AntonLysachev/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AntonLysachev/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/fee8742d7525473c7c2e/maintainability)](https://codeclimate.com/github/AntonLysachev/python-project-52/maintainability)

Description: task manager
             Manage your tasks with the task manager
             https://task-manager-srxp.onrender.com

Commands: 
        Install - `make setup`,
        start guincorn - `make start`,
        start djando server - `make dev`,
        linter - `make lint`,
        start tests - `male test`

Environment variables: Required environment variables in the .env.sample file

Run:
to run on your local computer, create a ".env" file in the project root and add the necessary environment variables from .env.sample to it. To install the environment, use the `make setup` command. To start the Django server, use the `make dev` command.