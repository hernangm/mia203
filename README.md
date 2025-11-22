# Proyecto MIA203

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hernangm/mia203/CICD.yaml?branch=main&label=Main)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hernangm/mia203/CICD.yaml?branch=production&label=Production)
![Coverage](https://hernangm.github.io/mia203/coverage.svg)

La API está disponible en [https://mia203.onrender.com](https://mia203.onrender.com)

La documentación está disponible en [https://mia203.onrender.com/docs](https://mia203.onrender.com/docs)

## Integrantes

- María Luisa Boettner
- Hernán Marano

## Decisiones de Diseño

### Uso del Patrón Strategy para Validación

Se eligió implementar el patrón Strategy para la validación de métodos de pago por las siguientes razones:

- **Extensibilidad:** Permite agregar fácilmente nuevos métodos de pago y sus validaciones específicas sin modificar el código existente. Cada método de pago tiene su propia estrategia de validación encapsulada en una clase independiente.
- **Separación de responsabilidades:** La lógica de validación de cada método de pago está aislada, lo que facilita el mantenimiento y la comprensión del código.
- **Testabilidad:** Al tener cada estrategia en una clase separada, es sencillo escribir tests unitarios específicos para cada tipo de validación, asegurando que los cambios en una estrategia no afecten a las demás.
- **Trade-offs:** Se consideró usar condicionales simples (if/elif) para la validación, pero esto haría el código menos escalable y más difícil de mantener a medida que se agregan nuevos métodos de pago. El patrón Strategy implica mayor cantidad de clases, pero mejora la organización y la flexibilidad.
- **Desacoplamiento:** El controlador principal no necesita conocer los detalles de cada validación, solo delega la responsabilidad a la estrategia correspondiente.

En resumen, el patrón Strategy fue elegido para favorecer la modularidad, la escalabilidad y la claridad en la lógica de validación de pagos, alineándose con buenas prácticas de diseño orientado a objetos.

### Flujo de Validación

```mermaid
sequenceDiagram
    participant Usuario
    participant API
    participant EstrategiaValidacion
    Usuario->>API: Solicita pago con método X
    API->>EstrategiaValidacion: Valida datos
    EstrategiaValidacion-->>API: Resultado validación
    API-->>Usuario: Respuesta (éxito/error)
```

## Integración y Despliegue Continuos (CI/CD)

El proyecto utiliza GitHub Actions para automatizar los procesos de integración y despliegue continuo. El archivo de configuración `.github/workflows/CICD.yaml` define dos flujos principales:

### 1. Flujo de Integración Continua (CI)

- **Disparadores:** Se ejecuta automáticamente en cada push o pull request a las ramas `main` y `production`.
- **Pasos principales:**
  - **Checkout:** Descarga el código fuente del repositorio.
  - **Cache de dependencias:** Optimiza la instalación de paquetes usando caché de pip.
  - **Setup de Python:** Configura el entorno con Python 3.11.
  - **Instalación de dependencias:** Instala los paquetes necesarios y los opcionales para testing.
  - **Ejecución de tests:** Corre los tests con cobertura usando `pytest` y genera un badge de cobertura.
  - **Actualización de badge:** El badge de cobertura se actualiza automáticamente en la rama `gh-pages` para visualizar el estado en el README.
  - **Linting:** Ejecuta `flake8` para asegurar calidad y estilo del código.

### 2. Flujo de Despliegue Continuo (CD)

- **Desencadenante:** Se ejecuta automáticamente en cada push a la rama `production`.
- **Despliegue:** Utiliza la acción `render-deploy` para desplegar la aplicación en Render, usando credenciales seguras almacenadas en GitHub Secrets.
- **Badge de despliegue:** El estado del despliegue se refleja en el README mediante badges automáticos.

### Beneficios

- **Automatización:** Reduce errores manuales y asegura que el código siempre pase por pruebas antes de desplegarse.
- **Transparencia:** Los badges permiten visualizar rápidamente el estado de los tests, cobertura y despliegue.
- **Calidad:** El linting y la cobertura ayudan a mantener un estándar alto en el código fuente.


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
pip install .
```

## Ejecuta la aplicación

```bash
uvicorn main:app --reload
```

## Corre los tests

```bash
pip install .[test]
```

```bash
python -m pytest src/tests
```