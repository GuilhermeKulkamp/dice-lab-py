"""
Módulo contendo a lógica principal do simulador de dados.
Contém funções para cálculo de probabilidades e simulação de jogadas.
"""

from itertools import product
from collections import Counter
import random

def calcular_probabilidades(num_dados, lados):
    """
    Calcula todas as combinações possíveis e suas probabilidades.
    
    Args:
        num_dados: Quantidade de dados a serem jogados (inteiro > 0)
        lados: Número de lados de cada dado (inteiro > 0)
        
    Returns:
        Dicionário com somas possíveis e suas probabilidades
        
    Raises:
        ValueError: Se os parâmetros não forem inteiros positivos
    """
    # Valida os parâmetros
    if not isinstance(num_dados, int) or not isinstance(lados, int):
        raise ValueError("Quantidade de dados e número de lados devem ser números inteiros")
    
    if num_dados <= 0 or lados <= 0:
        raise ValueError("Quantidade de dados e número de lados devem ser maiores que zero")
    
    # Gera todas as combinações possíveis de resultados
    # product() cria o produto cartesiano - todas as combinações
    # Ex: 2 dados D6 = (1,1), (1,2), (1,3)... (6,6) = 36 combinações
    todas_combinacoes = list(product(range(1, lados + 1), repeat=num_dados))
    
    # Calcula a soma de cada combinação
    somas = [sum(comb) for comb in todas_combinacoes]
    
    # Conta quantas vezes cada soma aparece
    contagem = Counter(somas)
    
    # Calcula a probabilidade de cada soma
    total_combinacoes = len(todas_combinacoes)
    probabilidades = {
        soma: (count / total_combinacoes) * 100 
        for soma, count in sorted(contagem.items())
    }
    
    return probabilidades

def simular_jogadas(num_dados, lados, num_jogadas):
    """
    Simula as jogadas de dados e retorna os resultados.
    
    Args:
        num_dados: Quantidade de dados por jogada
        lados: Número de lados de cada dado
        num_jogadas: Quantidade de jogadas a simular
        
    Returns:
        Counter com a contagem de cada resultado
    """
    resultados = []
    
    # Simula cada jogada
    for _ in range(num_jogadas):
        # Joga todos os dados e soma os resultados
        jogada = sum(random.randint(1, lados) for _ in range(num_dados))
        resultados.append(jogada)
    
    # Retorna a contagem de cada resultado
    return Counter(resultados)