import app.application.fast_api as fast_api
import logging

# Configuración del registro
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configurar el logger raíz
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Añadir un StreamHandler para asegurar que los registros se muestren en la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

app = fast_api.create_app()