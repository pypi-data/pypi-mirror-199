# Instrucciones

Este juego de pruebas puede usarse en el modo simulación de AAPP2FACe.
Consiste en una colección de respuestas de datos equivalentes a las que
retornaría el servicio web de FACe. Pueden ser usadas directamente o
como base para crear otras respuestas.

Más abajo se detallan los archivos que contiene este juego de pruebas y
los comandos de ejemplo que pueden invocarse con ellas. Obsérvese que en
los ejemplo se usa la opción general `-f`, por lo que es necesario
configurar la ubicación del juego de pruebas en el archivo de
configuración. Otra alternativa es usar `--fake-set DIRECTORIO` en cada
invocación, para indicar la ubicación donde se ha copiado el juego de
pruebas.

Resumen de los comandos que pueden invocarse con este juego de pruebas
son:

```shell
$ aapp2face -f unidades
$ aapp2face -f estados
$ aapp2face -f facturas nuevas
$ aapp2face -f facturas descargar 1111
$ aapp2face -f facturas confirmar P00000010 202001020718 RCF1234
$ aapp2face -f facturas consultar 202001020718 9999
$ aapp2face -f facturas estado P00000010 1300 "Comentario" 202001020718 202001017112 9999
$ aapp2face -f facturas crcf 202001020718 1200
$ aapp2face -f facturas rcf 202001017112
$ aapp2face -f facturas rcf 202001020718
$ aapp2face -f anulaciones nuevas
$ aapp2face -f anulaciones nuevas P99999999
```


### Archivo `consultarUnidades.json`

Respuesta a consulta de las relaciones vinculadas al RCF.

```shell
$ aapp2face -f unidades
```


### Archivo `consultarEstados.json`

Respuesta a consulta de los códigos y descripción de los estados que
maneja FACe.

```shell
$ aapp2face -f estados
```


### Archivo `solicitarNuevasFacturas.json`

Respuesta a petición de nuevas facturas registradas en la plataforma.

```shell
$ aapp2face -f facturas nuevas
```


### Archivo `descargarFactura.1111.json`

Respuesta a intento de descarga de una factura ya descargada
anteriormente que tiene por número de registro 1111.

```shell
$ aapp2face -f facturas descargar 1111
```


### Archivo `confirmarDescargaFactura.P00000010.202001020718.json`

Respuesta a confirmación de la descarga de una factúra correspondiente a
la oficina contable P00000010 y número de registro 202001020718.

```shell
$ aapp2face -f facturas confirmar P00000010 202001020718 RCF1234
```


### Archivo `consultarListadoFacturas.202001020718.9999.json`

Respuesta a consulta del estado de varias facturas con números de
registro 202001020718 y 9999, siendo este último correspondiente a una
factura no existente.

```shell
$ aapp2face -f facturas consultar 202001020718 9999
```


### Archivo `cambiarEstadoListadoFacturas.P00000010.202001020718.202001017112.9999.json`

Respuesta a la solicitud de cambio de estado de las facturas de la
oficina contable P00000010 con números de registro 202001020718,
202001017112 y 9999. En el ejemplo se usa como nuevo código de estado
1300 pero puede usarse cualquier otro.

```shell
$ aapp2face -f facturas estado P00000010 1300 "Comentario" 202001020718 202001017112 9999
```


### Archivo `cambiarCodigoRCF.202001020718.json`

Respuesta a solicitud de cambio del código RCF asignado a la factura con
código de registro 202001020718. En el ejemplo se usa como nuevo código
RCF 1200 pero puede usarse cualquier otro.

```shell
$ aapp2face -f facturas crcf 202001020718 1200
```


### Archivo `consultarCodigoRCF.202001017112.json`

Respuesta a consulta del código RCF registrado en FACe para una factura
que con número de registro 202001017112 no tiene asignado código.

```shell
$ aapp2face -f facturas rcf 202001017112
```


### Archivo `consultarCodigoRCF.202001020718.json`

Respuesta a consulta del código RCF registrado en FACe para la factura
con número de registro 202001020718.

```shell
$ aapp2face -f facturas rcf 202001020718
```


### Archivo `solicitarNuevasAnulaciones.json`

Respuesta a petición de nuevas solicitudes de anulación de facturas
registradas en la plataforma.

```shell
$ aapp2face -f anulaciones nuevas
```


### Archivo `solicitarNuevasAnulaciones.P99999999.json`

Respuesta a petición de nuevas solicitudes de anulación de facturas
registradas en la plataforma indicando una oficina contable no
existente.

```shell
$ aapp2face -f anulaciones nuevas P99999999
```
