# Clear file contents.
> ./facade-service.env

# Initialize service address.
echo "HOST=127.0.0.1" > ./facade-service.env
echo "PORT=${1}" >> ./facade-service.env

# Run service.
uvicorn facade_server:app --workers 1 --reload --port ${1}