# Facebook Marketplace Scraper

Este proyecto contiene un script de Python que permite extraer información de publicaciones del Facebook Marketplace utilizando Playwright para automatización web.

## ⚠️ Disclaimer

**Este script es solo con fines educativos. El autor no se hace responsable del uso que se le dé.**

## 📋 Funcionalidades

- Extracción automatizada de listings del Facebook Marketplace
- Autenticación persistente de Facebook (guarda estado de sesión)
- Navegación automática por los listings
- Filtrado automático de publicaciones patrocinadas
- Extracción de datos clave:
  - Título del producto
  - Precio
  - Ubicación
  - Descripción completa
- Exportación de datos a archivo Excel
- Manejo de errores y reintentos automáticos

## 🛠️ Requisitos del Sistema

- Python 3.7 o superior
- Windows (compatible con PowerShell)
- Conexión a internet
- Navegador Chromium (se instala automáticamente con Playwright)

## 📦 Instalación

1. **Clonar o descargar el proyecto:**

   ```bash
   git clone <url-del-repo>
   cd MarketplaceScraper
   ```

2. **Crear un entorno virtual (recomendado):**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar las dependencias:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Instalar los navegadores de Playwright:**
   ```powershell
   playwright install chromium
   ```

## 🚀 Uso

### Configuración inicial

1. **Ejecutar el script por primera vez:**

   ```powershell
   python scraper.py
   ```

2. **Autenticación manual:**
   - El script abrirá automáticamente Facebook en el navegador
   - Inicia sesión manualmente con tus credenciales
   - El script guardará tu sesión para usos futuros

### Configuración de búsqueda

Por defecto, el script está configurado para buscar "Toyota Echo 2003" en San José, Costa Rica. Para cambiar la búsqueda:

1. Modifica la variable `marketplaceurl` en el archivo `scraper.py`
2. Reemplaza la URL con tu búsqueda personalizada de Facebook Marketplace

**Ejemplo de URL personalizada:**

```python
marketplaceurl = "https://www.facebook.com/marketplace/tu-ciudad/search/?query=tu-busqueda"
```

### Ejecución

```powershell
python scraper.py
```

El script:

1. Utilizará tu sesión guardada de Facebook
2. Navegará a la página de búsqueda configurada
3. Extraerá automáticamente los datos de los listings
4. Generará un archivo Excel con timestamp: `marketplace_dataYYYYMMDD_HHMMSS.xlsx`

## 📁 Estructura del Proyecto

```
MarketplaceScraper/
│
├── scraper.py              # Script principal
├── requirements.txt        # Dependencias de Python
├── fb_login.json          # Estado de sesión de Facebook (generado automáticamente)
├── marketplace_data*.xlsx  # Archivos de datos extraídos
├── .venv/                 # Entorno virtual (si se usa)
└── README.md              # Este archivo
```

## 🔧 Configuración Avanzada

### Parámetros modificables en `scraper.py`:

- **Tiempo de espera entre scrolls:** Modifica `scrollpause` en la función `listall()`
- **Número máximo de scrolls:** Modifica `maxscrolls` en la función `listall()`
- **Timeouts:** Ajusta los valores de `timeout` en las llamadas a `wait_for_selector()`

### Ejemplo de personalización:

```python
def listall(page, scrollpause=3, maxscrolls=5):  # Más tiempo y más scrolls
    # ...resto del código
```

## 📊 Datos Extraídos

El script extrae los siguientes campos para cada listing:

| Campo       | Descripción                      |
| ----------- | -------------------------------- |
| title       | Título del producto/servicio     |
| price       | Precio en la moneda local        |
| location    | Ubicación geográfica             |
| description | Descripción completa del listing |

## ⚡ Características Técnicas

- **Navegador headless:** Configurable (por defecto `headless=False` para debugging)
- **Manejo de modales:** Automático para abrir y cerrar detalles de listings
- **Filtrado inteligente:** Omite automáticamente publicaciones patrocinadas
- **Reintentos:** Sistema de reintentos para listings que fallan al cargar
- **Persistencia de sesión:** Evita tener que loguearse en cada ejecución

## 🐛 Solución de Problemas

### Error: "Login timeout expired"

- **Causa:** No se completó el login manual en 2 minutos
- **Solución:** Ejecutar nuevamente y completar el login más rápido

### Error: "Modal did not open"

- **Causa:** Listing no se pudo abrir correctamente
- **Solución:** El script continúa automáticamente con el siguiente listing

### Error: "Error extracting data"

- **Causa:** Cambios en la estructura HTML de Facebook
- **Solución:** Revisar y actualizar los selectores CSS en el código

### Archivo fb_login.json corrupto

- **Solución:** Eliminar el archivo `fb_login.json` y volver a autenticarse

## 📝 Limitaciones

- Depende de la estructura HTML de Facebook (puede cambiar)
- Limitado por las políticas de rate limiting de Facebook
- Requiere autenticación manual inicial
- Solo funciona con búsquedas públicas de Marketplace

## 🔄 Actualizaciones

Para mantener el scraper funcionando:

1. Actualizar regularmente las dependencias:

   ```powershell
   pip install --upgrade -r requirements.txt
   ```

2. Revisar los selectores CSS si Facebook cambia su estructura

## 📄 Licencia

Este proyecto es solo para fines educativos. Úsalo de manera responsable y respetando los términos de servicio de Facebook.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

---

**Nota:** Este script está diseñado para uso educativo y de investigación. Asegúrate de cumplir con los términos de servicio de Facebook y las leyes locales sobre web scraping.
