
# DESCRIPCIÓN

El módulo que nos asignaron es el de **Headhunters** y consiste en la parte de la plataforma de **Ducky Ways** que se encarga de gestionar a los cazatalentos de las empresas, facilitándole la búsqueda de candidatos, así como la creación de ofertas mediante herramientas de IA.

---

# FUNCIONALIDADES

## 1. Acceso y Búsqueda de Perfiles:
- Autenticación y permisos específicos para usuarios tipo head hunter.
- Funcionalidad de búsqueda avanzada de perfiles de CV filtrando por características como:
  - Habilidades
  - Experiencia
  - Nivel de idiomas

## 2. Publicación de Ofertas de Trabajo:
- Capacidad para que los head hunters publiquen y gestionen ofertas de trabajo.
- Enlace de las ofertas de trabajo con perfiles de CV y notificación a los usuarios relevantes.

## 3. Gestión de Seguimiento y Agenda:
- Sistema de agenda para gestionar y documentar acciones realizadas y pendientes con los postulantes.
- Posibilidad de añadir notas y programar recordatorios sobre cada oferta y candidato.

## 3. Implementacion de Inteligencias Artificiales:
- Chatbot
- sistema de recomendación de candidatos
- sistema de recomendación de ofertas de trabajo
---

# LIBRERÍAS NECESARIAS

```
absl-py==2.1.0
asgiref==3.8.1
astunparse==1.6.3
bleach==6.2.0
Brotli==1.1.0
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.4.0
colorama==0.4.6
cryptography==44.0.0
cssselect2==0.7.0
defusedxml==0.8.0rc2
Django==5.1.3
django-debug-toolbar==4.4.6
django-summernote==0.8.20.0
Faker==33.1.0
filelock==3.16.1
flatbuffers==24.3.25
fonttools==4.55.0
fsspec==2024.10.0
gast==0.6.0
google-pasta==0.2.0
grpcio==1.68.1
h5py==3.12.1
huggingface-hub==0.26.5
idna==3.10
Jinja2==3.1.4
joblib==1.4.2
keras==3.7.0
libclang==18.1.1
Markdown==3.7
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
ml-dtypes==0.4.1
mpmath==1.3.0
namex==0.0.8
networkx==3.4.2
numpy==2.0.2
oauthlib==3.2.2
opt_einsum==3.4.0
optree==0.13.1
packaging==24.2
pillow==10.4.0
protobuf==5.29.0
pycparser==2.22
pydyf==0.11.0
Pygments==2.18.0
PyJWT==2.10.1
pyphen==0.15.0
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python3-openid==3.2.0
PyYAML==6.0.2
regex==2024.11.6
requests==2.32.3
requests-oauthlib==2.0.0
rich==13.9.4
safetensors==0.4.5
scikit-learn==1.5.2
scipy==1.14.1
setuptools==75.1.0
six==1.16.0
social-auth-app-django==5.4.2
social-auth-core==4.5.4
sqlparse==0.5.2
sympy==1.13.1
tensorboard==2.18.0
tensorboard-data-server==0.7.2
tensorflow==2.18.0
tensorflow_intel==2.18.0
termcolor==2.5.0
threadpoolctl==3.5.0
tinycss2==1.4.0
tinyhtml5==2.0.0
tokenizers==0.21.0
torch==2.5.1
tqdm==4.67.1
transformers==4.47.0
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
weasyprint==63.0
webencodings==0.5.1
Werkzeug==3.1.3
wheel==0.44.0
wrapt==1.17.0
zopfli==0.2.3.post1
```

---

# INTERACCIÓN CON LOS DEMÁS COMPONENTES DEL PROYECTO

Nuestro módulo interactúa continuamente con el grupo **CV PROFILE USER** debido al hecho de que los head hunters buscan candidatos, y estos candidatos son gestionados por dicho grupo, incluyendo los currículums y sus características.  
También se conecta con el grupo de **TESTS** para relacionar una oferta con esos test.
