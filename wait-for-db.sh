#!/bin/sh

# Wait for MySQL
while ! nc -z db 3306; do
  echo "Waiting for MySQL..."
  sleep 1
done

echo "MySQL is up - executing command"
exec "$@"
