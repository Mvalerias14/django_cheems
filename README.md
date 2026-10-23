# Sistema de órdenes de trabajo

Aplicación web hecha con Python, Django y MySQL. Permite crear órdenes de
trabajo, cambiar su estado (con historial automático), administrar usuarios
y consultar un log de acciones.

## Requisitos

- Python 3.12 o superior
- MySQL en ejecución local

## Instalación

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Crea y activa un entorno virtual:
```powershell
   python -m venv venv312
   venv312\Scripts\activate
```
3. Instala las dependencias:
```powershell
   pip install -r requirements.txt
```
4. Crea una base de datos vacía en MySQL y carga las tablas con `schema.sql`.
   Si tu base ya existe, solo agrega la columna nueva:
```sql
   ALTER TABLE work_order_history ADD COLUMN action VARCHAR(200) NULL;
```
5. Define las variables de entorno (cada integrante usa las de su máquina):
```powershell
   $env:DB_NAME = "nombre_de_tu_base"
   $env:DB_PASSWORD = "tu_contraseña_de_mysql"
```
   Opcionales: `DB_USER` (por defecto `root`), `DB_HOST` (`127.0.0.1`) y
   `DB_PORT` (`3306`). Con `setx` quedan guardadas de forma permanente
   (hay que reabrir la terminal).
6. Crea el primer usuario administrador:
```powershell
   python manage.py shell -c "from hello.models import User; from django.contrib.auth.hashers import make_password; User.objects.create(name='Administrador', account='admin', password=make_password('Admin123'), profile=1)"
```
7. Arranca el servidor:
```powershell
   python manage.py runserver
```
   y abre http://127.0.0.1:8000/ (usuario `admin`, contraseña `Admin123`;
   cámbiala después desde la sección Usuarios).

No es necesario ejecutar `migrate`: las tablas las define `schema.sql` y las
sesiones se guardan en una cookie firmada.

## Perfiles

| Perfil | Permisos |
|---|---|
| Administrador | Todo, incluida la administración de usuarios |
| Operador | Órdenes, historial y log |

## Estados de una orden

Pendiente → En proceso → Terminada. Una orden Pendiente o En proceso también
puede pasar a Cancelada. Las órdenes Terminadas o Canceladas ya no cambian.
Cada cambio queda en el historial con fecha, usuario y acción.

## Valores numéricos en la base de datos

- `user.profile`: 1 = Administrador, 2 = Operador
- `work_order.status`: 1 = Pendiente, 2 = En proceso, 3 = Terminada, 4 = Cancelada
- `log.module`: 1 = Usuarios, 2 = Órdenes

## Estructura

- `hello/models.py`: modelos sobre las tablas existentes (`managed = False`)
- `hello/services.py`: lógica de negocio (crear orden, cambiar estado, usuarios)
- `hello/views.py`: vistas
- `hello/decorators.py`: protección de vistas por sesión y por perfil
- `hello/templates/hello/`: plantillas HTML