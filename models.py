from __future__ import (annotations,)  # to pass a City other than self to a method in the City class
import functools

import geopandas as gpd
import geopy
import itertools
import pandas as pd
import heapq


# per confrontare due citta'
@functools.total_ordering
class City(): 
    """Rappresenta una citta'. oltre all'anagrafica contiene anche elementi che ne permettono l'inserimento in un grafo"""

    def __init__(
        self,
        city: str,
        country: str,
        iso3: str,
        population: int,
        longitude: float,
        latitude: float,
        east_of_london: float,
        admin_name: str,
        index: int
    ):
        #anagrafica citta'
        self.city = city
        self.country = country
        self.iso3 = iso3
        self.population = population
        self.longitude = longitude
        self.latitude = latitude
        self.east_of_london = east_of_london
        self.admin_name = admin_name
        #nodi grafo
        self.prev = [] #prev City
        self.succ = None #lista successori
        self.index = index

    # ho dovuto def una funzione hash causa la necessita' di rendere gli oggetti comparable
    # semplicemente uso il tuple (city, codice_stato, provincia) come identificatore univoco
    def __hash__(self):
        return hash((self.city, self.iso3, self.admin_name))

    # OSS: definisco funzioni di comparazione, vengono poi usate implicitamente nel calcolo del percorso ottimo
    # per scegliere che citta' raggiungere se ho piu' scelte a pari distanza (in ore)

    # due citta' sono uguali se hanno (nome, stato, provincia) uguali
    def __eq__(self, other):
        return ((self.city, self.iso3, self.admin_name) == (other.city, other.iso3, other.admin_name))

    # una citta' e' minore dell'altra in base all'ordine alfabetico del nome
    def __lt__(self, other):
        return (self.population < other.population)


    def __repr__(self) -> str:
        return f'({self.city}, {self.iso3})'


    def hours(self, closest: list):
        """Calcola la durata del viaggio da una citta' alle piu' vicine"""
        res = dict(zip(closest, [2, 4, 8]))
        # print(res)
        for city in res:
            if city.iso3 != self.iso3:
                res[city] += 2
            if city.population > 200000:
                res[city] += 2
        res = sorted(res.items(), key=lambda item: item[1])
        return res

    
    def closest_cities_dict(self, cities_to_visit: list, dist_dict: dict) -> list:  # scelgo tra quelle a est (longitude > 0 fino a 180)
        """Restituisce un dizionario con le citta' in ordine di distanza dalla citta' corrente, ordinandole usando heapsort"""
        res = []
        for city in cities_to_visit:
            d = dist_dict[self, city]
            if d > 0 and abs(city.east_of_london - self.east_of_london < 180):
                dist = (d, city)
                heapq.heappush(res, dist)

        closest = [y for _, y in heapq.nsmallest(3, res)]
        return closest


    def get_candidates_dict(self, cities: list, dist_dict: dict) -> list:
        """calcola le 3 citta' piu' vicine (in ore), ovvero le uniche candidate per lo spostamento dalla citta' corrente"""
        cities = [city for city in cities if city.east_of_london > self.east_of_london]
        
        three_closest = self.closest_cities_dict(cities, dist_dict)
        three_closest_hours = self.hours(three_closest)

        return three_closest_hours
    

            
   

# funzioni ausiliarie

def normalize_lng(lng: float) -> float:
    """ normalize_longitude: [0, 180] U [-180, 0] -> [0, 360]
    sorta di 'traslazione' della longitudine per renderla sempre positiva, ovvero una funzione che vale 0 per londra. Di fatto
    misura 'quanto sono a est' rispetto ad essa. Faccio anche in modo di settare come 0 La posizione esatta di Londra, per semplicita'."""
    if (lng < 0):
        lng = 360 - abs(lng)
    
    return (lng + 0.1275) % 360  # -0.1275 e' la lng di londra



def dijkstra(graph: list, start, end):
    """Implementazione dell'algoritmo di Dijkstra"""
    # inizializzo il dizionario delle distanze, assegnando a ogni nodo una distanza infinita
    distances = {city: float('inf') for city in graph}
    distances[start] = 0
     
    # uso uno heap come coda di priorita'. inizializzo:
    heap = [(0, start)]
     
    # dizionario delle citta' precedenti
    prev = {}
     
    #finche' lo heap non e' vuoto
    while heap:
        current_dist, current_city = heapq.heappop(heap)
         
        # se ho gia' un percorso piu' veloce, continue
        if current_dist > distances[current_city]:
            continue
         
        # esce se ho raggiunto l'ultima tappa 
        if current_city == end:
            break
         
        # controllo delle citta' piu' vicine ed eventuale aggiornamento dei valori
        for closest, distance in current_city.succ:
            new_distance = current_dist + distance
            if new_distance < distances[closest]:
                distances[closest] = new_distance
                heapq.heappush(heap, (new_distance, closest))
                prev[closest] = current_city
     
    # ricostruisce il percorso partendo dal fondo
    path = []
    city = end
  
    while city != start:
        path.append(city)
        city = prev[city]
    path.append(start)
    # ribalta il percorso affinche' sia nell'ordine giusto
    path.reverse()

    return distances[end], path