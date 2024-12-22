# Test Management Module

Este repositorio contiene el módulo **Test Management**, que forma parte de un proyecto más amplio destinado a gestionar pruebas psicotécnicas, evaluaciones de conocimiento y validaciones de habilidades blandas y técnicas.

## Descripción del Módulo
Aplicación para la realización de examenes con chatbot, con feedback final y consejos de mejora.
### Funciones y Características Principales
- **Gestión de Pruebas:**
  - Realización de exámenes.
  - Evaluaciones predefinidas para diferentes áreas (soft skills, Python, Django, etc.).
- **Chatbot Inteligente:**
  - Responde preguntas relacionadas con las pruebas.
  - Utiliza modelos de IA entrenados con TensorFlow.
- **Resultados y Comparaciones:**
  - Historial de evaluaciones con gráficos comparativos.
  - Perfil de usuario con competencias destacadas.

### Interacción con Otros Componentes
- **Integración del Chatbot:** Permite a los usuarios realizar consultas sobre las pruebas directamente desde sus paneles.
- **Conexión al Backoffice:** Los administradores pueden gestionar pruebas y analizar resultados globales.
- **Interoperabilidad:** Este módulo interactúa con los módulos de gestión de usuarios, recursos y perfiles para personalizar las evaluaciones.

## Instalación y Ejecución

### Requisitos
- Python 3.8 o superior.
- Django 4.0 o superior.
- TensorFlow 2.0 o superior.

### Instalación
1. Clona el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd test_management
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Realiza las migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

### Ejecución del Chatbot
1. Los modelos preentrenados se encuentran en la carpeta `chatbot`.
2. Para interactuar con el chatbot:
   - Accede a la ruta `/chatbot/` en tu navegador una vez que el servidor esté corriendo.

## Dependencias
- **Django:** Framework web para la gestión del servidor y vistas.
- **TensorFlow:** Para la gestión e inferencia del chatbot.
- **Pickle:** Serialización de modelos y datos.

## Estructura del Repositorio
```
├── test_management/
│   ├── admin.py
│   ├── apps.py
│   ├── chatbot/
│   ├── migrations/
│   ├── models.py
│   ├── static/
│   ├── templates/
│   ├── urls.py
│   ├── views.py
├── requirements.txt
└── README.md
```

## Contacto
Si tienes alguna pregunta o necesitas soporte, no dudes en contactar con el equipo de desarrollo a través del repositorio o correo electrónico.
