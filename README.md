Interfaz Inteligente: Control a través de gestos y voz para Microsoft Office Word y Power Point 

---

El siguiente proyecto es la base de un Trabajo Final de Maestría, para la Maestría en Inteligencia Artificial de la UNIR México.
El principal objetivo de este trabajo es el desarrollo de un prototipo funcional que proporcione a usuarios la interacción con Word y Power Point a través de una Interfaz de Usuario Natural.

## Requisitos

1. Sistema Operativo: MacOS Ventura 13.0 o Windows 10/11
2. Python 3.9
3. PIP version 3
4. Permisos de acceso a micrófono, cámara y al sistema de archivos.


## Instalación

Para poder ejecutar adecuadamente el proyecto es necesario clonar el repositorio en su máquina local 

```
git clone https://github.com/smart-interface-13/smart-interface.git
cd smart-interface
```

Posteriormente se debe crear un entorno virtual e instalar los requerimientos de librerías de Python y ejecutar el flujo principal

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main_flow.py
```

## Notas especiales

Siempre que el programa se ejecuta el modo default es con comando de voz, es necesario cambiar mediante comando al modo de reconocimiento gestual si se requiere.

**Ocasionalmente, sobre todo al ser ejecutado por primera vez, el sistema operativo puede solicitar permisos de acceso al micrófono, cámara y al sistema de archivos. Todos los permisos son requeridos para el funcionamiento correcto del software.**