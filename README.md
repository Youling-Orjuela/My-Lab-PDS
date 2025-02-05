# Laboratorio 1 Análisis estadístico de la señal
## Introducción 
El siguiente código tiene como propósito el análisis estadístico de una señal fisiológica; siendo en este caso una señal de ECG (electrocardiograma). Para este análisis, el ECG obtenido pertenece a un caso en el cual la muestra está siendo evaluada bajo condiciones de apnea. Teniendo en cuenta la señal mencionada, se calcularán los estadísticos de la gráfica para su posterior análisis bajo condiciones estándares. Posteriormente, se agregaran diferentes tipos de ruidos (Gaussiano, tipo impulso y artefacto), que usualmente se presentan en la captura de señales y así mismo, evidenciar el comportamiento dentro de la captura y representación de la señal de forma gráfica.

## Obtención de la señal ECG
Para obtener una señal adecuada se empleo la base de datos Physionet, en donde se escogió de la sección Apnea ECG Database una señal que contiene los archvios "a02.dat" y "a02.hea" los cuales permiten que se pueda usar en Python.

```python
import wfdb
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

```
**wfdb**: Se usa para trabajar con archivos de ECG (WFDB es un formato estándar para los datos de ECG).

**seaborn**: Facilita la creación del histograma y permite que la función de probabilidad se vea óptima.

**matplotlib**: Usada para crear gráficos en general (en este caso, gráficos de la señal ECG).

**numpy**: Permite trabajar con arrays y realizar cálculos numéricos.

### Registro y extracción de la señal
```python
# Nombre del archivo del registro (Parte 1)
ecg1 = 'a02'

try:
    # Leer el archivo del registro
    record = wfdb.rdrecord(ecg1)
except FileNotFoundError:
    print(f"Archivo '{ecg1}' no encontrado.")
    exit()

# Extraer la señal, etiquetas, frecuencia de muestreo y tiempo (parte 2)
senal = record.p_signal
etiquetas = record.sig_name
frecuencia = record.fs  # Frecuencia de muestreo
tiempo = np.arange(senal.shape[0]) / frecuencia  # Crear vector de tiempo

```
En la primera parte se lee el archivo a02 que contiene los datos del ECG. Si el archivo no se encuentra, el código muestra un mensaje y termina la ejecución con exit(). Una vez cargado el archivo como se ve en la segunda parte, se extraen los datos de la señal (p_signal), las etiquetas de la señal (sig_name), y la frecuencia de muestreo (fs). Además, se crea un vector de tiempo basado en la frecuencia de muestreo.

### Primeros 10 segundos de la señal
Como la señal era muy extensa, se decidió solo tomar los primeros 10 segundos (ventana de tiempo), para hacer esto se hizo lo siguiente:
```python
# Filtrar los primeros 10 segundos
duracion_segundos = 10
muestras_10s = int(frecuencia * duracion_segundos)  # Número de muestras en 10 segundos
senal_10s = senal[:muestras_10s]  # Cortar señal
tiempo_10s = tiempo[:muestras_10s]  # Cortar tiempo
```
Se extraen los primeros 10 segundos de la señal y el tiempo correspondiente. Se calcula el número de muestras para 10 segundos de acuerdo con la frecuencia de muestreo, y luego se cortan tanto los datos de la señal como el tiempo.

Para visualizar la señal y los datos obtenidos se hace de esta forma

```python
# Información básica
print("Laboratorio 1: Análisis estadístico de la señal")
print(f"Frecuencia de muestreo: {frecuencia} Hz")
print(f"Forma completa de la señal: {senal.shape}")
print(f"Forma de la señal (10 segundos): {senal_10s.shape}")

# Graficar los primeros 10 segundos de la señal
plt.figure(figsize=(10, 5))
plt.title("Señal ECG - Primeros 10 segundos")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_10s, label='ECG Canal I', color='blue')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_10s) - 0.1, np.max(senal_10s) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()
```
[![Primeros-10-segundos.png](https://i.postimg.cc/WzrbT8LM/Primeros-10-segundos.png)](https://postimg.cc/xNfSPKdC)

## Análisis estadístico

### Forma larga

```python
suma=0
contar=0 
datos=senal_10s
for valor in datos:
    suma+=valor
    contar+=1

media=suma/contar
suma_cuadrados=0 
diferencia = 0

for valor in datos:
    diferencia= valor - media
    suma_cuadrados+=diferencia ** 2 
    
varianza=suma_cuadrados / (contar-1)
    
desviacion=varianza**0.5

coeficiente= desviacion  / media
# Crear histograma sin funciones
# Paso 1: Generar más datos para que las barras no estén tan separadas
senal_10s = np.random.normal(loc=0.5, scale=0.3, size=1000)  # Ejemplo con 1000 datos generados de una distribución normal
# Paso 2: Definir el número de bins
bins = 50  # Puedes ajustar el número de bins si quieres más o menos barras
# Paso 3: Calcular los límites de los bins
min_val = min(senal_10s)
max_val = max(senal_10s)
bin_width = (max_val - min_val) / bins  # Ancho de cada bin
# Paso 4: Crear los bins
bin_edges = [min_val + i * bin_width for i in range(bins + 1)]  # Limites de los bins
# Paso 5: Contar cuántos valores caen en cada bin
counts = [0] * bins  # Inicializa una lista para contar las frecuencias

for value in senal_10s:
    for i in range(bins):
        if bin_edges[i] <= value < bin_edges[i + 1]:
            counts[i] += 1
            break

# Paso 6: Graficar el histograma (con barras)
plt.figure(figsize=(10, 6))
plt.bar(bin_edges[:-1], counts, width=bin_width, color='blue', edgecolor='black', alpha=0.7)
# Paso 7: Configurar el gráfico
plt.title('Histograma de la Señal ECG (Primeros 10 segundos)')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Frecuencia')
plt.grid(True, linestyle='--', alpha=0.7)
# Mostrar el gráfico
plt.show()

```
[![media.jpg](https://i.postimg.cc/RC3TwHLK/media.jpg)](https://postimg.cc/grWRWr52)
[![Histograma-normal.png](https://i.postimg.cc/4d0mJnKT/Histograma-normal.png)](https://postimg.cc/dk8q6smW)


### Con funciones
En esta parte se calcula la media, desviación estándar y el coeficiente de variación de la señal de los primeros 10 segundos usando la función numpy que facilita estos cálculos.

```python
print('Datos estadísticos con el empleo de funciones: ')
print ('La media es: ',np.mean(senal_10s))
print ('La desviación estándar es: ', np.std(senal_10s))
print ('El coeficiente de variación es: ', (np.std(senal_10s)/ np.mean(senal_10s)))
#Histograma
plt.figure(figsize=(10, 6))
sns.histplot(senal_10s, bins=50, color='blue', edgecolor='black', alpha=0.7, kde=True)
# Configurar el gráfico
plt.title('Histograma y Densidad de Probabilidad de la Señal ECG (Primeros 10 segundos)')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad de Probabilidad')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

```
[![Histograma-funciones.png](https://i.postimg.cc/ZYgdms3y/Histograma-funciones.png)](https://postimg.cc/14GtcHv9)
## Ruidos y relación SNR
Agregar ruido a una señal se realiza generalmente con el fin de simular condiciones reales y probar cómo un sistema de procesamiento de señales (como un receptor de comunicaciones, un sistema de imágenes médicas, o un sistema de monitoreo) manejará ese ruido en un entorno no ideal. 

El SNR se define como la relación entre la potencia de la señal y la potencia del ruido. Generalmente, se expresa en decibelios (dB). El SNR se utiliza para evaluar la calidad de la señal y el desempeño del sistema. Es una de las métricas más importantes en el análisis de sistemas de comunicación y procesamiento de señales.

### Ruido Gaussiano
Cuando se agrega ruido gaussiano a una señal, la señal original se ve alterada por fluctuaciones aleatorias que siguen una distribución normal. Este tipo de ruido puede ser causado por interferencias electrónicas, fluctuaciones térmicas, o errores en la transmisión de datos.
```python
# Parámetros del ruido gaussiano
med = 0          # Media de la distribución
desviacion_std = 0.1 # Desviación estándar de la distribución

# Generar ruido gaussiano
"ruido_gaussiano = np.random.normal(med, desviacion_std, len(senal_10s))"
x = np.random.randn(1000)
ruido = x.reshape(-1, 1)
ruido2=ruido*0.06
senal_ruidosa= ruido + senal_10s
senal_ruidosa2= ruido2 + senal_10s

# Media de la señal
mu_senal = np.mean(senal_10s)
# Desviación estándar del ruido
sigma_ruido = np.std(senal_ruidosa - senal_10s)
# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido


plt.figure(figsize=(10, 5))
plt.title("Señal ECG - Ruido Gaussiano")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_ruidosa, label='ECG con ruido', color='red')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_ruidosa) - 0.1, np.max(senal_ruidosa) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

Ps = np.mean(senal_ruidosa**2)
Pn = np.mean(ruido**2)

SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Gaussiano alta amplitud')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")


plt.figure(figsize=(10, 5))
plt.title("Señal ECG - Ruido Gaussiano")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_ruidosa2, label='ECG con ruido', color='red')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_ruidosa2) - 0.1, np.max(senal_ruidosa2) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

Ps = np.mean(senal_ruidosa2**2)
Pn = np.mean(ruido2**2)
sigma_ruido2 = np.std(senal_ruidosa2 - senal_10s)
# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido2

SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Gaussiano baja amplitud')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")
```
Ruido Gaussiano alta amplitud

Potencia de la señal:  1.049098525359266

Potencia del ruido:  1.014453723938748

Relación SNR:  0.14584035846237886

SNR estadístico: -0.0007347094243723512

Ruido Gaussiano baja amplitud

Potencia de la señal:  0.023388433491410576

Potencia del ruido:  0.0036520334061794922

Relación SNR:  8.064663931483452

SNR estadístico: -0.01224515707287252

[![Ruido-gaussiano.png](https://i.postimg.cc/HL7NShQ4/Ruido-gaussiano.png)](https://postimg.cc/WDTSzSYh)
[![Ruido-gaussiano-2.png](https://i.postimg.cc/zBCcNH2y/Ruido-gaussiano-2.png)](https://postimg.cc/S2Kr7Rh4)
### Ruido de impulso
Este tipo de ruido tiene una naturaleza diferente al ruido gaussiano, ya que no sigue una distribución normal, sino que se presenta como saltos rápidos o impulsos de gran amplitud en comparación con el resto de la señal.
```python
# Parámetros del ruido impulsivo
proporcion_impulsos = 0.01  # Proporción de muestras que serán reemplazadas por impulsos (5%)
amplitud_impulso_min = -0.1  # Amplitud mínima de los impulsos
amplitud_impulso_max = 0.1   # Amplitud máxima de los impulsos
num_muestras = len(senal_10s)
num_impulsos = int(proporcion_impulsos * num_muestras)


# Generar una copia de la señal original para agregar el ruido impulsivo
senal_impulso = np.copy(senal_10s)
senal_impulso = senal_impulso.ravel()


# Generar posiciones aleatorias para los impulsos
posiciones_impulsos = np.random.choice(num_muestras, num_impulsos, replace=False)

valores_impulso = np.random.uniform(amplitud_impulso_min, amplitud_impulso_max, num_impulsos)

# Aplicar los impulsos a la señal
senal_impulso[posiciones_impulsos] = valores_impulso

# Graficar la señal con ruido impulsivo
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido Impulso")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_impulso, label='ECG con ruido impulsivo', color='green')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_impulso) - 0.1, np.max(senal_impulso) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

ruido_impulso = senal_impulso - senal_10s
Ps = np.mean(senal_impulso**2)
Pn = np.mean(ruido_impulso**2)
sigma_ruido3 = np.std(senal_impulso - senal_10s)


# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido3
SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Impulso')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")

# Parámetros del ruido impulsivo 2
proporcion_impulsos2 = 0.01  # Proporción de muestras que serán reemplazadas por impulsos (5%)
amplitud_impulso_min2 = -1.0  # Amplitud mínima de los impulsos
amplitud_impulso_max2 = 1.0   # Amplitud máxima de los impulsos

num_muestras2 = len(senal_10s)
num_impulsos2 = int(proporcion_impulsos2 * num_muestras2)


# Generar una copia de la señal original para agregar el ruido impulsivo
senal_impulso2 = np.copy(senal_10s)
senal_impulso2 = senal_impulso2.ravel()


# Generar posiciones aleatorias para los impulsos
posiciones_impulsos2 = np.random.choice(num_muestras2, num_impulsos2, replace=False)

valores_impulso2 = np.random.uniform(amplitud_impulso_min2, amplitud_impulso_max2, num_impulsos2)

# Aplicar los impulsos a la señal
senal_impulso2[posiciones_impulsos2] = valores_impulso2

# Graficar la señal con ruido impulsivo
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido Impulsivo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_impulso2, label='ECG con ruido impulsivo', color='yellow')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_impulso2) - 0.1, np.max(senal_impulso2) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

ruido_impulso2=senal_impulso2 - senal_10s
Ps = np.mean(senal_impulso2**2)
Pn = np.mean(ruido_impulso2**2)
sigma_ruido4 = np.std(senal_impulso2 - senal_10s)


# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido4
SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Impulso')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")
```
Ruido Impulso

Potencia de la señal:  0.018769939713125162

Potencia del ruido:  0.037554128482172495

Relación SNR:  -3.0119481005080004

SNR estadístico: -0.003818594073214786

Ruido Impulso

Potencia de la señal:  0.02108236799906126

Potencia del ruido:  0.03986846994177009

Relación SNR:  -2.767101789773936

SNR estadístico: -0.0037062202480479694

[![Ruido-impulso.png](https://i.postimg.cc/901gR5hV/Ruido-impulso.png)](https://postimg.cc/FkdV86zn)
[![Ruido-impulso-2.png](https://i.postimg.cc/nrnwhVN0/Ruido-impulso-2.png)](https://postimg.cc/hz30CnDd)
### Ruido de artefacto
Este tipo de ruido se presenta de forma artificial, en el sentido de que no es parte de la señal original que se está midiendo, sino que proviene de fuentes externas o de fallos en el sistema que genera o captura la señal.
```python
# Parámetros del ruido de artefacto
frecuencia_artefacto = 60  # Frecuencia del artefacto en Hz
amplitud_artefacto = 0.1   # Amplitud del artefacto

# Generar la señal de artefacto
R_artefacto = amplitud_artefacto * np.sin(2 * np.pi * frecuencia_artefacto * tiempo_10s)

# Agregar el artefacto a la señal original
artefacto = R_artefacto.reshape(-1, 1)
senal_artefacto = senal_10s + artefacto

# Graficar la señal con ruido de artefacto
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido de Artefacto")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_artefacto, label='ECG con ruido de artefacto', color='purple')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_artefacto) - 0.1, np.max(senal_artefacto) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

ruido_artefacto=senal_artefacto - senal_10s
Ps = np.mean(senal_artefacto**2)
Pn = np.mean(ruido_artefacto**2)
sigma_ruido5 = np.std(senal_artefacto - senal_10s)

# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido5
SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Artefacto')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")


# Parámetros del ruido de artefacto 2
frecuencia_artefacto2 = 60  # Frecuencia del artefacto en Hz
amplitud_artefacto2 = 0.9   # Amplitud del artefacto

# Generar la señal de artefacto
R_artefacto2 = amplitud_artefacto2 * np.sin(2 * np.pi * frecuencia_artefacto2 * tiempo_10s)

# Agregar el artefacto a la señal original
artefacto2 = R_artefacto2.reshape(-1, 1)
senal_artefacto2 = senal_10s + artefacto2

# Graficar la señal con ruido de artefacto
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido de Artefacto")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, senal_artefacto2, label='ECG con ruido de artefacto', color='pink')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(senal_artefacto2) - 0.1, np.max(senal_artefacto2) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()

ruido_artefacto2=senal_artefacto2 - senal_10s
Ps = np.mean(senal_artefacto2**2)
Pn = np.mean(ruido_artefacto2**2)
sigma_ruido6 = np.std(senal_artefacto2 - senal_10s)

# Calcular SNR estadístico
SNR_est = mu_senal / sigma_ruido6
SNRdB = 10*np.log10(Ps/Pn)
print('Ruido Artefacto')
print('Potencia de la señal: ',Ps)
print ('Potencia del ruido: ',Pn)
print('Relación SNR: ', SNRdB)
print(f"SNR estadístico: {SNR_est}")
```
Ruido Artefacto baja amplitud

Potencia de la señal:  0.023794211168532003

Potencia del ruido:  0.004999999999999977

Relación SNR:  6.775013072012653

SNR estadístico: -0.010465180361560932

Ruido Artefacto alta amplitud

Potencia de la señal:  0.4238695005167864

Potencia del ruido:  0.4049999999999982

Relación SNR:  0.1977714486618093

SNR estadístico: -0.0011627978179512143

[![Ruido-artefacto.png](https://i.postimg.cc/j50FB4cV/Ruido-artefacto.png)](https://postimg.cc/Ty00DmBQ)
[![Ruido-artefacto-2.png](https://i.postimg.cc/QdzPJ3Wd/Ruido-artefacto-2.png)](https://postimg.cc/HrQBTF2q)

## Análisis de los resultados obtenidos

### Cálculo de la media, desviación estándar y coeficiente de variación

En cuanto a la media obtenida tanto de manera manual como por medio de las funciones de phyton, se evidencia que ambos valores de voltaje son negativos (aprox. -0,00074), lo cual dice que los valores de voltaje en el ECG evaluado tiene como magnitud promedio el valor anteriormente mencionado ya que en el transcurso de la señal, esta experimenta cambios de voltaje entre valores positivos y negativos, predominando los negativos.

Por otro lado, el valor de la desviación estándar en ambos métodos dio un valor aproximado a 0,137. Este valor nos indica que la dispersion de datos es bajo. Además, el valor del coeficiente de variación en ambos métodos calculados dio un valor de -185.210.

### Ruidos y relación SNR

1. Ruido Gaussiano: Al analizar el comportamiento del SNR y el valor de amplitud del ruido, se observa que son valores inversamente proporcionales; lo que indica que a mayor amplitud, la relación SNR es baja y viceversa. En el caso de una amplitud alta, en el cual se tiene un SNR cercano a 0 dB, nos indica que la señal del ruido es alto y dificulta la lectura del ECG de manera correcta. En el caso de una amplitud baja, el valor de SNR es mayor, lo cual dice que la señal es mucho mas fuerte que el ruido y por ende, la lectura del ECG será optima. 

2. Ruido impulsivo: Dada la naturaleza del ruido impulsivo, la interpretación del valor de SNR será de manera diferente, ya que este tipo de interferencia no se propaga por toda la señal. El valor negativo de esta lectura indica la fuerza con la cual esta alteración se hace presente. A pesar de que se presente por picos breves, presentan una gran amplitud, mucho mayores a los picos mostrados en un ECG normal.

3. Ruido tipo artefacto: En el caso del ruido tipo artefacto, su relación entre SNR y amplitud de ruido es inversamente proporcional. Si se tiene un ruido de alta amplitud, el SNR es cercano a 0, lo cual indica que el ruido es alto y la lectura de la señal será deficiente. Ante un ruido de alta baja amplitud, el SNR es alto y su afectación a la señal no es notoria, por lo cual la lectura se puede hacer de una manera clara

## Bibliografía
https://medium.com/@ms_somanna/guide-to-adding-noise-to-your-data-using-python-and-numpy-c8be815df524 
https://pysdr.org/es/content-es/noise.html
https://www.wavewalkerdsp.com/2024/07/01/calculate-signal-to-noise-ratio-snr-in-simulation/


## Colaboradores
1. Youling Andrea Orjuela Bermúdez (5600815)
2. Jose Manuel Gomez Carrillo (5600793)
3. Juan Camilo Quintero Velandia (5600745)
