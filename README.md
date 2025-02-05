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
wfdb se usa para trabajar con archivos de ECG (WFDB es un formato estándar para los datos de ECG).
seaborn permite que 
matplotlib: Para crear gráficos en general (en este caso, gráficos de la señal ECG).
numpy: Para trabajar con arrays y realizar cálculos numéricos.
2. Lectura de la Señal ECG
python
Copiar
ecg1 = 'a02'

## Análisis estadístico
### Forma larga
### Con funciones
## Ruidos y relación SNR
### Ruido Gaussiano
### Ruido de impulso
### Ruido de artefacto
