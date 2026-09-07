Informe Proxy
Integrantes :
Seccion : 
Profesor : 


# Declaracion de IA
Durante el desarrollo de esta actividad no se hizo uso de IA. Este trabajo fue a base de mucha prueba y error. 

# link Repo
Primeramente se necesita instalar la libreria dnslib para poder correr el codigo, el env que esta presente en los archivos era experimentativo. 

Para poder correr el `resolver.py` se necesita ejecutar `python3 resolver.py -g`

# Explicacion del codigo
## Flujo

(¿Qué tipo de socket debe usar? Anótelo en su informe)
R: No orientado a coneccion





# Preguntas
## Pruebas de funcionalidad
El comando dig -p8000 @IP_VM eol.uchile.cl responde con una IP de la forma 146.83.63.X ¿Cuántas respuestas encuentra? Indíquelo en su informe
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

Si al iniciar su resolver hace una consulta a eol.uchile.cl, la segunda consulta a eol.uchile.cl con dig -p8000 @IP_VM da la misma dirección IP (¿cuál?), pero respondió el caché.
R: Si

El comando dig -p8000 @IP_VM www.uchile.cl resuelve a 200.89.76.36
R:

El comando dig -p8000 @IP_VM cc4303.bachmann.cl resuelve a 104.248.65.245
R:

## Experimentos




Intente resolver el siguiente dominio con su programa www.webofscience.com ¿Resuelve su programa este dominio? ¿Qué sucede? ¿Por qué? ¿Cómo arreglaría usted este problema? Anote las respuestas a estas preguntas en su informe.
R:

Ejecute el comando dig -p8000 @IP_VM www.cc4303.bachmann.cl ¿Qué ocurre? ¿Qué habría esperado que ocurriera? Anote sus observaciones en su informe. Contraste sus observaciones con la respuesta de ejecutar dig @1.1.1.1 www.cc4303.bachmann.cl y utilice sus conocimientos sobre DNS para explicar por qué ocurre esto.
R:

Realice varias consultas a un mismo dominio y a través del modo debug vea a qué Name Servers y direcciones IP le pregunta su resolver en cada consulta. ¿Son siempre los mismos Name Servers? ¿Por qué cree usted que sucede esto? Anote las respuestas a estas preguntas en su informe.
R:



tkm benja uwu