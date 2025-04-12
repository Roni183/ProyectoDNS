
🛡️ Auditoría DNS con Shodan
===========================

Una herramienta gráfica desarrollada en Python para realizar auditorías de servidores DNS expuestos públicamente. 
Utiliza la API de Shodan para detectar IPs con el puerto 53 abierto y permite probar la resolución de dominios, 
identificar servidores recursivos y visualizar los resultados en una interfaz intuitiva.

📋 Características
------------------
- Búsqueda de servidores DNS expuestos (puerto 53 abierto) con Shodan.
- Verificación de resolución DNS por UDP y TCP.
- Detección de servidores con recursividad habilitada.
- Admite múltiples dominios separados por comas.
- Interfaz gráfica con soporte de paginación.
- Verificación directa de IPs específicas.
- Visualización detallada de resultados con doble clic.
- Exportación posible al copiar desde la tabla.
- Mensaje legal de advertencia al iniciar.

🛠️ Requisitos
-------------
- Python 3.7+
- API Key de Shodan (https://account.shodan.io/)
- Módulos de Python:

  pip install shodan dnspython

📦 Instalación
--------------
1. Clona o descarga el repositorio.
2. Asegúrate de tener los módulos instalados.
3. Renombra el archivo `CodigoDNS.txt` a `auditor_dns.py`.
4. Ejecuta con:

   python auditor_dns.py

🧪 Uso
------
1. Introduce dominios (ej: google.com,facebook.com) en el campo correspondiente.
2. Haz clic en "Buscar DNS Expuestos" para iniciar la auditoría con Shodan.
3. Usa los botones "Siguiente" y "Anterior" para navegar los resultados.
4. También puedes introducir una IP específica para comprobar su comportamiento con los dominios ingresados.
5. Haz doble clic sobre una fila para ver el resultado de resolución directa.

📜 Estructura de salida
-----------------------
Cada resultado contiene:

| Campo         | Descripción                                |
|---------------|--------------------------------------------|
| IP            | Dirección IP del servidor DNS              |
| Organización  | Dueño o proveedor (según Shodan)           |
| País          | Ubicación geográfica                       |
| Dominio       | Dominio consultado                         |
| Método        | Protocolo usado en la resolución (UDP/TCP) |
| Respuesta     | Resultado de la resolución DNS             |
| ¿Recursivo?   | Indica si el servidor es recursivo         |

⚠️ Aviso Legal
--------------
Esta herramienta es solo para fines educativos y auditorías autorizadas. 
El uso indebido puede ser ilegal. El autor no se hace responsable de cualquier mal uso de esta herramienta.

🧑‍💻 Autor
---------
Desarrollada por un estudiante de ciberseguridad con fines académicos y de práctica en auditorías DNS.
