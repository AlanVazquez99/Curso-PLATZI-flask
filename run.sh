#! /bin/bash

source activate backend

export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
export GOOGLE_CLOUD_PROJECT=curso-platzi-flask-279305

echo "Elija la opcion a ejecutar"
echo -ne "Test App[t] 		Correr App[r]: \t\t"
read option

if [ "$option" == "t" ]; then
	flask test
else 
	flask run
fi