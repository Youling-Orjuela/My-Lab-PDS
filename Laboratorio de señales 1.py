# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 15:49:44 2025

@author: andre
"""

import wfdb
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Nombre del archivo del registro
ecg1 = 'a02'

try:
    # Leer el archivo del registro
    record = wfdb.rdrecord(ecg1)
except FileNotFoundError:
    print(f"Archivo '{ecg1}' no encontrado.")
    exit()

# Extraer la señal, etiquetas, frecuencia de muestreo y tiempo
senal = record.p_signal
etiquetas = record.sig_name
frecuencia = record.fs  # Frecuencia de muestreo
tiempo = np.arange(senal.shape[0]) / frecuencia  # Crear vector de tiempo

# Filtrar los primeros 10 segundos
duracion_segundos = 10
muestras_10s = int(frecuencia * duracion_segundos)  # Número de muestras en 10 segundos
senal_10s = senal[:muestras_10s]  # Cortar señal
tiempo_10s = tiempo[:muestras_10s]  # Cortar tiempo

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

# Parte de estadistica con señal de 10 segundos
print('Datos estadísticos con el empleo de funciones: ')
print ('La media es: ',np.mean(senal_10s))
print ('La desviación estándar es: ', np.std(senal_10s))
print ('El coeficiente de variación es: ', (np.std(senal_10s)/ np.mean(senal_10s)))

#sin funciones
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

print('Datos estadísticos sin el empleo de funciones: ')
print('La media es:',media)
print ('La desviación es: ',desviacion)
print('El coeficiente de variación es: ', coeficiente)
#Histograma
plt.figure(figsize=(10, 6))
sns.histplot(senal_10s, bins=50, color='blue', edgecolor='black', alpha=0.7, kde=True)
# Configurar el gráfico
plt.title('Histograma y Densidad de Probabilidad de la Señal ECG (Primeros 10 segundos)')
plt.xlabel('Amplitud (mV)')
plt.ylabel('Densidad de Probabilidad')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# Parámetros del ruido gaussiano
med = 0          # Media de la distribución
desviacion_std = 0.1 # Desviación estándar de la distribución

# Generar ruido gaussiano
"ruido_gaussiano = np.random.normal(med, desviacion_std, len(senal_10s))"
x = np.random.randn(1000)
plt.plot(x, '.-')
plt.show()
ruido = x.reshape(-1, 1)
ruido2=ruido*0.06
senal_ruidosa= ruido + senal_10s

senal_ruidosa2= ruido2 + senal_10s


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

Ps = np.mean(np.abs(senal_ruidosa)**2)
Pn = np.mean(np.abs(ruido)**2)

SNRdB = 10*np.log10(Ps/Pn)
print(Ps)
print (Pn)
print(SNRdB)

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

Ps = np.mean(np.abs(senal_ruidosa2)**2)
Pn = np.mean(np.abs(ruido2)**2)

SNRdB = 10*np.log10(Ps/Pn)
print(Ps)
print (Pn)
print(SNRdB)


#Ruido impulso



# Generar ruido de impulso en un rango entre el 20% del valor mínimo y el 30% del valor máximo de la señal
noise_sample = np.random.default_rng().uniform(0.2 * min(senal_10s), 0.3 * max(senal_10s), int(0.03 * len(senal_10s)))

# Crear un vector de ceros que tenga la misma longitud que la señal original
zeros = np.zeros(len(senal_10s) - len(noise_sample))

# Concatenar el ruido con ceros
noise = np.concatenate([noise_sample, zeros])

# Asegurarse de que la longitud del ruido coincida con la longitud de la señal
if len(noise) != len(senal_10s):
    raise ValueError("La longitud del ruido no coincide con la longitud de la señal.")

# Mezclar aleatoriamente el ruido
np.random.shuffle(noise)

# Agregar el ruido a la señal original
y_noised = senal_10s + noise

# Graficar la señal con ruido
plt.figure(figsize=(10, 5))
plt.title("Señal ECG con Ruido de Impulso")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud (mV)")
plt.plot(tiempo_10s, y_noised, label='ECG con ruido de impulso', color='green')
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim([0, duracion_segundos])
plt.ylim(np.min(y_noised) - 0.1, np.max(y_noised) + 0.1)
plt.legend()
plt.tight_layout()
plt.show()


"""
#Histograma
count, bins, _ = plt.hist(senal_10s, bins=50, density=False, color='blue', edgecolor='black', alpha=0.7)
plt.grid(True)
plt.show()
"""

"""# Parte de estadistica con toda la señal
print ('La media es: ',np.mean(senal))
print ('La desviación estándar es: ', np.std(senal))
print ('El coeficiente de variación es: ', np.mean(senal)/np.std(senal))
"""
"""
plt.hist(senal, bins=50, color='blue', edgecolor='black', alpha=0.7)
plt.grid(True)
plt.show()
"""
"""
print(len(senal))
print(sum(senal)/len(senal))
"""
"""
media=sum(senal_10s)/len(senal_10s)
desviacion1=(sum ((senal_10s-media)**2)) / (len(senal_10s)-1)
desviacion=desviacion1**0.5
coeficiente= (desviacion / media)
"""