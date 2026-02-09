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

Gerando dados não normais para teste

np.random.seed(42)

g1 = np.random.lognormal(mean=2, sigma=0.5, size=150)

g2 = np.random.lognormal(mean=2.3, sigma=0.5, size=150)

resultado = bootstrap_efeito(g1, g2)

print(f"\n⚠️ AVISO: Amostra atual ({res['n_atual'][0]}) abaixo do n sugerido ({n_ideal}) para efeitos médios.")

print("-" * 50)



