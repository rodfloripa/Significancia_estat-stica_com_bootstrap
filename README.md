# Significância estatística com Bootstrap

<p align="justify">
O artigo <a href="https://sites.stat.columbia.edu/gelman/research/published/signif4.pdf">"_The difference between “significant” and “not significant” is not itself statistically significant_"</a> de Andrew Gelman e Hal Stern é um clássico!
</p>

<p align="justify">
O ponto principal é que:
</p>
<p align="justify">  
- A diferença entre um resultado "significativo" (p < 0.05) e "não significativo" (p >= 0.05) *não é* necessariamente significativa.
</p>
<p align="justify">  
- Comparações de p-valores entre estudos/grupos devem ser feitas com cuidado.O melhor é observar o tamanho do efeito e seu nível de confiança
</p>

<p align="justify">
O artigo destaca problemas em interpretar p-valores como fronteiras rígidas (0.05) e a importância de considerar incertezas e contextos.
</p>
<p align="justify">
Podemos calcular a significância estatistica com Bootstrap em qualquer distribuição,resultando no d de Cohen e Intervalo de Confiança,com
uma estimativa confiável da significância estatística.
</p>
<br><br>

Situação,Recomendação
Distribuições Normais,Amostras a partir de 30 unidades costumam ser suficientes.
Distribuições Não Normais,Exigem amostras maiores (n=100 ou mais) para que o Bootstrap seja estável.
Efeitos Pequenos,Exigem amostras muito maiores para serem detectados com precisão.

## Guia de Recomendação para Tamanho de Amostra

| Cenário | Recomendação | Justificativa |
| :--- | :--- | :--- |
| **Distribuições Normais** | Amostras $n \ge 30$ | A distribuição das médias tende à normalidade (Teorema Central do Limite). |
| **Distribuições Não Normais** | Amostras $n \ge 100$ | Garante que o **Bootstrap** tenha "matéria-prima" suficiente para reamostrar as caudas. |
| **Efeitos Pequenos** | Amostras Elevadas ($n > 400$) | Efeitos sutis (d < 0.2) são facilmente mascarados pelo ruído estatístico em amostras pequenas. |

--- EXEMPLO DE USO COM DISTRIBUIÇÕES NÃO NORMAIS ---
if __name__ == "__main__":
    np.random.seed(42)
   
Criando dados não normais (Exponenciais)
Grupo 1: Média ~200 | Grupo 2: Média ~300
g1 = np.random.exponential(scale=200, size=120)
g2 = np.random.exponential(scale=300, size=120)

1. Planejamento (Opcional): Se eu quisesse detectar um efeito Médio (0.5)
n_ideal = calcular_n_necessario(efeito_esperado=0.5)

2. Execução da Análise
res = bootstrap_efeito(g1, g2)

3. Print dos Resultados
print("-" * 50)
print(f"ANÁLISE ESTATÍSTICA (n={res['n_atual'][0]} por grupo)")
print("-" * 50)
print(f"D de Cohen: {res['d']:.3f} ({res['interpretacao'].upper()})")
print(f"IC 95%: [{res['ic'][0]:.3f} a {res['ic'][1]:.3f}]")
print("-" * 50)
print(f"INTERPRETAÇÃO PRÁTICA:")
print(f"* Probabilidade de Superioridade: {res['superioridade_pct']:.1f}%")
print(f"  (Chance de um indivíduo do {res['vencedor']} ser superior ao do {res['perdedor']})")
print(f"* Sobreposição entre grupos: {res['sobreposicao_pct']:.1f}%")

if res['n_atual'][0] < n_ideal:
    print(f"\n⚠️ AVISO: Amostra atual ({res['n_atual'][0]}) abaixo do n sugerido ({n_ideal}) para efeitos médios.")
print("-" * 50)


res = bootstrap_efeito(dados_a, dados_b)

print(f"D de Cohen: {res['d']:.2f} ({res['interpretacao']})")
