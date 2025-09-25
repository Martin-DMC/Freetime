#### 7 PRINCIPIOS DE LAS PRUEBAS DE SOFTWARE ####
# # # # # # # # # # # # # # # # # # # # # # # # #

# 1 No es podible realizar pruebas exhaustivas
* Nesecitamos una cantidad optima de pruebas 
  - (se refiere a no probar todo sino lo esencial)

# 2 Agrupacion de defectos
* Modulo reporte 20% defectos
- (se refiere a la ley de pareto, el 20% genera el 80%, si encontramos ese 20% de errores y los agrupamos de seguro solucionaremos el 80% faltate)

# 3 paradoja de los pesticidas
* Mejorar las pruebas
* Las pruebas que son repetitivas automatizarlas 
- (se refiere a generar siempre nuevas pruevas para testear, ya que si la app avanza y seguimos aplicando las mismas pruebas no vamos a detectar errores obviamente)

# 4 Las pruebas muestran la presencia de defectos
* las pruebas deben estar enfocadas a detectar defectos
- (la pruebas de software reducen la posibilidad de que existan defectos no descubiertos en el sofware, pero incluso aunque no se encuentren defectos no es una prueba de correccion)

# 5 La ausencia de error = falacia
* libre de errores al 99% pero no se puede usar
- (el enfoque de las pruebas no debe ser solamente poner nuestro sistema al 99% libre de defectos, sino que tambien deben ser enfocadas a que el software se pueda usar y cumpla aquello para lo cual se a diseñado)

# 6 Pruebas tempranas
* Nos ahorra tiempo y dinero
- (cuando el software esta en etapas iniciales es bueno realizarle muchas pruebas asi garantizamos que el software a medida que crece lo hace sin errores)

# 7 Las pruebas dependen del contexto
* No es lo mismo probar una app bancaria que una app de compras
- (el enfoque de las pruebas va a ser muy diferente segun el sistema que estamos probando)

# #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Terminos que debemos conocer
* SDLC Software Development Life cycle
* STLC Software Testing Life Cycle

#  SDLC:                                  STLC:
        planing -- analysis                    requirement analysis -- test planing
       /                  \                       /                          \
  mantenance             desing             test closure                test desing
     \                     /                      \                          /
testing & integracion -- implementacion       test ececution -- enviroment setup

muchas veces nos vamos a encontrar con la nesecidad de saber en que parte del desarrollo nos encontramos y debemos ser capaces de identificar todos estos ciclos (obviamente esto cambia dependiendo de los equipos con los que trabajamos)

# ¿Que es el modelo v?

analisis                             pruebas
    diseño                        pruebas
        implementacion         pruebas
            verificacion    pruebas
                mantenimiento


* RELATO DEL MODELO CASCADA:
---------------------------
cuando se construye un software atras tiene un proceso de desarrollo, 1er paso es el analisis (que software se va a contruir?) entonces se hace el analisis acerca de las caracteristicas que va a tener, 2do (como va a ser la maqueta? va a ser una aplicacion web? que colores?, etc), 3er cuando ya tenemos la maqueta y la estructura definida de como va a ser se pasa a la implementacion, 4to etapa de verificacion y es donde se ejecutan los test para verificar si todas las capas cumplen con todo, el analisis el diseño y la implementacion, si todo esta bien se pasa a la ultima etapa que es la del mantenimiento (el software ya va a estar disponible para los usuarios pero pueden aparecer nuevos errores)

# Problemas con el modelo cascada
* poco margen para realizar ajustes a lo largo del proyecto debido a un cambio en las exigencias
* el usuario final no se integra en el proceso de produccion hasta que no termina la programacion
* en ocaciones, los fallos solo se detectan una vez finalizado el proceso de desarrollo 

# solucion al modelo cascada
* Modelo V
(lo que nos dice este modelo es que nosotros en cada etapa debemos hacer pruebas, en cada instancia hay que hacer nuevas pruebas (por que no se trabaja sobre lo mismo) y tienen que estar relacionadas con la etapa que van haciendo.)

# conclusion
* la prueba no es una actividad independiente y tiene que adaptarse al modelo de desarrollo elegido para el proyecto
* en cualquier modelo, las pruebas deben realizarse en todos los niveles, es decir, desde los requisitos hasta el mantenimiento.
