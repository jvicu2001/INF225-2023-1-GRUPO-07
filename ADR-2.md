# Titulo
integrar Svelte para el frontend

## Contexto
Se comienza utilizando un frontend puro lo que nos dificulta la union del frontend y el backend 

## Decision
Se decide utilizar Svelte un framework reactivo y basado en componentes que utiliza un paso de compilación al momento de realizar cambios en el DOM (Document Object Model) 

## Status
Implementado

## Consecuencias
### Positivas
-  Genera código de JavaScript ligero y optimizado a partir de nuestro código fuente
- Hacer más liviano el trabajo del navegador del lado cliente y reducir lo más posible la carga de código de librerías o frameworks por código JavaScript puro
- Mejor rendimiento y fácil desarrollo

### Negativas
- Debido a que es más nueva que el resto, hay poco material el línea para user de referencia y resolver problemas
- Por errores poco documentados, se hizo imposible el poder implementar el listado de archivos en la plataforma. Esto llevó a fallar las historias 2, 5 y 6