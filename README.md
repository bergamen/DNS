# Informe Proxy
- Integrantes : Benjamin Alvarez, Vicente Garrido 
- Profesora : Ivana Bachmann
- Seccion : 2


# Declaracion de IA
Durante el desarrollo de esta actividad no se hizo uso de IA. Este trabajo fue a base de mucha prueba y error. 

# Link Repo
El codigo puede ser encontrado en el siguiente github https://github.com/bergamen/DNS, puede ser clonado el repositorio atraves de `git clone https://github.com/bergamen/DNS`

Primeramente se necesita instalar la libreria dnslib para poder correr el codigo, el env que esta presente en los archivos era experimentativo. 

Para poder correr el `resolver.py` se necesita ejecutar `python3 resolver.py`
Para ejecutarlo en modo debug, se usa como parametro `g`
Para activar el cache, se usa el parametro `c`
Para usar ambos a la vez, se usa el parametro `gc` o `cg`
ejemplo de uso: `python3 resolver.py -gc`

# Explicacion del codigo
## Flujo
Primeramente, se debe usar un socket no orientado a coneccion, esto debido a la naturaleza de dicho socket, en el que se realizan una gran cantidad de redirecciones, no es conveniente tener una direccion especifica. junto con que es mas rapido, una prioridad en este tipo de consultas.  

Para el manejo de cache, debido al analisis de casos bordes como, por ejemplo, al eliminar la consulta mas antigua, puede ocurrir que se elimine uno de los 3 que se encuentran en el cache, lo que implicaria que salga del top3 y debamos poner el nuevo que entre y en caso de que no sea la ip que acaba de entrar, de modo que la siguiente vez se se realice una consulta a esa dirección, aunque este en el top 3, forzara la busqueda para rellenar la informacion faltante.

Para el desarrollo del resolver se siguio el flujo dado en la especificaciones, y con esto, como se nos indica, si nos llegan respuestas de otro tipo debemos ignorarlas, esto podria generar a que lo que enviamos como respuesta no tenga la respuesta en si, al llegarnos datos que no supimos manipular bien para resolver la consulta DNS, basicámente, no tenemos toda la información necesaria para resolver todo tipo de consultas.

Siguiendo el código, en main entra en un bucle donde espera que le llegue una question de DNS, l parsea a DNSRecord para panejar los datos, si esta en el modo cache, preguntara si esta en el cache su respuesta, si no, manda todo al resolver, donde obtiene la respuesta y se la reenvia a el solicitante original.


# Preguntas
## Pruebas de funcionalidad
#### El comando `dig -p8000 @IP_VM eol.uchile.cl` responde con una IP de la forma 146.83.63.X ¿Cuántas respuestas encuentra? Indíquelo en su informe
R: LA respuesta del resolver incluia 12 respuestas distintas

```bash
;; ANSWER SECTION:
eol.uchile.cl.          3600    IN      CNAME   oeol-c.uchile.cl.
oeol-c.uchile.cl.       3600    IN      A       146.83.63.65
oeol-c.uchile.cl.       3600    IN      A       146.83.63.77
oeol-c.uchile.cl.       3600    IN      A       146.83.63.69
oeol-c.uchile.cl.       3600    IN      A       146.83.63.73
oeol-c.uchile.cl.       3600    IN      A       146.83.63.40
oeol-c.uchile.cl.       3600    IN      A       146.83.63.31
oeol-c.uchile.cl.       3600    IN      A       146.83.63.68
oeol-c.uchile.cl.       3600    IN      A       146.83.63.64
oeol-c.uchile.cl.       3600    IN      A       146.83.63.72
oeol-c.uchile.cl.       3600    IN      A       146.83.63.71
oeol-c.uchile.cl.       3600    IN      A       146.83.63.74
```

#### Si al iniciar su resolver hace una consulta a eol.uchile.cl, la segunda consulta a `eol.uchile.cl con dig -p8000 @IP_VM` da la misma dirección IP (¿cuál?), pero respondió el caché.
R: Si, en especifico, da la direccion `146.83.63.74` que fue la que se guardo en caché

#### El comando `dig -p8000 @IP_VM www.uchile.cl` resuelve a 200.89.76.36
R:Si

#### El comando `dig -p8000 @IP_VM cc4303.bachmann.cl` resuelve a 104.248.65.245
R:Si

## Experimentos

#### Intente resolver el siguiente dominio con su programa www.webofscience.com ¿Resuelve su programa este dominio? ¿Qué sucede? ¿Por qué? ¿Cómo arreglaría usted este problema? Anote las respuestas a estas preguntas en su informe.

R: Nuestro programa no resuelve este dominio, porque entra en un bucles de consultas, como se observa en la consola

```bash
(debug) Consultando www.webofscience.com. a ns-342.awsdns-42.com. con dirección IP 205.251.193.86
(debug) Consultando ns-342.awsdns-42.com. a . con dirección IP 198.41.0.4
(debug) Consultando ns-342.awsdns-42.com. a l.gtld-servers.net. con dirección IP 192.41.162.30
(debug) Consultando ns-342.awsdns-42.com. a g-ns-43.awsdns-42.com. con dirección IP 205.251.192.43
(debug) Consultando www.webofscience.com. a ns-342.awsdns-42.com. con dirección IP 205.251.193.86
```
esto sucede porque no se encuentra y empieza a buscarse en un ciclo cerrado. Una solucion rapida sera colocar un limite de consultas, y si no se resuelve, pasar de ella. 


### Ejecute el comando `dig -p8000 @IP_VM www.cc4303.bachmann.cl` ¿Qué ocurre? ¿Qué habría esperado que ocurriera? Anote sus observaciones en su informe. Contraste sus observaciones con la respuesta de ejecutar `dig @1.1.1.1 www.cc4303.bachmann.cl` y utilice sus conocimientos sobre DNS para explicar por qué ocurre esto.

R: Solamente nos llega el AUTHORITY, y una respuesta del tipo SOA, esto puede ser porque estamos preguntando por una zona de dominio, no por una ip en particular, nos estan dando las credenciales, por eso no se recibe ningun answer. Lo esperado que mandara toda la informacion, como lo hacen el resto de dominios (junto con el ANSWER SECTION). Al compararlo con el codigo sugerido, obtenemos lo mismo. 

### Realice varias consultas a un mismo dominio y a través del modo debug vea a qué Name Servers y direcciones IP le pregunta su resolver en cada consulta. ¿Son siempre los mismos Name Servers? ¿Por qué cree usted que sucede esto? Anote las respuestas a estas preguntas en su informe.
R: Al momento de conectar nos dio lo mismo, esto puede ser debido se pregunta la misma ip a el mismo servidor, por lo que tenemos las mismas redirecciones. si es que se preguntara a otro servidor o ocurriera algun cambio interno como de host, puede que cambien los datos. 

