def insertion_sort(arr):
    """Usado para ordenar pequenos grupos de no máximo 5 elementos."""
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr

def partition(arr, pivot):
    """Particiona o array em torno do pivô escolhido."""
    menores = []
    iguais = []
    maiores = []
    
    for elem in arr:
        if elem < pivot:
            menores.append(elem)
        elif elem > pivot:
            maiores.append(elem)
        else:
            iguais.append(elem)
    
    return menores, iguais, maiores

def mediana_das_medianas(arr, k):
    """
    Retorna o k-ésimo menor elemento de 'arr' (k é 1-indexado).
    Usa o algoritmo Mediana das Medianas para garantir tempo linear no pior caso.
    """
    if len(arr) <= 5:
        sorted_arr = insertion_sort(arr)
        return sorted_arr[k - 1]

    # Divide o array em grupos de 5
    grupos = [arr[i:i + 5] for i in range(0, len(arr), 5)]
    medianas = [insertion_sort(grupo)[len(grupo) // 2] for grupo in grupos]

    # Recursivamente encontra a mediana das medianas
    pivot = mediana_das_medianas(medianas, len(medianas) // 2 + 1)

    # Particiona o array com base no pivô
    menores, iguais, maiores = partition(arr, pivot)

    if k <= len(menores):
        return mediana_das_medianas(menores, k)
    elif k <= len(menores) + len(iguais):
        return pivot
    else:
        novo_k = k - len(menores) - len(iguais)
        return mediana_das_medianas(maiores, novo_k)
