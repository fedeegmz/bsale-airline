# Bsale Airline
**url**: https://deta.space/discovery/r/fequtwywazgg2c61  
La API tiene dos endpoint:  
- root:
    - path: "/"  
    - response: JSON
        ```json
        {
            "testData": "Hello World"
        }
        ```
- check_in:  
    - path: "/flights/<flight_id>/passengers"  
    - path param: flight_id (int que corresponde al id de vuelo)  
    - response: JSON  
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
    - errors:
        - error al conectar con la DB: status_code=400
        - error al no encontrar un flight_id: status_code=404
        - si un pasajero menor de 18 años no tiene adultos responsables: status_code=409
        - si no se encuentra un asiento: status_code=409
## Ejecutar en local
Una vez clonado el repositorio, es necesario instalar los requerimientos. Antes de eso hay que **descomentar** las líneas en el archivo requirements.txt.  
Para instalar las dependencias ejecutar <pip install requirements.txt>  
### Servidor
Comando para iniciar el servidor <uvicorn main:app --reload>  