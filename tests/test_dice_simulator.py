"""
Testes unitários para o Dice Lab Py usando pytest.

Para executar os testes:
    pytest test_dice_simulator.py -v

Para executar com cobertura:
    pytest test_dice_simulator.py --cov=dice_simulator --cov-report=html

Para executar um teste específico:
    pytest test_dice_simulator.py::test_calcular_probabilidades_2d6 -v
"""

import pytest
from collections import Counter
from itertools import product
import random

# ============================================
# Importa as funções do módulo de lógica
# ============================================
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH para permitir imports relativos
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dice_logic import calcular_probabilidades, simular_jogadas


# ============================================
# FIXTURES - Dados compartilhados entre testes
# ============================================

@pytest.fixture
def probabilidades_2d6():
    """
    Fixture que retorna as probabilidades teóricas conhecidas para 2D6.
    Útil para evitar recalcular em múltiplos testes.
    """
    return calcular_probabilidades(2, 6)


@pytest.fixture
def seed_aleatoria():
    """
    Fixture que define uma seed para testes reproduzíveis.
    Garante que os testes de simulação sejam consistentes.
    """
    random.seed(42)
    yield
    random.seed()  # Restaura aleatoriedade após o teste


# ============================================
# TESTES DE PROBABILIDADES TEÓRICAS
# ============================================

class TestCalcularProbabilidades:
    """
    Testes para a função calcular_probabilidades().
    Verifica se os cálculos matemáticos estão corretos.
    """
    
    def test_calcular_probabilidades_2d6(self):
        """
        Testa o caso clássico de 2 dados de 6 lados (2D6).
        Este é o caso mais comum em jogos de tabuleiro.
        """
        prob = calcular_probabilidades(2, 6)
        
        # Verifica se todos os valores possíveis estão presentes
        assert len(prob) == 11  # Valores de 2 a 12
        assert min(prob.keys()) == 2
        assert max(prob.keys()) == 12
        
        # Verifica probabilidades específicas conhecidas
        assert pytest.approx(prob[2], rel=1e-2) == 2.78  # 1/36
        assert pytest.approx(prob[7], rel=1e-2) == 16.67  # 6/36
        assert pytest.approx(prob[12], rel=1e-2) == 2.78  # 1/36
        
        # Verifica se a soma de todas as probabilidades é 100%
        assert pytest.approx(sum(prob.values()), rel=1e-2) == 100.0
    
    def test_calcular_probabilidades_1d20(self):
        """
        Testa um único dado de 20 lados (1D20).
        Usado em sistemas de RPG como D&D.
        """
        prob = calcular_probabilidades(1, 20)
        
        # Um dado justo deve ter 20 resultados possíveis
        assert len(prob) == 20
        
        # Todos os valores devem ter a mesma probabilidade (5%)
        for valor in range(1, 21):
            assert pytest.approx(prob[valor], rel=1e-2) == 5.0
    
    def test_calcular_probabilidades_3d6(self):
        """
        Testa 3 dados de 6 lados (3D6).
        Usado em sistemas como GURPS.
        """
        prob = calcular_probabilidades(3, 6)
        
        # Valores possíveis de 3 a 18
        assert len(prob) == 16
        assert min(prob.keys()) == 3
        assert max(prob.keys()) == 18
        
        # O valor mais provável deve ser 10 ou 11 (valores centrais)
        valor_mais_provavel = max(prob, key=prob.get)
        assert valor_mais_provavel in [10, 11]
    
    def test_probabilidades_soma_100_por_cento(self):
        """
        Testa se a soma das probabilidades sempre é 100%.
        Propriedade fundamental da probabilidade.
        """
        casos_teste = [
            (1, 6),   # 1D6
            (2, 6),   # 2D6
            (3, 4),   # 3D4
            (2, 10),  # 2D10
            (4, 6),   # 4D6
        ]
        
        for num_dados, lados in casos_teste:
            prob = calcular_probabilidades(num_dados, lados)
            soma_probabilidades = sum(prob.values())
            assert pytest.approx(soma_probabilidades, rel=1e-10) == 100.0
    
    def test_valores_minimo_maximo_corretos(self):
        """
        Verifica se os valores mínimo e máximo possíveis estão corretos.
        Mínimo = num_dados × 1
        Máximo = num_dados × lados
        """
        casos_teste = [
            (2, 6, 2, 12),    # 2D6: min=2, max=12
            (3, 8, 3, 24),    # 3D8: min=3, max=24
            (1, 20, 1, 20),   # 1D20: min=1, max=20
            (4, 4, 4, 16),    # 4D4: min=4, max=16
        ]
        
        for num_dados, lados, min_esperado, max_esperado in casos_teste:
            prob = calcular_probabilidades(num_dados, lados)
            assert min(prob.keys()) == min_esperado
            assert max(prob.keys()) == max_esperado


# ============================================
# TESTES DE SIMULAÇÃO
# ============================================

class TestSimularJogadas:
    """
    Testes para a função simular_jogadas().
    Verifica se a simulação produz resultados válidos e estatisticamente corretos.
    """
    
    def test_simular_jogadas_quantidade_correta(self, seed_aleatoria):
        """
        Testa se o número de jogadas simuladas está correto.
        A soma de todas as frequências deve ser igual ao número de jogadas.
        """
        num_jogadas = 1000
        resultados = simular_jogadas(2, 6, num_jogadas)
        
        # A soma de todas as contagens deve ser igual ao número de jogadas
        total_jogadas = sum(resultados.values())
        assert total_jogadas == num_jogadas
    
    def test_simular_jogadas_valores_validos(self, seed_aleatoria):
        """
        Testa se todos os resultados estão dentro do intervalo válido.
        """
        num_dados = 2
        lados = 6
        resultados = simular_jogadas(num_dados, lados, 1000)
        
        # Todos os valores devem estar entre o mínimo e máximo possível
        valor_minimo = num_dados * 1
        valor_maximo = num_dados * lados
        
        for valor in resultados.keys():
            assert valor >= valor_minimo
            assert valor <= valor_maximo
    
    def test_simular_jogadas_distribuicao_uniforme_1d6(self, seed_aleatoria):
        """
        Testa se a distribuição de 1D6 é aproximadamente uniforme.
        Com muitas jogadas, cada valor deve aparecer ~16.67% das vezes.
        """
        num_jogadas = 60000  # Número alto para reduzir variação estatística
        resultados = simular_jogadas(1, 6, num_jogadas)
        
        # Cada valor deve aparecer aproximadamente 10.000 vezes (16.67%)
        for valor in range(1, 7):
            frequencia = resultados.get(valor, 0)
            porcentagem = (frequencia / num_jogadas) * 100
            
            # Permite uma margem de erro de ±2% (teste estatístico)
            assert pytest.approx(porcentagem, abs=2.0) == 16.67
    
    def test_simular_jogadas_lei_grandes_numeros(self):
        """
        Testa a Lei dos Grandes Números.
        Quanto mais jogadas, mais próximo das probabilidades teóricas.
        """
        num_dados = 2
        lados = 6
        
        # Calcula probabilidades teóricas
        prob_teoricas = calcular_probabilidades(num_dados, lados)
        
        # Simula com número crescente de jogadas
        jogadas_pequenas = simular_jogadas(num_dados, lados, 100)
        jogadas_grandes = simular_jogadas(num_dados, lados, 10000)
        
        # Calcula erro médio para ambas as simulações
        def calcular_erro_medio(resultados, num_jogadas):
            erros = []
            for valor, prob_teorica in prob_teoricas.items():
                freq_observada = resultados.get(valor, 0)
                prob_observada = (freq_observada / num_jogadas) * 100
                erro = abs(prob_teorica - prob_observada)
                erros.append(erro)
            return sum(erros) / len(erros)
        
        erro_pequeno = calcular_erro_medio(jogadas_pequenas, 100)
        erro_grande = calcular_erro_medio(jogadas_grandes, 10000)
        
        # O erro deve diminuir com mais jogadas
        assert erro_grande < erro_pequeno


# ============================================
# TESTES DE VALIDAÇÃO DE ENTRADA
# ============================================

class TestValidacaoEntrada:
    """
    Testes para validação de entradas inválidas.
    Garante que o sistema trata erros adequadamente.
    """
    
    def test_valores_negativos_devem_falhar(self):
        """
        Testa se valores negativos geram erro apropriado.
        """
        with pytest.raises((ValueError, AssertionError)):
            calcular_probabilidades(-1, 6)
        
        with pytest.raises((ValueError, AssertionError)):
            calcular_probabilidades(2, -6)
    
    def test_valores_zero_devem_falhar(self):
        """
        Testa se valores zero geram erro apropriado.
        """
        with pytest.raises((ValueError, ZeroDivisionError, AssertionError)):
            calcular_probabilidades(0, 6)
        
        with pytest.raises((ValueError, ZeroDivisionError, AssertionError)):
            calcular_probabilidades(2, 0)
    
    def test_tipos_invalidos_devem_falhar(self):
        """
        Testa se tipos de dados inválidos geram erro.
        """
        with pytest.raises((TypeError, ValueError)):
            calcular_probabilidades("dois", 6)
        
        with pytest.raises((TypeError, ValueError)):
            calcular_probabilidades(2, "seis")
        
        with pytest.raises((TypeError, ValueError)):
            simular_jogadas(2, 6, "mil")


# ============================================
# TESTES DE CASOS EXTREMOS (EDGE CASES)
# ============================================

class TestCasosExtremos:
    """
    Testes para casos extremos e limites do sistema.
    """
    
    def test_um_dado_um_lado(self):
        """
        Testa o caso mais simples: 1 dado com 1 lado.
        Resultado deve ser sempre 1 com 100% de probabilidade.
        """
        prob = calcular_probabilidades(1, 1)
        assert len(prob) == 1
        assert prob[1] == 100.0
    
    def test_muitos_dados_pequenos(self):
        """
        Testa com muitos dados pequenos (10D4).
        Deve formar distribuição normal.
        """
        prob = calcular_probabilidades(10, 4)
        
        # Valores possíveis de 10 a 40
        assert min(prob.keys()) == 10
        assert max(prob.keys()) == 40
        
        # O valor central deve ter maior probabilidade
        valor_central = 25  # (10 + 40) / 2
        valor_mais_provavel = max(prob, key=prob.get)
        assert abs(valor_mais_provavel - valor_central) <= 2
    
    def test_dado_grande(self):
        """
        Testa um dado com muitos lados (1D100).
        Todos devem ter 1% de probabilidade.
        """
        prob = calcular_probabilidades(1, 100)
        
        assert len(prob) == 100
        for valor in range(1, 101):
            assert pytest.approx(prob[valor], rel=1e-2) == 1.0


# ============================================
# TESTES DE PERFORMANCE
# ============================================

class TestPerformance:
    """
    Testes de performance para garantir eficiência.
    """
    
    def test_calculo_rapido_2d6(self, benchmark):
        """
        Testa a velocidade do cálculo de probabilidades para 2D6.
        Usa pytest-benchmark para medir tempo de execução.
        """
        benchmark(calcular_probabilidades, 2, 6)
    
    def test_simulacao_rapida_1000_jogadas(self, benchmark, seed_aleatoria):
        """
        Testa a velocidade da simulação de 1000 jogadas.
        """
        benchmark(simular_jogadas, 2, 6, 1000)


# ============================================
# TESTES PARAMETRIZADOS
# ============================================

@pytest.mark.parametrize("num_dados,lados,min_esperado,max_esperado", [
    (1, 6, 1, 6),
    (2, 6, 2, 12),
    (3, 4, 3, 12),
    (1, 20, 1, 20),
    (2, 10, 2, 20),
    (4, 6, 4, 24),
])
def test_parametrizado_limites(num_dados, lados, min_esperado, max_esperado):
    """
    Teste parametrizado que verifica limites para várias combinações.
    Executa o mesmo teste com diferentes parâmetros automaticamente.
    """
    prob = calcular_probabilidades(num_dados, lados)
    assert min(prob.keys()) == min_esperado
    assert max(prob.keys()) == max_esperado
    assert pytest.approx(sum(prob.values()), rel=1e-10) == 100.0


# ============================================
# TESTES DE INTEGRAÇÃO
# ============================================

class TestIntegracao:
    """
    Testes que verificam a integração entre componentes.
    """
    
    def test_fluxo_completo_simulacao(self, seed_aleatoria):
        """
        Testa o fluxo completo: calcular probabilidades → simular → comparar.
        Simula o uso real do aplicativo.
        """
        # 1. Configurar parâmetros
        num_dados = 2
        lados = 6
        num_jogadas = 10000
        
        # 2. Calcular probabilidades teóricas
        prob_teoricas = calcular_probabilidades(num_dados, lados)
        assert len(prob_teoricas) > 0
        
        # 3. Simular jogadas
        resultados = simular_jogadas(num_dados, lados, num_jogadas)
        assert sum(resultados.values()) == num_jogadas
        
        # 4. Comparar resultados (devem estar próximos)
        for valor, prob_teorica in prob_teoricas.items():
            freq_observada = resultados.get(valor, 0)
            prob_observada = (freq_observada / num_jogadas) * 100
            
            # Permite margem de erro de 3% para simulação estocástica
            assert pytest.approx(prob_observada, abs=3.0) == prob_teorica


# ============================================
# CONFIGURAÇÃO DE MARCADORES
# ============================================

# Marcadores customizados para organizar testes
# Execute com: pytest -m rapido
# ou: pytest -m lento

@pytest.mark.rapido
class TestRapidos:
    """Testes que executam rapidamente (< 1 segundo)"""
    pass

@pytest.mark.lento
class TestLentos:
    """Testes que podem demorar mais (> 1 segundo)"""
    pass


if __name__ == "__main__":
    # Permite executar diretamente: python test_dice_simulator.py
    pytest.main([__file__, "-v", "--tb=short"])