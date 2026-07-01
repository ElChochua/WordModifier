# Manual de Usuario — DockGen

> Genera documentos Word de forma masiva a partir de una plantilla y una tabla de datos.

---

## Índice

1. [¿Qué es DockGen?](#1-qu%C3%A9-es-dockgen)
2. [Requisitos previos](#2-requisitos-previos)
3. [Instalación y primer arranque](#3-instalaci%C3%B3n-y-primer-arranque)
4. [Conceptos que debes conocer](#4-conceptos-que-debes-conocer)
5. [Preparación de la plantilla de Word](#5-preparaci%C3%B3n-de-la-plantilla-de-word)
6. [Conociendo la interfaz](#6-conociendo-la-interfaz)
7. [Flujo de trabajo paso a paso](#7-flujo-de-trabajo-paso-a-paso)
8. [Tipos de archivo de datos admitidos](#8-tipos-de-archivo-de-datos-admitidos)
9. [Catálogo de errores y soluciones](#9-cat%C3%A1logo-de-errores-y-soluciones)
10. [Cómo funciona por dentro](#10-c%C3%B3mo-funciona-por-dentro)
11. [Preguntas frecuentes (FAQ)](#11-preguntas-frecuentes-faq)
12. [Glosario rápido](#12-glosario-r%C3%A1pido)
13. [Soporte y versión](#13-soporte-y-versi%C3%B3n)

---

## 1. ¿Qué es DockGen?

DockGen es una aplicación de escritorio que te permite **crear muchos documentos Word de una sola vez**, de forma automática. Para ello solo necesitas dos cosas:

- 📄 Una **plantilla** (un archivo `.docx` con huecos marcados para rellenar).
- 📊 Una **tabla de datos** (puede venir de Excel, CSV, otro Word o introducirse a mano).

La aplicación toma cada fila de la tabla y genera un documento Word nuevo, rellenando automáticamente los huecos de la plantilla con los valores de esa fila.

### ¿Para quién está pensado este manual?

Para **cualquier persona**, incluso si nunca ha usado programas similares. Las instrucciones siguientes están escritas paso a paso y evitando tecnicismos.

### ¿Qué casos de uso tiene?

- Cartas personalizadas para un listado de clientes.
- Certificados para una lista de alumnos.
- Contratos o constancias con datos individuales.
- Cualquier documento repetitivo donde solo cambian algunos datos (nombre, fecha, importe, etc.).

---

## 2. Requisitos previos

### Sistema operativo

- ✅ Windows 10 / 11
- ✅ macOS 11 o superior
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

### Si vas a convertir el resultado a PDF

DockGen puede producir PDFs combinados, para lo cual necesita **LibreOffice** instalado en el equipo. No es obligatorio para generar documentos Word.

| Sistema | Enlace / Comando |
|---|---|
| Windows | https://www.libreoffice.org/download/ |
| macOS | `brew install --cask libreoffice` |
| Linux | `sudo apt install libreoffice` |

### Permisos

- Permiso de lectura sobre la carpeta donde está la plantilla.
- Permiso de escritura sobre la carpeta de destino (donde se guardarán los documentos generados).
- No necesita conexión a Internet.

### Archivos con los que trabaja

DockGen **solo lee y escribe**, no envía tus datos a ningún servidor externo.

---

## 3. Instalación y primer arranque

### Si tienes el archivo ejecutable (`.exe` recomendado para el usuario normal)

1. Localiza el archivo `main.exe` (o el nombre que se haya entregado, por ejemplo `DockGen.exe`).
2. Haz **doble clic** sobre él.
3. Si Windows muestra la pantalla de "SmartScreen — Windows protegió su PC":
   - Pulsa en **"Más información"**.
   - Pulsa en **"Ejecutar de todas formas"**.
4. Aparecerá la ventana principal de DockGen. ¡Listo!

> :information_source: **No requiere instalación**. Es una aplicación portable. Puedes copiarla a una memoria USB y usarla en otro equipo.

### Si tu equipo es Mac o Linux

1. Descarga la versión correspondiente (por ejemplo `DockGen` sin extensión, o `.AppImage`).
2. En Mac, si el sistema lo bloquea, ve a **Preferencias del sistema → Privacidad y seguridad** y pulsa "Abrir de todas formas".
3. Haz doble clic para iniciar.

### Solución de problemas al arrancar

| Síntoma | Causa probable | Solución |
|---|---|---|
| Doble clic y no pasa nada | Sistema bloqueó el ejecutable | Ver instrucciones de SmartScreen arriba. |
| Mensaje "Falta una DLL" / "VCRUNTIME140" | Falta una librería de Windows | Instala *Microsoft Visual C++ Redistributable* desde la web oficial de Microsoft. |
| La ventana se abre y se cierra de inmediato | Sistema sin librerías gráficas muy antiguo | Actualiza el sistema o solicita la versión con instalador. |
| Ventana en blanco o con textos muy pequeños | Resolución de pantalla muy alta | Cambia la escala de pantalla desde *Configuración → Pantalla*. |

---

## 4. Conceptos que debes conocer

Antes de empezar conviene entender cuatro ideas básicas:

### :page_facing_up: Plantilla
Es un archivo Word (`.docx`) "tipo" con el formato y el texto fijo que quieres mantener. Contiene huecos que serán sustituidos por los datos de cada registro.

### :label: Marcador
Es **un texto cualquiera** que tú colocas en la plantilla para indicar qué parte se va a sustituir. Por convención se usan identificadores descriptivos como `Nombre_completo`, `Fecha_emision`, `Importe_total`, etc., pero **puede ser cualquier texto único**.

El programa busca ese texto en el documento y lo cambia por el valor correspondiente de la tabla de datos.

### :bar_chart: Datos
Es una tabla con filas y columnas. Cada **fila** es un documento nuevo a generar. Cada **columna** corresponde a un marcador de la plantilla.

Ejemplo de tabla:

| Nombre_completo | Fecha_emision | Importe_total |
|---|---|---|
| Ana García López | 12-03-2026 | 150,00 € |
| Pedro Suárez Vidal | 12-03-2026 | 220,00 € |

El resultado serán **dos documentos** Word, uno por fila, con los huecos rellenados.

### :open_file_folder: Carpeta de salida
Es la carpeta donde se guardarán los documentos generados.

---

## 5. Preparación de la plantilla de Word

### Paso 1 — Diseña el documento

Crea un `.docx` con el texto y formato que quieras mantener (logo, márgenes, encabezado, pie de página, etc.).

### Paso 2 — Inserta los marcadores

Escribe los marcadores **exactamente como aparecerán** en los nombres de columna de tu futura tabla de datos.

> :bulb: **Consejo:** usa un prefijo para identificarlos más fácilmente, por ejemplo `Nombre_completo:`, `Fecha_emision:`, `Importe_total:`. El texto a la izquierda de los dos puntos es el marcador; el texto posterior es solo contexto visual en el documento.
>
> Ejemplo dentro del Word:
> ```
> Estimado/a Nombre_completo:
>
> Por la presente se certifica que la cantidad de Importe_total euros
> ha sido abonada en la fecha Fecha_emision.
> ```

Una vez generados los documentos, esos marcadores serán sustituidos por el valor de la columna correspondiente, de modo que el Word finalizará como:

```
Estimado/a Ana García López:

Por la presente se certifica que la cantidad de 150,00 € euros
ha sido abonada en la fecha 12-03-2026.
```

### Paso 3 — Guarda la plantilla

Guarda el archivo como `.docx` (formato estándar de Word). **No uses el antiguo `.doc`**, DockGen no lo soporta.

### :warning: Cosas que debes evitar

- **Marcadores duplicados dentro de la misma plantilla.** Cada marcador debe aparecer solo en los puntos donde realmente quieras sustitución. Si la misma palabra aparece en otro lugar por casualidad, será reemplazada también. Elige nombres únicos.
- **Marcadores partidos entre varios "runs"** de Word. Si copias y pegas texto desde otro programa y Word lo divide en varios fragmentos internos, el reemplazo puede fallar. Para evitarlo:
  - Escribe los marcadores directamente en el Word, sin pegar.
  - O bien, después de pegarlos, reescríbelos a mano dentro del mismo párrafo.
- **Marcadores con espacios al principio o al final.** El programa procesa los nombres, pero procura que coincidan exactamente con el nombre de la columna.
- **Caracteres extraños en los nombres de columna.** Evita usar `:`, `?`, `/`, `\`, `*`. Si la columna se llama así, DockGen la limpia automáticamente (`Nombre:` pasa a `Nombre`), pero pueden perderse datos.

---

## 6. Conociendo la interfaz

Al abrir DockGen verás una pantalla dividida en **tres zonas principales**:

```
+----------------------------------------------------------+
| CABECERA: [ Desbloquear documento ] [ Generar documentos ]|
+----------------+-----------------------------------------+
| PANEL IZQUIERDO| PANEL DERECHO                          |
|                |                                        |
| [Plantilla]    | Registros                              |
|  [Seleccionar] | [Limpiar Todo] [Eliminar Filas Vacías]  |
|  [Carpeta sal.]| +-------------------------------------+ |
|                | | TABLA DE DATOS (editable)          | |
| [Marcadores]   | |                                    | |
|  [añadir...]   | |                                    | |
|  [chips]       | |                                    | |
|                | |                                    | |
| [Datos]        | |                                    | |
|  [Importar]    | +-------------------------------------+ |
|  [Añadir man.] |                                        |
|  [Extraer]     |                                        |
+----------------+-----------------------------------------+
```

### :triangular_ruler: Cabecera

| Elemento | Función |
|---|---|
| **Desbloquear documento** | Quita contraseñas / marcas "Solo lectura / Edición limitada" de un `.docx`. |
| **Generar documentos** | Crea todos los `.docx` finales (uno por fila de la tabla). |

### :open_file_folder: Sección *Plantilla*

- **Seleccionar plantilla** → abre un diálogo donde eliges el `.docx` con los marcadores.
- **Seleccionar carpeta de destino** → eliges dónde se guardarán los documentos generados.

Tras elegirlos aparece el **nombre** del archivo/carpeta como solo lectura.

### :label: Sección *Marcadores*

- Escribe un marcador en el campo de texto y pulsa **Enter** para añadirlo.
- Cada marcador aparece como un **chip** (botón con su nombre).
- **Haz clic en un chip** para eliminarlo.
- El botón con icono circular (esquina superior derecha) elimina **todos** los marcadores de una vez.

### :bar_chart: Sección *Datos*

| Botón | Qué hace |
|---|---|
| **Importar Datos** | Abre un archivo (CSV, XLSX, DOCX con tablas) y carga sus filas. |
| **Agregar Datos Manualmente** | Abre una pequeña ventana para escribir un registro a mano, campo por campo. |
| **Eliminar Columnas Vacías** | Quita aquellas columnas que estén vacías en todos los registros. |
| **Casilla "Extraer de Marcadores"** | Si está marcada y se carga un DOCX, en lugar de tomar sus tablas, DockGen busca los marcadores y extrae lo que hay después de cada uno. |

### :card_index_dividers: Panel *Registros*

Muestra la **tabla con todos los registros cargados**.

- Puedes **editar las celdas**: haz doble clic y escribe.
- Los cambios se aplican automáticamente.
- Si introduces un valor que no encaja con el tipo de la columna (por ejemplo, letras en una columna numérica), se mostrará un aviso y se revertirá el cambio.
- **Limpiar Todo** → elimina registros y marcadores.
- **Eliminar Filas Vacías** → borra las filas que estén completamente vacías.

---

## 7. Flujo de trabajo paso a paso

Trabaja siempre en este orden; saltarse pasos produce errores.

### :one: Preparar la plantilla (uno sola vez)

1. Abre Word y diseña tu documento.
2. Inserta los marcadores que necesites.
3. Guarda como `.docx`.

### :two: Preparar la tabla de datos

Puedes usar:
- **Excel** (recomendado por su sencillez).
- **CSV** (un único bloque de texto con columnas separadas por comas o punto y coma).
- **Otro Word** con una tabla.
- O bien escribir los datos manualmente más tarde.

Asegúrate de que **el nombre de cada columna coincide con el marcador** de la plantilla.

### :three: Arrancar DockGen

Doble clic sobre el ejecutable. La ventana principal aparece vacía.

### :four: Seleccionar la plantilla

1. Pulsa **Seleccionar plantilla**.
2. Elige tu `.docx`.
3. El nombre del archivo aparece como solo lectura bajo el botón.

### :five: Seleccionar la carpeta de salida

1. Pulsa **Seleccionar carpeta de destino**.
2. Elige (o crea) una carpeta donde se guardarán los resultados.
3. Aparece el nombre de la carpeta como solo lectura.

### :six: Cargar los datos

Tienes dos opciones:

- **Opción A — Importar:**
  1. Pulsa **Importar Datos**.
  2. Elige el archivo (`.xlsx`, `.csv` o `.docx` con tablas).
  3. Si el archivo es XLSX, DockGen te preguntará **en qué fila empieza la tabla** (escribe `1` si la primera fila es el encabezado).
  4. Si el archivo es DOCX con varias tablas, te mostrará una ventana para elegir cuál cargar.
  5. Las filas aparecen en el panel derecho.

- **Opción B — Manual:**
  1. Pulsa **Agregar Datos Manualmente**.
  2. Rellena la ventana que aparece.
  3. Pulsa **Guardar** para añadir una fila.
  4. Repite para cada registro.

> :bulb: Tras la primera carga, los **marcadores** se generan automáticamente a partir de los nombres de columna. Si quieres reordenarlos o renombrarlos, añade/elimina los chips manualmente.

### :seven: Revisar la tabla

- Comprueba que todas las celdas tengan el valor esperado.
- Corrige los errores tipográficos directamente en la celda (doble clic).
- Si te has equivocado de archivo, pulsa **Limpiar Todo** y vuelve al paso anterior.

### :eight: Generar los documentos

1. Pulsa **Generar documentos** en la cabecera.
2. Aparece un mensaje: "Se generaron N documento(s)".
3. Revisa la carpeta de destino: habrá un archivo `Document_<nombre>.docx` por cada fila.
4. El nombre del archivo se forma tomando el valor de la primera columna (por defecto), sustituyendo espacios por guiones bajos y barras por guiones.

### :nine: (Opcional) Desbloquear documentos protegidos

Si tu plantilla tenía contraseña o restricciones de edición:
- Pulsa **Desbloquear documento** antes de generar.
- DockGen elimina las marcas de protección y guarda una copia en la carpeta de destino.

---

## 8. Tipos de archivo de datos admitidos

DockGen detecta el tipo de archivo por su **extensión** y aplica una lógica distinta en cada caso.

| Extensión | Programa que lo abre | Cómo se interpreta | Limitaciones |
|---|---|---|---|
| `.csv` | Excel / Bloc de notas | Cada línea es una fila; la primera suele ser el encabezado. | El carácter separador (coma, punto y coma, tabulador) lo detecta la librería automáticamente. Si tu CSV tiene un formato muy particular, pre-procésalo en Excel. |
| `.xlsx` | Excel | Solo se admite la versión **xlsx** (no `xls` antiguo). Al cargarlo te pregunta en qué fila empieza la tabla. | Hojas con macros (`.xlsm`) **no** se soportan. Fórmulas: se importan los valores calculados (no la fórmula). |
| `.docx` (tablas) | Word | Lee todas las tablas del documento. Si hay varias, te pide elegir una. Si solo hay una, la usa automáticamente. Solo se carga la primera fila como encabezado. | Tablas anidadas o con celdas combinadas complejas pueden no importarse correctamente. Si activas *Extraer de marcadores*, en lugar de tablasDockGen analizará el texto siguiendo los marcadores. |
| `.docx` (texto + marcadores) | Word | Si activas la casilla *Extraer de Marcadores*, DockGen extrae el texto que sigue a cada marcador, separado por saltos de línea, tabulaciones o frases tipo "Etiqueta:". | Busca coincidencias literales. Si un marcador no existe en el documento, su valor quedará vacío. |
| `.json` | — | Estructura JSON estándar. | Soporte muy básico; se recomienda usar CSV/XLSX. |
| `.sav` | SPSS | Archivos de SPSS. | Necesita SPSS instalado; soporte limitado. |

> :warning: **Cualquier otra extensión** (TXT, ODS, RTF, PDF, etc.) **provocará un error** "Unsupported file format". Convierte previamente a CSV o XLSX.

### Convención de limpieza automática de nombres de columna

Para evitar problemas al generar nombres de archivo, DockGen aplica esta limpieza al cargar datos:

- Quita **espacios** al inicio y al final.
- Sustituye los **espacios internos** por guiones bajos (`_`).
- Elimina los **dos puntos** (`:`).

Ejemplo: la columna `Nombre: completo` se convierte en `Nombre_completo`. Asegúrate de que ese mismo identificador aparece en la plantilla, o ajústalo después añadiendo manualmente el marcador correspondiente.

---

## 9. Catálogo de errores y soluciones

A continuación, todos los mensajes que DockGen puede mostrar, con su causa y la forma de resolverlos.

### Mensajes en pantalla

| Mensaje (castellano de la app) | Cuándo aparece | Solución |
|---|---|---|
| *"No se ha seleccionado una plantilla. Por favor, seleccione una plantilla antes de importar datos."* | Pulsas *Importar Datos* sin haber elegido plantilla. | Primero pulsa *Seleccionar plantilla*. |
| *"No hay marcadores disponibles. Por favor, agregue marcadores antes de añadir registros."* | Pulsas *Agregar Datos Manualmente* o *Importar Datos* con la opción *Extraer de Marcadores* sin tener ningún marcador creado. | Añade al menos un marcador en el campo *Marcadores* antes de continuar. |
| *"El marcador no puede estar vacío"* | Pulsas Enter con el campo de marcador vacío. | Escribe un nombre antes de pulsar Enter. |
| *"El marcador 'XXX' ya existe."* | Intentas añadir un marcador que ya está en la lista. | Usa otro nombre distinto. |
| *"Archivo de Excel detectado. Por favor, ingrese el número de fila de la tabla que desea usar"* | Cargas un `.xlsx` y DockGen no sabe dónde empieza la tabla. | Indica el número de fila (por defecto `1`). |
| *"Número inválido. Por favor, ingrese un número válido."* | Respondiste con texto o un valor no numérico a la pregunta anterior. | Escribe un entero positivo (1, 2, 3…). |
| *"El archivo X fue omitido porque sus columnas no coinciden con los marcadores actuales."* | Importas un segundo archivo cuyas columnas no coinciden con las del primero. | Haz que los nombres de columna coincidan con los marcadores, o limpia todo y vuelve a empezar con un único archivo. |
| *"Tipo de valor inválido. Se esperaba {dtype}."* | Al editar una celda, introduces un valor no convertible al tipo original de la columna (p. ej., letras en un campo numérico). | Escribe un valor válido o edita la columna desde el archivo original. |
| *"No hay registros cargados."* | Pulsas *Eliminar selección* sin haber cargado datos. | Carga datos primero. |
| *"No se ha seleccionado ningún registro."* | Pulsas *Eliminar selección* sin haber seleccionado filas en la tabla. | Haz clic en la fila a borrar. |
| *"Confirmar eliminación — ¿Está seguro de que desea eliminar N registro(s) seleccionado(s)?"* | Al borrar varios registros a la vez. | Pulsa *Sí* para confirmar o *No* para cancelar. |
| *"Documento Desbloqueado"* / *"Error al desbloquear"* | Al usar la función *Desbloquear Documento*. | Si aparece error, comprueba que el archivo no esté abierto en otro programa. |
| *"Se generaron N documento(s)."* | Generación correcta. | No requiere acción. Verifica los archivos en la carpeta de salida. |

### Errores no traducidos (mensajes técnicos en inglés o cierre de la app)

| Mensaje técnico | Significado | Solución |
|---|---|---|
| `Unsupported file format` | El archivo de datos tiene una extensión no admitida. | Conviértelo a `.csv`, `.xlsx` o `.docx`. |
| `output_folder is required to generate documents` | No has elegido carpeta de salida y has pulsado *Generar documentos*. | Selecciona primero la *Carpeta de destino*. |
| `data must be a pandas DataFrame` | Error interno; suele indicar archivo de datos vacío o ilegible. | Comprueba que el archivo no esté dañado; prueba abrirlo en Excel. |
| `LibreOffice no encontrado. Instálalo desde https://www.libreoffice.org/` | Intentas convertir a PDF sin tener LibreOffice. | Instala LibreOffice. |
| `Error al convertir {archivo}: ...` | LibreOffice no pudo convertir el archivo a PDF. | Verifica que el `.docx` no esté corrupto y que tengas permisos de escritura en la carpeta destino. |
| Ventana se cierra al abrir | Falta una dependencia del sistema. | Reinstala *Microsoft Visual C++ Redistributable* o usa otra versión de DockGen. |
| La tabla aparece vacía tras importar | El archivo no contenía datos o la fila de importación era incorrecta. | Vuelve a importar indicando la fila correcta (normalmente `1`). |
| El icono del programa no aparece | No es un error; tu carpeta no contiene los Assets. | Contacta con soporte; algunos archivos son necesarios para mostrar los iconos. |
| Elimina todos los marcadores al pulsar el botón circular | Estás pulsando *Limpiar Todo* por confusión. | Si solo quieres eliminar algunos, haz clic en cada chip individualmente. |
| Al editar una celda el cambio se revierte | Estás escribiendo un valor del tipo incorrecto. | Ajusta el valor al tipo esperado. |

---

## 10. Cómo funciona por dentro

Si tienes curiosidad, esta sección explica el proceso en términos sencillos (sin entrar en código).

### :mag: Paso a paso simplificado

```
   PLANTILLA (.docx)                          DATOS (tabla)
       │                                          │
       │                                          │
       └──────────────┬───────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Por cada FILA de la tabla │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌─────────────────────────────┐
        │  Copia la plantilla (.docx) │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │  Busca cada marcador y lo       │
        │  sustituye por el valor de la  │
        │  columna correspondiente       │
        └──────────────┬──────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │  Guarda como Document_<valor1> │
        │  .docx en la carpeta elegida   │
        └─────────────────────────────────┘
```

### Lo que ocurre "por la trastienda"

1. **Lectura de la plantilla.** DockGen abre tu `.docx` y carga su estructura (párrafos del cuerpo, encabezados, pies de página). Detecta además si hay protección activada.

2. **Conversión de datos.** La tabla que importas se interpreta con la librería *pandas*. Cada columna mantiene su tipo de dato (texto, número entero, número decimal, fecha). Esto permite que, si editas después una celda, DockGen pueda avisarte cuando el valor sea incompatible.

3. **Generación en bucle.** Para cada fila:
   - Se abre **una copia independiente** de la plantilla. La plantilla original nunca se modifica.
   - Se recorre cada párrafo del documento (incluyendo los de encabezados y pies de página buscando etiquetas de marcador) buscando los textos exactos de cada marcador.
   - Cada coincidencia se reemplaza por el valor de la columna que tenga el mismo nombre.
   - El archivo se guarda con un nombre seguro (espacios → `_`, barras → `-`). Si no hay valor para usar como nombre, se usa `row_1`, `row_2`, etc.

4. **Extrabucción desde Word (modo *Extraer de Marcadores*).** En este modo, DockGen usa expresiones regulares (búsqueda de patrones de texto) para localizar cada marcador y tomar todo el texto que aparece a continuación, hasta encontrar otro marcador o un patrón de "Etiqueta:".

5. **Desbloqueo.** Si la plantilla tenía marcas de protección (w:documentProtection / w:writeProtection), DockGen las elimina antes de generar.

### Privacidad

- DockGen trabaja **en local**. Ningún dato se envía a Internet.
- Los archivos generados se crean en la carpeta de destino que tú elijas.

---

## 11. Preguntas frecuentes (FAQ)

**P: ¿Qué pasa si me equivoco de plantilla después de cargar datos?**
R: DockGen recuerda la plantilla seleccionada, pero la puedes cambiar pulsando otra vez *Seleccionar plantilla*. Los datos cargados no se pierden, aunque ten en cuenta que los nombres de columna deben coincidir con los nuevos marcadores; de lo contrario la sustitución no funcionará.

**P: ¿Puedo usar una plantilla protegida con contraseña?**
R: Sí. Primero pulsa *Desbloquear documento* para crear una copia sin protección y luego trabaja con esa copia.

**P: ¿Hay límite de filas?**
R: No hay un límite duro. El programa puede manejar tablas grandes, pero cuanto más grande sea el documento, más tardará. Miles de filas pueden tomar varios minutos.

**P: ¿Por qué mis archivos se llaman `Document_<algo>` y no con otro formato?**
R: Por defecto DockGen usa el valor de la primera columna para nombrar el archivo. Los caracteres problemáticos (espacios, barras) se reemplazan automáticamente para mantener nombres válidos en Windows, Mac y Linux.

**P: ¿Puedo abrir un archivo `.xls` (formato antiguo)?**
R: No directamente. Ábrelo en Excel y *Guardar como…* `.xlsx`.

**P: ¿Por qué al pulsar Enter sobre la tabla me salta de celda pero no edita?**
R: La tabla está pensada para edición con doble clic. Pulsa Enter dentro de una celda para confirmar el cambio una vez hayas escrito el valor.

**P: ¿Por qué no puedo escribir tildes ni acentos en la plantilla?**
R: Sí puedes. Las plantillas pueden contener tildes, eñes y cualquier carácter Unicode. Solo asegúrate de que el *archivo de plantilla* esté codificado correctamente al guardarlo desde Word.

**P: ¿Los archivos generados respetan el formato (negrita, cursiva, estilos)?**
R: Sí, los formatos se mantienen. Lo único que cambia es el texto sustituido; conserva la fuente, tamaño y estilo del marcador original.

**P: He añadido un marcador pero no aparece en los chips. ¿Qué ha pasado?**
R: Probablemente escribiste un marcador que ya existía o dejaste el campo vacío. DockGen muestra un mensaje emergente en ambos casos.

**P: ¿Cómo cambio el idioma de la interfaz?**
R: La interfaz principal está en español. Existe soporte para inglés, pero el cambio requiere editar el archivo de configuración; consulta con el administrador de tu organización si lo necesitas.

**P: ¿La aplicación modifica mis archivos originales?**
R: No. La plantilla original **nunca** se modifica. Si usas *Desbloquear Documento*, DockGen guarda una copia sin protección en la carpeta de destino.

---

## 12. Glosario rápido

| Término | Significado |
|---|---|
| **Plantilla** | Archivo Word base sobre el que se generan los documentos finales. |
| **Marcador** | Texto que aparece en la plantilla y será reemplazado por un valor. |
| **Dato / Registro** | Una fila de la tabla; equivale a un documento generado. |
| **Columna** | Cada campo de la tabla (se corresponde con un marcador). |
| **Carpeta de salida** | Carpeta donde DockGen guarda los documentos generados. |
| **CSV** | Archivo de texto plano con valores separados por comas. |
| **XLSX** | Formato estándar de hoja de cálculo de Excel (a partir de 2007). |
| **DOCX** | Formato estándar de documento Word (a partir de 2007). |
| **PDF** | Formato de documento portable (solo lectura). Requiere LibreOffice. |
| **Desbloquear** | Quitar marcas de protección ("Solo lectura", "Edición limitada") del documento. |
| **Token / Run** | Fragmento interno de texto dentro de un párrafo de Word. |

---

## 13. Soporte y versión

### Versión del manual

- **Manual:** 1.0
- **Aplicación:** DockGen (WordModifier)

### Soporte

Si encuentras un problema no cubierto en este manual:

1. Vuelve a leer la sección :point_right: **[Catálogo de errores y soluciones](#9-cat%C3%A1logo-de-errores-y-soluciones)**.
2. Comprueba que tu sistema cumple los [Requisitos previos](#2-requisitos-previos).
3. Si utilizas una versión corporativa, contacta con el administrador o soporte interno.
4. Si eres usuario particular, vuelve a descargar la última versión desde la fuente original.

### Información útil para reportar un problema

Cuando contactes con soporte, incluye:

- Sistema operativo y versión (ej. *Windows 11 23H2*).
- Pasos exactos que seguiste antes del error.
- Mensaje de error (si lo hay, copia el texto literal).
- Tipo de archivo que intentabas procesar (extensión y tamaño aproximado).

---

> :lock: **Aviso legal.** DockGen trabaja sobre tus archivos en local. Asegúrate de cumplir la normativa vigente de protección de datos personales aplicable a la información que procesas.
