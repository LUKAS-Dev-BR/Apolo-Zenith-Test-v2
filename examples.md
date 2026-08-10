# Exemplos de Uso - Apolo Zenith 1.9

## Chat Básico

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat/send",
    json={
        "message": "Olá, como você está?",
        "reasoning_mode": "normal"
    }
)

print(response.json())
```

## Geração de Imagem

```python
import requests

response = requests.post(
    "http://localhost:8000/api/media/generate",
    json={
        "media_type": "image",
        "prompt": "Um pôr do sol em Marte",
        "parameters": {
            "width": 512,
            "height": 512
        }
    }
)

job_id = response.json()["job_id"]
print(f"Job ID: {job_id}")
```

## Verificação de Progresso

```python
import requests

response = requests.get(
    f"http://localhost:8000/api/media/progress/{job_id}"
)

print(f"Progresso: {response.json()['progress']}%")
```

## Codificação Agentica

```python
import requests

# Ler arquivo
response = requests.post(
    "http://localhost:8000/api/agents/code/execute",
    json={
        "command": "read_file",
        "params": {"path": "example.py"}
    }
)

print(response.json()["result"])

# Escrever arquivo
response = requests.post(
    "http://localhost:8000/api/agents/code/execute",
    json={
        "command": "write_file",
        "params": {
            "path": "output.py",
            "content": "print('Olá Mundo!')"
        }
    }
)

print(response.json()["result"])
```

## Modelagem 3D

```python
import requests

# Criar cubo
response = requests.post(
    "http://localhost:8000/api/agents/modeling/execute",
    json={
        "command": "create_mesh",
        "params": {
            "name": "MeuCubo",
            "primitive_type": "cube",
            "position": {"x": 0, "y": 0, "z": 0}
        }
    }
)

print(response.json()["result"])

# Exportar cena
response = requests.get(
    "http://localhost:8000/api/agents/modeling/scene"
)

print(response.json()["scene"])
```

## Uso do Frontend

1. Acesse http://localhost:3000
2. Digite sua mensagem na caixa de texto
3. Clique em "Enviar" ou pressione Enter
4. Aguarde a resposta do Apolo Zenith

## Configuração de Modo de Raciocínio

```python
import requests

# Usar modo de raciocínio avançado
response = requests.post(
    "http://localhost:8000/api/chat/send",
    json={
        "message": "Explique como funciona um transformer",
        "reasoning_mode": "ultra_mega_high"
    }
)

print(response.json()["response"])
```

## Criação de API Key

```python
import requests

response = requests.post(
    "http://localhost:8000/api/auth/keys",
    json={
        "name": "Minha Chave"
    }
)

api_key = response.json()["key"]
print(f"API Key: {api_key}")
```
