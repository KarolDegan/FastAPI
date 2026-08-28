import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzg4MTIyNjM2fQ.PC0Mez5H2wUNXH1NxSY0bADssOZJxk52TTrnAAxoZLM"
}

requisicao = requests.get("http://localhost:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())