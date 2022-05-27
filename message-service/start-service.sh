# Clear file contents.
> ./message-service.env

# Initialize service address.
echo "HOST=127.0.0.1" > ./message-service.env
echo "PORT=${1}" >> ./message-service.env

# Run service.
uvicorn message_server:app --workers 1 --reload --port ${1}