# algoritmos_dc/par_de_pontos_mais_proximos.py
import math

def dist(p1, p2):
    # p1 e p2 são tuplas (x, y, nome)
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def encontrar_par_mais_proximo(pontos):
    if len(pontos) < 2:
        return float('inf'), (None, None)
        
    distancia_minima = float('inf')
    par_mais_proximo = (None, None)
    
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            d = dist(pontos[i], pontos[j])
            if d < distancia_minima:
                distancia_minima = d
                par_mais_proximo = (pontos[i], pontos[j])
                
    return distancia_minima, par_mais_proximo