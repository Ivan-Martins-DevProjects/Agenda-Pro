#!/bin/bash

set -e

echo "Iniciando a API em Python"
cd backend/python
python main.py

PYTHON_PID=$!


echo "Iniciando a API em Golang"
cd ./backend/golang/cmd
go run main.go &

GO_PID=$!

echo "APIs iniciadas com PID's: Python= $PYTHON_PID, Golang=$GO_PID"

wait $PYTHON_PID $GO_PID
