# Laboratorio 1
##Parte estadística
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
