#!/bin/bash

TOKEN=`curl -s -H "Content-Type: application/json" -X POST http://localhost:9092/auth -d '{"username":"pav", "password":"123"}'  | jq -r '.token'`

curl -H "Authorization:$TOKEN" http://localhost:9092
echo ""
curl -H "Authorization:$TOKEN" http://localhost:9092/admin
echo ""
