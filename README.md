# Programming-with-Python
PROGETTO DEL CORSO PROGRAMMING WITH PYTHON - MASTER DSFBEF<br>
Alyssa Pezzutti
----------------------------------------------

Il giro del mondo in 80 giorni
---

<i>Consideriamo il dataset che descrive alcune delle principali città del mondo. Supponiamo che sia sempre possibile viaggiare da ciascuna città alle 3 città più vicine e che tale viaggio richieda 2 ore per la città più vicina, 4 ore per la seconda città più vicina e 8 ore per la terza città più vicina. Inoltre, il viaggio dura altre 2 ore se la città di destinazione si trova in un Paese diverso da quello di partenza e altre 2 ore se la città di destinazione ha più di 200.000 abitanti.

Partendo da Londra e viaggiando sempre verso est, è possibile fare il giro del mondo tornando a Londra in 80 giorni? Quanto tempo richiede almeno?</i>

----

Il file principale del progetto e' il notebook project.ipynb. La classe usata e alcune funzioni ausiliarie si trovano in models.py, mentre preprocessing.py illustra
come ho estratto un dataset piu' piccolo da quello principale perche' il costo computazionale era altrimenti troppo elevato per il mio PC.

La soluzione e' basata sulla costruzione di un grafo i cui nodi sono oggetti di tipo City, i quali contengono l'anagrafica di una citta' (nome, provincia, stato, popolazione, latitudine e longitudine) e le informazioni che la identificano come nodo nel grafo, ovvero la lista di citta' precedenti e successive e il numero di ore necessario a raggiungerle -- il grafo e' infatti implementato tramite liste di adiacenza.

Il grafo ottenuto e' un grafo pesato, orientato e connesso. Il calcolo del percorso piu' breve in termini di tempo avviene quindi applicando l'algoritmo di Dijkstra per il calcolo del cammino minimo tra due nodi fissati.

