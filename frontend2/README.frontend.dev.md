## Desarrollo Local Frontend PymeRisk

### Instalación

```
# usando npm
npm install

# o usando pnpm (recomendado)
pnpm install
```

### Ejecutar
```
pnpm dev
```

Abrir: http://localhost:3000

### Estructura
- src/app: Rutas (Next.js App Router)
- src/components: Componentes reutilizables

### Objetivo Actual
Solo un campo para ingresar una red social (url o @handle) con detección básica de plataforma.

### Validación Futuro
- Llamar a endpoint reputación
- Normalizar dominios
- Chequear existencia vía API pública
