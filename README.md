# Bsale Airline API
La API simula el trabajo de una aerolínea, ubicando a los pasajeros en un avión. Se realizó con **Python** (framework: **FastAPI**). Solo cuenta con el endpoint **check_in**, además del endpoint root (que solo retorna un mensaje).  
Este endpoint recibe por "path parameter" el id de vuelo. Con ese id realiza diferentes consultas para acceder a los datos necesarios (información de los pasajeros y sus tarjetas de embarque, información de los aviones, información de vuelos, etc), que se encuentran en una base de datos MySQL. Se utilizó **SQL Alchemy** como ORM.  
Ya con los datos listos, ordena los pasajeros en los asientos vacíos que quedan. Se le da prioridad a los pasajeros menores de 18 años, debido a que deben sentarse al lado de un adulto que se responsabilice de ellos. Luego se van asignando asientos (en la misma fila o culumna en lo posible) para los demas pasajeros, dando prioridad a los grupos más grandes, es decir, los grupos más grandes de pasajeros que hicieron la compra del pasaje a la vez (comparten purchaseId).  
El endpoint check_in cuenta con varios tests escritos también en Python (**PyTest**) que verifican que:
- los datos del vuelo estén correctos
- la cantidad de pasajeros retornados sea la correcta
- no se repiten pasajeros
- los pasajeros menores de 18 años tienen a un adulto responsable al lado
- no se asignaron asientos de una clase diferente a ningún pasajero
- hay 60% o más de pasajeros que tienen a un acompañante cerca (que comparte purchaseId)  
## Endpoints:
- **root**:
    - **path**: "/"  
    - **response**: JSON
        ```json
        {
            "msg": "Welcome to Bsale Airline API"
        }
        ```
- **check_in**:  
    - **path**: "/flights/<flight_id>/passengers"
    - **path param**: flight_id (int que corresponde al id de vuelo)  
    - **response**: JSON  
        ```json
        {
            "code": 200,
            "data": {
                "flightId": 1,
                "takeoffDateTime": 1688207580,
                "takeoffAirport": "Aeropuerto Internacional Arturo Merino Benitez, Chile",
                "landingDateTime": 1688221980,
                "landingAirport": "Aeropuerto Internacional Jorge Cháve, Perú",
                "airplaneId": 1,
                "passengers": [
                    {
                        "passengerId": 90,
                        "dni": 983834822,
                        "name": "Marisol",
                        "age": 44,
                        "country": "México",
                        "boardingPassId": 24,
                        "purchaseId": 47,
                        "seatTypeId": 1,
                        "seatId": 1
                    },
                    {...}
                ]
            }
        }
        ```
    - **errors**:
        - **error al conectar con la DB**: status_code=400
        - **error al no encontrar un flight_id**: status_code=404
        <!-- - **si un pasajero menor de 18 años no tiene adultos responsables**: status_code=409
        - **si no se encuentra un asiento**: status_code=409 -->
## Docs
La documentación (**Swagger**) se encuentra en "/docs"
## Local
Una vez clonado el repositorio, es necesario instalar los requerimientos. Antes de eso hay que **descomentar** las líneas en el archivo requirements.txt.  
Para instalar las dependencias ejecutar ```pip install requirements.txt```  
También es necesario crear un archivo .env en la ruta "./", este debe contener las sigueintes variables de entorno, con sus respectivos valores para acceder a la DB:
    ```env
    MYSQL_HOST="localhost"
    MYSQL_PORT="3306"
    MYSQL_USER="username"
    MYSQL_PASSWORD="password"
    ```
## Server
Comando para iniciar el servidor ```uvicorn main:app --reload```  
## Testing
Comando para ejecutar los tests ```pytest```  
# Future
- Para los pasajeros que viajan de a dos (es decir, cuando solo hay dos pasajeros con el mismo purchaseId) sentarlos al lado.
- Si un pasajero viaja solo (es decir, no hay otro pasajero con el mismo purchaseId) que su asiento no tenga un asiento disponible al lado; para optimizar el espacio.