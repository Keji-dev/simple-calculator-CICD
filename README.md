# 🧮 Calculadora Simple CI/CD

Este proyecto es una calculadora web desarrollada en Python (Flask), con integración y despliegue continuo (CI/CD) mediante Jenkins. La aplicación está contenerizada con Docker y preparada para ser desplegada en un clúster Kubernetes sobre AWS. Incluye pruebas automatizadas, análisis de calidad y rendimiento.

---

## 🚀 Tecnologías Utilizadas

- Python 3
- Flask
- Jenkins
- Docker
- Kubernetes (AWS EKS)
- Terraform
- JMeter
- SonarQube
- OWASP ZAP
- Bandit
- Flake8
- Coverage.py
- WireMock

---

## ⚙️ Jenkins CI/CD Pipeline

### Flujo Automatizado:

1. **Obtener el código**
   - Se clona el repositorio desde GitHub y se guarda con `stash`.

2. **Pruebas en paralelo**
   - `Unit`: Ejecuta `pytest` para tests unitarios (`test/unit/`).
   - `REST`: 
     - Inicia servidores de prueba (Flask y WireMock).
     - Ejecuta `pytest` sobre la API REST (`test/rest/`).

3. **Cobertura de código**
   - Calculada con `coverage.py`.
   - Evaluada con `Cobertura` plugin.

4. **Controles de calidad**
   - `Bandit`: Análisis de seguridad.
   - `Flake8`: Análisis estático.
   - `JMeter`: Pruebas de rendimiento (`test/jmeter/flask.jmx`).
   - `SonarQube` y `OWASP ZAP` pueden integrarse para análisis de calidad adicional (si configurado en el entorno).

5. **Publicación de resultados**
   - Pruebas y cobertura se reportan en Jenkins.

6. **Limpieza de entorno**
   - Se detienen contenedores y se limpia el workspace automáticamente.

---
