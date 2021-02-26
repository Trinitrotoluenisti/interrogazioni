if [ ! -d env ]; then
    echo "Env non trovato, lo creo."
    python3 -m venv env
    source env/bin/activate
    echo "Installo i requisiti."
    pip3 install -r requirements.txt
else
    source env/bin/activate
fi

echo "Avvio server api."
echo
python3 run.py
echo
echo "Programma terminato."

deactivate