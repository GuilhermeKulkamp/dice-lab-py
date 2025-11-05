# 🎲 Dice Lab Py

*A Python-based dice rolling simulator with probability analysis and interactive charts*

*Simulador de dados em Python com análise de probabilidades e gráficos interativos*

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Flet](https://img.shields.io/badge/flet-0.25.0%2B-purple)](https://flet.dev/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Demonstração](#demonstração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Decisões Técnicas](#decisões-técnicas)
- [Estrutura do Código](#estrutura-do-código)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuindo](#contribuindo)
- [Roadmap](#roadmap)
- [Licença](#licença)
- [Contato](#contato)

## 🎯 Sobre o Projeto

Dice Lab Py é uma ferramenta educacional e prática para simular jogadas de dados e analisar suas probabilidades. Ideal para:

- 📚 **Estudantes** aprendendo probabilidade e estatística
- 🎲 **Jogadores de RPG** querendo entender mecânicas de dados
- 🎮 **Game designers** balanceando sistemas de jogo
- 👨‍🏫 **Professores** demonstrando conceitos de probabilidade
- 🔬 **Entusiastas** de matemática e simulações

O aplicativo oferece uma interface gráfica moderna e responsiva, construída com Flet, permitindo visualizar tanto as probabilidades teóricas quanto os resultados de simulações práticas.

## ✨ Funcionalidades

- ✅ **Configuração Flexível**: Escolha quantidade de dados, número de lados (D4, D6, D8, D10, D12, D20, etc.) e número de jogadas
- 📊 **Cálculo de Probabilidades Teóricas**: Calcula e exibe todas as combinações possíveis com suas respectivas probabilidades
- 🎲 **Simulação de Jogadas**: Executa milhares de jogadas e mostra a distribuição real dos resultados
- 📈 **Gráficos Interativos**: Visualização em barras com tooltips detalhados
- 📱 **Interface Responsiva**: Adapta-se automaticamente a diferentes tamanhos de tela
- 🎨 **Design Moderno**: Interface limpa e intuitiva com Material Design
- ⚡ **Performance Otimizada**: Suporta até 100.000 jogadas com processamento rápido
- 🔢 **Comparação Teórica vs Prática**: Visualize como os resultados simulados se comparam às probabilidades teóricas

## 🖼️ Demonstração

```
┌─────────────────────────────────────┐
│     🎲 Simulador de Dados           │
├─────────────────────────────────────┤
│  Configurações:                     │
│  • Quantidade de Dados: 2           │
│  • Lados do Dado: 6 (D6)           │
│  • Número de Jogadas: 1000          │
│                                     │
│  [Simular Jogadas]                  │
├─────────────────────────────────────┤
│  Probabilidades Teóricas:           │
│  Soma │ Probabilidade │ Visual      │
│  2    │ 2.78%        │ ▓░░░░░      │
│  7    │ 16.67%       │ ▓▓▓▓▓▓▓░    │
│  12   │ 2.78%        │ ▓░░░░░      │
├─────────────────────────────────────┤
│  Resultados da Simulação:           │
│  [Gráfico de Barras Interativo]    │
└─────────────────────────────────────┘
```

## 🛠️ Tecnologias Utilizadas

- **[Python 3.8+](https://www.python.org/)**: Linguagem de programação principal
- **[Flet](https://flet.dev/)**: Framework para criar interfaces gráficas multiplataforma
- **[itertools](https://docs.python.org/3/library/itertools.html)**: Geração eficiente de combinações
- **[collections](https://docs.python.org/3/library/collections.html)**: Counter para contagem de resultados
- **[random](https://docs.python.org/3/library/random.html)**: Geração de números aleatórios para simulação

## 📥 Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/dice-lab-py.git
cd dice-lab-py
```

2. **Crie um ambiente virtual (recomendado)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o aplicativo**
```bash
python dice_simulator.py
```

### Instalação Rápida (uma linha)

```bash
git clone https://github.com/seu-usuario/dice-lab-py.git && cd dice-lab-py && pip install flet && python dice_simulator.py
```

## 🚀 Como Usar

1. **Configure os Parâmetros**:
   - **Quantidade de Dados**: Quantos dados você quer jogar simultaneamente (1-10)
   - **Lados do Dado**: Número de faces do dado (Ex: 6 para D6, 20 para D20)
   - **Número de Jogadas**: Quantas vezes simular a jogada (1-100.000)

2. **Clique em "Simular Jogadas"**

3. **Analise os Resultados**:
   - Veja a tabela de probabilidades teóricas
   - Compare com o gráfico de resultados simulados
   - Passe o mouse sobre as barras para ver detalhes

## 🧠 Decisões Técnicas

### 1. **Estrutura Geral**
- **Flet como framework**: Escolhi Flet porque permite criar interfaces modernas e responsivas com Python puro, sem necessidade de HTML/CSS/JavaScript. É ideal para aplicações científicas e educacionais.
- **Função main()**: Todo aplicativo Flet começa com uma função que recebe o objeto `page`, que representa a janela do aplicativo e gerencia o estado da interface.

### 2. **Cálculo de Probabilidades**
- **itertools.product()**: Uso essa função para gerar todas as combinações possíveis de forma eficiente e matemática. Por exemplo, 2 dados D6 geram 6² = 36 combinações possíveis: (1,1), (1,2), ... (6,6).
- **Counter**: Classe do módulo `collections` que conta automaticamente quantas vezes cada soma aparece, facilitando o cálculo de probabilidades sem loops manuais.
- **Fórmula de probabilidade**: `(ocorrências / total_combinações) * 100` para converter em percentual, seguindo a definição clássica de probabilidade.

### 3. **Simulação de Jogadas**
- **random.randint()**: Simula cada dado individualmente usando gerador de números pseudo-aleatórios do Python, que é suficientemente aleatório para aplicações educacionais.
- **Loop eficiente**: Uso list comprehension para manter o código limpo e rápido, aproveitando otimizações internas do Python.
- **Performance**: Para 100.000 jogadas com múltiplos dados, o processamento ocorre em menos de 1 segundo em hardware moderno.

### 4. **Interface Responsiva**
- **ResponsiveRow**: Componente do Flet que permite que os campos de entrada se reorganizem automaticamente em telas menores usando o sistema de grid (col={"sm": 12, "md": 4} significa 100% da largura em telas pequenas e 33% em médias).
- **Cards**: Organizam visualmente os conteúdos em seções distintas, seguindo princípios do Material Design.
- **scroll="adaptive"**: Permite rolagem automática quando o conteúdo excede o tamanho da tela, garantindo usabilidade em diferentes dispositivos.

### 5. **Gráfico de Barras**
- **BarChart do Flet**: Componente nativo que cria gráficos interativos sem dependências externas como matplotlib, reduzindo o tamanho da aplicação.
- **Tooltips informativos**: Ao passar o mouse sobre as barras, mostra informações detalhadas (valor da soma, frequência observada, frequência esperada, probabilidade teórica).
- **Cores e bordas**: Esquema de cores azul (#2196F3) para consistência visual e bordas arredondadas para aparência moderna.
- **Escala dinâmica**: O eixo Y ajusta-se automaticamente ao maior valor, com 10% de margem superior.

### 6. **Validações e Segurança**
- **Limites de segurança**: Máximo de 10 dados, 100 lados e 100.000 jogadas para evitar travamentos e consumo excessivo de memória.
- **Try-except**: Captura erros de conversão de tipos e validação, mostrando mensagens amigáveis via SnackBar.
- **Validação de inputs**: Verifica se valores são positivos e numéricos antes do processamento.

### 7. **Experiência do Usuário (UX)**
- **ProgressRing**: Indicador visual durante o processamento, importante para simulações longas.
- **SnackBar**: Mensagens de sucesso/erro não intrusivas que aparecem na parte inferior da tela.
- **Valores padrão**: Campos pré-preenchidos com exemplo comum (2D6 com 1000 jogadas) para facilitar o primeiro uso.
- **Feedback imediato**: Botão desabilitado durante processamento para evitar cliques duplos.

### 8. **Arquitetura do Código**
- **Separação de responsabilidades**: Funções específicas para cada tarefa (calcular, simular, exibir).
- **Comentários extensivos**: Docstrings em todas as funções e comentários inline para facilitar o aprendizado.
- **Nomenclatura clara**: Variáveis e funções com nomes descritivos em português/inglês.

## 📂 Estrutura do Código

```
dice-lab-py/
│
├── dice_simulator.py       # Arquivo principal do aplicativo
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── LICENSE                # Licença do projeto
├── .gitignore            # Arquivos ignorados pelo Git
│
├── docs/                 # Documentação adicional (opcional)
│   ├── screenshots/      # Capturas de tela
│   └── examples.md       # Exemplos de uso
│
└── tests/                # Testes unitários (futuro)
    └── test_simulator.py
```

### Principais Funções

```python
calcular_probabilidades(num_dados, lados)
    → Retorna dicionário com probabilidades teóricas

simular_jogadas(num_dados, lados, num_jogadas)
    → Retorna Counter com resultados da simulação

criar_grafico(resultados_simulacao, probabilidades_teoricas, num_jogadas)
    → Gera gráfico de barras interativo

mostrar_probabilidades(probabilidades)
    → Exibe tabela de probabilidades teóricas
```

## 💡 Exemplos de Uso

### Exemplo 1: Dados de RPG (2D6)
```
Quantidade de Dados: 2
Lados do Dado: 6
Número de Jogadas: 10000

Resultado: Distribuição em curva de sino, com pico em 7 (16.67%)
```

### Exemplo 2: Sistema D20
```
Quantidade de Dados: 1
Lados do Dado: 20
Número de Jogadas: 1000

Resultado: Distribuição uniforme, cada número com ~5% de chance
```

### Exemplo 3: Múltiplos Dados (Pool de Dados)
```
Quantidade de Dados: 5
Lados do Dado: 6
Número de Jogadas: 5000

Resultado: Distribuição normal, demonstrando o Teorema Central do Limite
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Este é um projeto educacional e toda ajuda é apreciada.

### Como Contribuir

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o código comentado e documentado
- Siga o estilo de código existente (PEP 8)
- Teste suas alterações antes de enviar
- Atualize a documentação se necessário

### Ideias para Contribuição

- 🌍 Tradução para outros idiomas
- 📊 Novos tipos de gráficos (pizza, linha)
- 💾 Exportar resultados para CSV/PDF
- 🎨 Temas customizáveis
- 📱 Versão mobile otimizada
- 🧪 Testes unitários

## 🗺️ Roadmap

- [x] Versão básica funcional
- [x] Interface responsiva
- [x] Gráficos interativos
- [ ] Exportar resultados para CSV
- [ ] Salvar configurações favoritas
- [ ] Modo escuro
- [ ] Comparar múltiplas simulações
- [ ] Suporte para dados customizados (D3, D7, etc.)
- [ ] Estatísticas avançadas (média, desvio padrão, variância)
- [ ] Histórico de simulações
- [ ] Testes unitários completos
- [ ] Deploy como aplicativo web (WASM)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2024 [Seu Nome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 📞 Contato

**Seu Nome** - [@seu_twitter](https://twitter.com/seu_twitter) - seu.email@exemplo.com

**Link do Projeto**: [https://github.com/seu-usuario/dice-lab-py](https://github.com/seu-usuario/dice-lab-py)

---

## 🙏 Agradecimentos

- [Flet](https://flet.dev/) - Framework excepcional para Python GUI
- [Python Software Foundation](https://www.python.org/psf/) - Pela linguagem Python
- Comunidade de RPG e game design - Pela inspiração
- Todos os contribuidores que ajudam a melhorar este projeto

---

## 📚 Recursos Adicionais

### Conceitos de Probabilidade

- **Lei dos Grandes Números**: Quanto mais jogadas, mais próximo dos valores teóricos
- **Teorema Central do Limite**: Múltiplos dados tendem a uma distribuição normal
- **Probabilidade Clássica**: P(E) = Casos Favoráveis / Casos Possíveis

### Artigos Relacionados

- [Understanding Dice Probability](https://en.wikipedia.org/wiki/Dice)
- [RPG Dice Mechanics](https://en.wikipedia.org/wiki/Dice_notation)
- [Probability Theory Basics](https://en.wikipedia.org/wiki/Probability_theory)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Feito com ❤️ e 🎲 em Python

[Reportar Bug](https://github.com/seu-usuario/dice-lab-py/issues) · [Solicitar Feature](https://github.com/seu-usuario/dice-lab-py/issues) · [Documentação](https://github.com/seu-usuario/dice-lab-py/wiki)

</div>