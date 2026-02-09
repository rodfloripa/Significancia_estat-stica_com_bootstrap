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

--- EXEMPLO DE FLUXO DE TRABALHO ---

1. Planejamento: Quero detectar um efeito médio (0.5). Quanto preciso coletar?

n_alvo = calcular_n_necessario(efeito_esperado=0.5)

print(f"🎯 Meta: Para um efeito médio, precisamos de n={n_alvo} por grupo.\n")

2. Execução: Simulando dados (abaixo do n_alvo para ver o efeito no IC)

np.random.seed(42)

grupo_a = np.random.gamma(shape=2, scale=2, size=40) # Distribuição não normal

grupo_b = np.random.gamma(shape=2.5, scale=2, size=40)

3. Análise

res = bootstrap_efeito(grupo_a, grupo_b)

print(f"📊 Resultado Observado: {res['d']:.2f} ({res['interpretacao']})")

print(f"⚖️ Intervalo de Confiança (Bootstrap): [{res['ic'][0]:.2f}, {res['ic'][1]:.2f}]")

if res['n_amostra'][0] < n_alvo:
    
   print(f"⚠️ Nota: Sua amostra atual ({res['n_amostra'][0]}) é menor que o n ideal ({n_alvo}).")


res = bootstrap_efeito(dados_a, dados_b)

print(f"D de Cohen: {res['d']:.2f} ({res['interpretacao']})")
