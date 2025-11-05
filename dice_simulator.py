import flet as ft
from itertools import product
from collections import Counter
import random
from math import comb

def main(page: ft.Page):
    """
    Função principal do aplicativo Flet.
    Define configurações da página e constrói a interface.
    """
    # Configurações da página
    page.title = "Simulador de Dados"
    page.padding = 20
    page.scroll = "adaptive"  # Permite scroll quando necessário
    
    # Variável para armazenar o gráfico atual
    chart_container = ft.Column()
    
    # Container para exibir as probabilidades
    probability_container = ft.Column(
        scroll="auto",
        height=300,
        visible=False
    )
    
    def calcular_probabilidades(num_dados, lados):
        """
        Calcula todas as combinações possíveis e suas probabilidades.
        
        Args:
            num_dados: Quantidade de dados a serem jogados
            lados: Número de lados de cada dado
            
        Returns:
            Dicionário com somas possíveis e suas probabilidades
        """
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
    
    def criar_grafico(resultados_simulacao, probabilidades_teoricas, num_jogadas):
        """
        Cria um gráfico de barras com os resultados da simulação.
        
        Args:
            resultados_simulacao: Counter com resultados da simulação
            probabilidades_teoricas: Dicionário com probabilidades teóricas
            num_jogadas: Número total de jogadas simuladas
        """
        # Limpa o container anterior
        chart_container.controls.clear()
        
        # Obtém todos os valores possíveis (união dos teóricos e simulados)
        todos_valores = sorted(set(list(probabilidades_teoricas.keys()) + 
                                  list(resultados_simulacao.keys())))
        
        # Prepara os dados para o gráfico
        # Cada barra terá a frequência simulada
        bar_groups = []
        
        for valor in todos_valores:
            count = resultados_simulacao.get(valor, 0)
            probabilidade_teorica = probabilidades_teoricas.get(valor, 0)
            
            # Calcula a frequência esperada baseada na probabilidade teórica
            frequencia_esperada = (probabilidade_teorica / 100) * num_jogadas
            
            # Cria a barra com tooltip mostrando informações detalhadas
            bar_groups.append(
                ft.BarChartGroup(
                    x=valor,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=count,
                            width=20,
                            color=ft.Colors.BLUE_400,
                            tooltip=f"Soma: {valor}\n"
                                   f"Frequência: {count}\n"
                                   f"Esperado: {frequencia_esperada:.1f}\n"
                                   f"Prob. Teórica: {probabilidade_teorica:.2f}%",
                            border_radius=5,
                        ),
                    ],
                )
            )
        
        # Encontra o valor máximo para ajustar o eixo Y
        max_y = max(resultados_simulacao.values()) if resultados_simulacao else 10
        
        # Cria o gráfico de barras
        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Frequência"),
                title_size=16,
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=40,
                title=ft.Text("Soma dos Dados"),
                title_size=16,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=max(1, max_y // 10),
                color=ft.Colors.GREY_300,
                width=1,
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.GREY_800),
            max_y=max_y * 1.1,  # Adiciona 10% de margem superior
            interactive=True,
            expand=True,
        )
        
        # Adiciona o gráfico ao container
        chart_container.controls.append(
            ft.Container(
                content=chart,
                padding=20,
                height=400,
            )
        )
        
        page.update()
    
    def mostrar_probabilidades(probabilidades):
        """
        Exibe a tabela de probabilidades teóricas.
        
        Args:
            probabilidades: Dicionário com as probabilidades de cada soma
        """
        probability_container.controls.clear()
        probability_container.visible = True
        
        # Adiciona título
        probability_container.controls.append(
            ft.Text("Probabilidades Teóricas:", size=18, weight=ft.FontWeight.BOLD)
        )
        
        # Cria uma tabela com os resultados
        rows = []
        for soma, prob in probabilidades.items():
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(soma))),
                        ft.DataCell(ft.Text(f"{prob:.4f}%")),
                        # Barra visual da probabilidade
                        ft.DataCell(
                            ft.Container(
                                content=ft.ProgressBar(
                                    value=prob / 100,
                                    color=ft.Colors.BLUE_400,
                                    bgcolor=ft.Colors.GREY_300,
                                ),
                                width=200,
                            )
                        ),
                    ]
                )
            )
        
        # Cria a tabela
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Soma", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Probabilidade", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Visual", weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
        )
        
        probability_container.controls.append(table)
        page.update()
    
    def on_simular_click(e):
        """
        Função chamada quando o botão 'Simular' é clicado.
        Valida os inputs e executa a simulação.
        """
        try:
            # Obtém e valida os valores dos inputs
            num_dados = int(input_num_dados.value)
            lados = int(input_lados.value)
            num_jogadas = int(input_num_jogadas.value)
            
            # Validações básicas
            if num_dados <= 0 or lados <= 0 or num_jogadas <= 0:
                raise ValueError("Todos os valores devem ser maiores que zero")
            
            if num_dados > 10:
                raise ValueError("Máximo de 10 dados permitido (desempenho)")
            
            if lados > 100:
                raise ValueError("Máximo de 100 lados permitido")
                
            if num_jogadas > 100000:
                raise ValueError("Máximo de 100.000 jogadas permitido")
            
            # Mostra indicador de carregamento
            progress_ring.visible = True
            btn_simular.disabled = True
            page.update()
            
            # Calcula as probabilidades teóricas
            probabilidades = calcular_probabilidades(num_dados, lados)
            mostrar_probabilidades(probabilidades)
            
            # Executa a simulação
            resultados = simular_jogadas(num_dados, lados, num_jogadas)
            
            # Cria o gráfico com os resultados
            criar_grafico(resultados, probabilidades, num_jogadas)
            
            # Esconde o indicador de carregamento
            progress_ring.visible = False
            btn_simular.disabled = False
            
            # Mostra mensagem de sucesso
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Simulação concluída com sucesso!"),
                    bgcolor=ft.Colors.GREEN_400,
                )
            )
            page.update()
            
        except ValueError as error:
            # Trata erros de validação
            progress_ring.visible = False
            btn_simular.disabled = False
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro: {str(error)}"),
                    bgcolor=ft.Colors.RED_400,
                )
            )
            page.update()
    
    # ========== CONSTRUÇÃO DA INTERFACE ==========
    
    # Campo de entrada: Quantidade de dados
    input_num_dados = ft.TextField(
        label="Quantidade de Dados",
        hint_text="Ex: 2",
        value="2",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
    )
    
    # Campo de entrada: Lados do dado
    input_lados = ft.TextField(
        label="Lados do Dado",
        hint_text="Ex: 6 (para D6)",
        value="6",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
    )
    
    # Campo de entrada: Número de jogadas
    input_num_jogadas = ft.TextField(
        label="Número de Jogadas",
        hint_text="Ex: 1000",
        value="1000",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
    )
    
    # Botão de simular
    btn_simular = ft.ElevatedButton(
        text="Simular Jogadas",
        icon=ft.Icons.PLAY_ARROW,
        on_click=on_simular_click,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_400,
        ),
    )
    
    # Indicador de carregamento
    progress_ring = ft.ProgressRing(visible=False)
    
    # Layout responsivo usando Column e Row
    # Column organiza os elementos verticalmente
    # Row organiza os elementos horizontalmente
    page.add(
        ft.Column(
            controls=[
                # Título do aplicativo
                ft.Container(
                    content=ft.Text(
                        "🎲 Simulador de Dados",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=20),
                ),
                
                # Card com os inputs
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Configurações", size=20, weight=ft.FontWeight.BOLD),
                                ft.Divider(),
                                # Usa Row para inputs em tela grande, Column em tela pequena
                                ft.ResponsiveRow(
                                    controls=[
                                        ft.Container(input_num_dados, col={"sm": 12, "md": 4}),
                                        ft.Container(input_lados, col={"sm": 12, "md": 4}),
                                        ft.Container(input_num_jogadas, col={"sm": 12, "md": 4}),
                                    ],
                                ),
                                ft.Row(
                                    controls=[btn_simular, progress_ring],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=20,
                    ),
                ),
                
                # Card com as probabilidades
                ft.Card(
                    content=ft.Container(
                        content=probability_container,
                        padding=20,
                    ),
                    visible=True,
                ),
                
                # Card com o gráfico
                ft.Card(
                    content=ft.Container(
                        content=chart_container,
                        padding=20,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll="adaptive",
        )
    )

# Inicia o aplicativo
# Para executar, use: flet run nome_do_arquivo.py
ft.app(target=main)