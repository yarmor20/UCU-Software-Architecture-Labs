# Clear file contents.
> ./logging-service.env

# Initialize service address.
echo "HOST=127.0.0.1" > ./logging-service.env
echo "PORT=${1}" >> ./logging-service.env

# Run service.
uvicorn logging_server:app --workers 1 --reload --port ${1}