# Proyecto MIA203

[![Main](https://github.com/hernangm/mia203/actions/workflows/CICD.yaml/badge.svg?branch=main)](https://github.com/hernangm/mia203/actions/workflows/CICD.yaml)

[![Production](https://github.com/hernangm/mia203/actions/workflows/CICD.yaml/badge.svg?branch=production)](https://github.com/hernangm/mia203/actions/workflows/CICD.yaml)

La API está disponible en: [https://mia203.onrender.com](https://mia203-api.onrender.com)

La documentacion esta disponible en: [https://mia203.onrender.com/docs](https://mia203.onrender.com/docs)

## Integrantes

- María Luisa Boettner
- Hernán Marano

## Instrucciones para correr el desarrollo y los tests

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

3. **Instalar dependencias**

```bash
python -m pip install --upgrade pip
pip install -r src/requirements.txt
```

## Cómo ejecutar la aplicación

```bash
uvicorn main:app --reload
```

## Cómo correr los tests

```bash
pytest src/tests
```