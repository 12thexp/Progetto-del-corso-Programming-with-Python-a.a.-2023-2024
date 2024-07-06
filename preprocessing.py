import numpy as np
import pandas as pd

# file in cui semplicemente mostro come ho importato il dataset ed estratto un sample casuale
# per questioni di costo computazionale non sono stata in grado di usare il dataset completo

df = pd.read_excel('worldcities.xlsx')

df.drop_duplicates()

# elimino colonne che non servono per leggibilita' del dataset
df = df.drop(['city_ascii', 'iso2', 'capital', 'id'], axis = 1)

# estraggo un campione casuale dal dataset originale
df = df.sample(frac=0.05)

# controllo se Londra e' presente nel sample, se no la aggiungo
if 'London, City of' not in df.values:
    df.loc[0] = ['London', 51.5072, -0.1275, 'United Kingdom', 'GBR', 'London, City of', 10979000.0] 

# scrivo su file excel. Il programma nel file project usera' questo dataset
df.to_excel("samplecities_.xlsx", index=False)

