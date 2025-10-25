# Proyecto MIA203

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hernangm/mia203/CICD.yaml?branch=main&label=Main)

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hernangm/mia203/CICD.yaml?branch=production&label=Production)

[![cov](https://hernangm.github.io/mia203/badges/coverage.svg)](https://github.com/hernangm/mia203/actions)

La API está disponible en [https://mia203.onrender.com](https://mia203-api.onrender.com)

La documentación está disponible en [https://mia203.onrender.com/docs](https://mia203.onrender.com/docs)

## Integrantes

- María Luisa Boettner
- Hernán Marano

## Cómo instalar la aplicación

1. **Clona el repositorio**

```bash
git clone https://github.com/hernangm/mia203.git
cd mia203
```

2. **Crea y activa un entorno virtual** (Opcional pero recomendado)

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
En Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Instala dependencias**

```bash
python -m pip install --upgrade pip
pip install -r src/requirements.txt
```

## Ejecuta la aplicación

```bash
uvicorn main:app --reload
```

## Corre los tests

```bash
pytest src/tests
```