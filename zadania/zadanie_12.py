import random
import numpy as np
import matplotlib.pyplot as plt
from qgis.core import (
    QgsPointXY,
    QgsRasterLayer,
    QgsRaster,
    QgsProject
)

# Ustawienie ziarna dla powtarzalnych wyników
random.seed(999)

# Generowanie losowych współrzędnych punktów
x_coordinates = random.choices(range(0, 1000, 10), k=100)
y_coordinates = random.choices(range(0, 1000, 10), k=100)

# Tworzenie listy obiektów punktowych (QgsPointXY)
punkty = [QgsPointXY(x, y) for x, y in zip(x_coordinates, y_coordinates)]

# Ścieżki do plików rastrowych
kanal1_sciezka = "Landsat_B1.tif"
kanal2_sciezka = "Landsat_B2.tif"

# Wczytanie rastrów jako QgsRasterLayer
kanal1 = QgsRasterLayer(kanal1_sciezka, "Kanał 1")
kanal2 = QgsRasterLayer(kanal2_sciezka, "Kanał 2")

if not kanal1.isValid() or not kanal2.isValid():
    raise ValueError("Nie udało się wczytać plików rastrowych.")

# Pobranie wartości rastra dla każdego punktu
def pobierz_wartosc_rastra(layer, point):
    ident = layer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue)
    return ident.results()[1] if ident.isValid() else np.nan

wartosci_kanal1 = [pobierz_wartosc_rastra(kanal1, p) for p in punkty]
wartosci_kanal2 = [pobierz_wartosc_rastra(kanal2, p) for p in punkty]

# Obliczenie różnic między wartościami kanałów
diff = np.array(wartosci_kanal1) - np.array(wartosci_kanal2)

# Obliczenie współczynnika korelacji
wspolczynnik_korelacji = np.corrcoef(wartosci_kanal1, wartosci_kanal2)[0, 1]

# Wizualizacja wykresu rozrzutu
plt.figure(figsize=(8, 6))
plt.scatter(wartosci_kanal1, wartosci_kanal2, alpha=0.5, label="Punkty danych")
plt.plot(
    [0, max(max(wartosci_kanal1), max(wartosci_kanal2))],
    [0, max(max(wartosci_kanal1), max(wartosci_kanal2))],
    color='red', label='Linia x = y'
)
plt.xlabel("Wartości pikseli - Kanał 1")
plt.ylabel("Wartości pikseli - Kanał 2")
plt.legend()
plt.title(f"Współczynnik korelacji: {wspolczynnik_korelacji:.2f}")
plt.grid()
plt.show()

# Wyświetlenie statystyk różnic
print("Średnia różnic pikseli:", np.nanmean(diff))
print("Odchylenie standardowe różnic pikseli:", np.nanstd(diff))
