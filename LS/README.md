=== Path Cover Solver ===

Tento program rieši úlohu pokrytia vrcholov grafu pomocou najviac k ciest
(pomocou SAT solvera MiniSAT).

--- Súbory ---
pathCover.py    - hlavný spustiteľný súbor
data.py         - obsahuje preddefinované grafy
sat.py          - pomocné triedy pre prácu so SAT solverom a DIMACS formátom

--- Ako spustiť ---
1. Upravte cestu k MiniSAT solveru v súbore pathCover.py, riadok s premennou:
    SAT_SOLVER_PATH = "/cesta/k/vasmu/minisatu"
   
2. V pathCover.py pod komentarom # vstup pre find
    - nastavte graf ktory chcete na vstup

3. Spustite program:
    python3 pathCover.py

--- Požiadavky ---
- nainštalovaný MiniSAT 

--- Výstup ---
Program vypíše zoznam ciest, ktoré pokrývajú všetky vrcholy grafu.
Ak riešenie neexistuje, vypíše "Žiadne cesty".
