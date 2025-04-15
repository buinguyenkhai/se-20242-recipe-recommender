uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Wait until server is healthy
until wget -qO- http://server:8000/health >/dev/null; do
  sleep 1
done

# Import data
wget --post-data='' http://server:8000/import_recipes/ -O-

wait