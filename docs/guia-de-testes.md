# 🧪 Guia de Testes com Pytest - Dice Lab Py

## 📋 Índice
1. [Instalação](#instalação)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Comandos Básicos](#comandos-básicos)
4. [Tipos de Testes](#tipos-de-testes)
5. [Fixtures](#fixtures)
6. [Testes Parametrizados](#testes-parametrizados)
7. [Cobertura de Código](#cobertura-de-código)
8. [Boas Práticas](#boas-práticas)

---

## 🔧 Instalação

### 1. Instalar Pytest e Dependências

```bash
# Instalar pytest e plugins úteis
pip install pytest pytest-cov pytest-benchmark

# Ou adicione ao requirements.txt:
# pytest>=7.4.0
# pytest-cov>=4.1.0
# pytest-benchmark>=4.0.0
```

### 2. Atualizar requirements.txt

```txt
# requirements.txt
flet>=0.25.0

# Dependências de desenvolvimento (opcional)
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0
```

---

## 📂 Estrutura do Projeto

```
dice-lab-py/
│
├── dice_simulator.py          # Código principal
├── test_dice_simulator.py     # Testes
├── requirements.txt
├── pytest.ini                 # Configuração do pytest
├── .coveragerc               # Configuração de cobertura
│
└── tests/                    # Alternativa: pasta separada
    ├── __init__.py
    ├── test_probabilidades.py
    ├── test_simulacao.py
    └── test_integracao.py
```

---

## 🚀 Comandos Básicos

### Executar Todos os Testes

```bash
# Forma básica
pytest

# Com saída detalhada
pytest -v

# Com saída muito detalhada
pytest -vv
```

### Executar Testes Específicos

```bash
# Executar um arquivo específico
pytest test_dice_simulator.py

# Executar uma classe específica
pytest test_dice_simulator.py::TestCalcularProbabilidades

# Executar um teste específico
pytest test_dice_simulator.py::TestCalcularProbabilidades::test_calcular_probabilidades_2d6

# Executar testes que contêm uma palavra no nome
pytest -k "probabilidades"

# Executar testes marcados com @pytest.mark.rapido
pytest -m rapido
```

### Opções Úteis

```bash
# Parar no primeiro erro
pytest -x

# Parar após N falhas
pytest --maxfail=3

# Executar apenas testes que falharam anteriormente
pytest --lf

# Executar os que falharam primeiro, depois os demais
pytest --ff

# Modo verbose com stack trace curto
pytest -v --tb=short

# Modo silencioso (apenas sumário)
pytest -q

# Mostrar print statements
pytest -s

# Executar em paralelo (requer pytest-xdist)
pytest -n auto
```

---

## 📊 Cobertura de Código

### Gerar Relatório de Cobertura

```bash
# Relatório no terminal
pytest --cov=dice_simulator test_dice_simulator.py

# Gerar relatório HTML (abre no navegador)
pytest --cov=dice_simulator --cov-report=html test_dice_simulator.py
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html # Windows

# Relatório detalhado no terminal
pytest --cov=dice_simulator --cov-report=term-missing test_dice_simulator.py

# Múltiplos formatos
pytest --cov=dice_simulator --cov-report=html --cov-report=term test_dice_simulator.py
```

### Arquivo de Configuração .coveragerc

```ini
# .coveragerc
[run]
source = .
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## 🎯 Tipos de Testes

### 1. Testes Unitários

Testam funções individuais isoladamente:

```python
def test_calcular_probabilidades_2d6():
    """Testa uma função específica com entrada conhecida"""
    prob = calcular_probabilidades(2, 6)
    assert len(prob) == 11
    assert pytest.approx(prob[7], rel=1e-2) == 16.67
```

### 2. Testes de Integração

Testam múltiplos componentes juntos:

```python
def test_fluxo_completo_simulacao():
    """Testa o fluxo completo do aplicativo"""
    # 1. Calcular probabilidades
    prob_teoricas = calcular_probabilidades(2, 6)
    
    # 2. Simular jogadas
    resultados = simular_jogadas(2, 6, 10000)
    
    # 3. Comparar resultados
    # ... comparações ...
```

### 3. Testes de Validação

Testam tratamento de erros:

```python
def test_valores_negativos_devem_falhar():
    """Verifica que entradas inválidas geram erro"""
    with pytest.raises(ValueError):
        calcular_probabilidades(-1, 6)
```

### 4. Testes de Performance

Medem velocidade de execução:

```python
def test_calculo_rapido_2d6(benchmark):
    """Mede tempo de execução"""
    benchmark(calcular_probabilidades, 2, 6)
```

---

## 🔧 Fixtures

Fixtures são funções que fornecem dados ou configuração para os testes:

```python
@pytest.fixture
def probabilidades_2d6():
    """Dados reutilizáveis para múltiplos testes"""
    return calcular_probabilidades(2, 6)

def test_usa_fixture(probabilidades_2d6):
    """Usa a fixture como parâmetro"""
    assert len(probabilidades_2d6) == 11
```

### Fixtures com Setup/Teardown

```python
@pytest.fixture
def seed_aleatoria():
    """Define seed antes do teste, restaura depois"""
    random.seed(42)  # Setup
    yield
    random.seed()    # Teardown
```

---

## 📋 Testes Parametrizados

Execute o mesmo teste com múltiplos parâmetros:

```python
@pytest.mark.parametrize("num_dados,lados,esperado", [
    (1, 6, 6),
    (2, 6, 11),
    (3, 4, 9),
])
def test_parametrizado(num_dados, lados, esperado):
    """Executa 3 vezes com parâmetros diferentes"""
    prob = calcular_probabilidades(num_dados, lados)
    assert len(prob) == esperado
```

---

## ⚙️ Arquivo pytest.ini

Configure o comportamento do pytest:

```ini
# pytest.ini
[pytest]
# Padrão para descoberta de testes
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Marcadores customizados
markers =
    rapido: marca testes que executam rapidamente
    lento: marca testes que podem demorar
    integracao: testes de integração
    unitario: testes unitários

# Opções padrão
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov-report=term-missing

# Ignorar warnings específicos
filterwarnings =
    ignore::DeprecationWarning
```

---

## 📈 Interpretando Resultados

### Saída do Pytest

```
================================ test session starts =================================
platform darwin -- Python 3.11.0, pytest-7.4.0, pluggy-1.3.0
rootdir: /path/to/dice-lab-py
collected 25 items

test_dice_simulator.py::test_calcular_probabilidades_2d6 PASSED           [  4%]
test_dice_simulator.py::test_calcular_probabilidades_1d20 PASSED          [  8%]
test_dice_simulator.py::test_valores_negativos_devem_falhar PASSED        [ 12%]
...

============================== 25 passed in 2.34s ================================
```

### Símbolos de Status

- `.` ou `PASSED` - Teste passou ✅
- `F` ou `FAILED` - Teste falhou ❌
- `E` ou `ERROR` - Erro durante execução ⚠️
- `s` ou `SKIPPED` - Teste pulado ⏭️
- `x` ou `XFAIL` - Falha esperada 🔶
- `X` ou `XPASS` - Passou mas era esperado falhar 🔷

---

## ✅ Boas Práticas

### 1. Nomenclatura Clara

```python
# ✅ BOM - Nome descritivo
def test_calcular_probabilidades_2d6_retorna_11_valores():
    pass

# ❌ RUIM - Nome vago
def test1():
    pass
```

### 2. Um Conceito por Teste

```python
# ✅ BOM - Testa uma coisa
def test_soma_probabilidades_igual_100():
    prob = calcular_probabilidades(2, 6)
    assert sum(prob.values()) == 100.0

# ❌ RUIM - Testa várias coisas
def test_tudo():
    prob = calcular_probabilidades(2, 6)
    assert sum(prob.values()) == 100.0
    assert len(prob) == 11
    assert prob[7] == 16.67
```

### 3. Use Docstrings

```python
def test_lei_grandes_numeros():
    """
    Verifica que simulações com mais jogadas
    convergem para probabilidades teóricas.
    """
    pass
```

### 4. Organize em Classes

```python
class TestCalcularProbabilidades:
    """Agrupa testes relacionados"""
    
    def test_2d6(self):
        pass
    
    def test_1d20(self):
        pass
```

### 5. Use Aproximações para Floats

```python
# ✅ BOM - Usa pytest.approx
assert pytest.approx(prob[7], rel=1e-2) == 16.67

# ❌ RUIM - Comparação direta de floats
assert prob[7] == 16.67  # Pode falhar por precisão
```

---

## 🎓 Comandos para Memorizar

```bash
# Dia a dia
pytest -v                              # Executar todos os testes
pytest -k "nome"                       # Filtrar por nome
pytest --lf                            # Apenas os que falharam

# Cobertura
pytest --cov=. --cov-report=html       # Gerar relatório HTML

# Debug
pytest -s                              # Mostrar prints
pytest -x                              # Parar no primeiro erro
pytest --pdb                           # Abrir debugger em falhas

# Performance
pytest --durations=10                  # Mostrar 10 testes mais lentos
```

---

## 🚨 Resolução de Problemas

### Problema: Imports não funcionam

```python
# Solução 1: Adicione __init__.py na pasta tests
# Solução 2: Adicione ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Solução 3: Instale o pacote em modo desenvolvimento
pip install -e .
```

### Problema: Testes muito lentos

```python
# Use pytest-xdist para paralelização
pip install pytest-xdist
pytest -n auto  # Usa todos os cores disponíveis
```

### Problema: Testes flakey (inconsistentes)

```python
# Use seed fixa em testes aleatórios
@pytest.fixture
def seed_fixa():
    random.seed(42)
    yield
    random.seed()
```

---

## 📚 Recursos Adicionais

- [Documentação Oficial Pytest](https://docs.pytest.org/)
- [Real Python - Pytest Guide](https://realpython.com/pytest-python-testing/)
- [Pytest Patterns](https://pytest-patterns.readthedocs.io/)

---

## 🎯 Checklist de Testes

Antes de fazer commit, verifique:

- [ ] Todos os testes passam: `pytest`
- [ ] Cobertura > 80%: `pytest --cov=. --cov-report=term`
- [ ] Sem warnings: `pytest -W error`
- [ ] Código formatado: `black .` (opcional)
- [ ] Linting OK: `pylint dice_simulator.py` (opcional)

---

**💡 Dica Final**: Comece com testes simples e aumente a complexidade gradualmente. Testes são documentação viva do seu código!