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


## Guia de Recomendação para Tamanho de Amostra

| Cenário | Recomendação | Justificativa |
| :--- | :--- | :--- |
| **Distribuições Normais** | Amostras $n \ge 30$ | A distribuição das médias tende à normalidade (Teorema Central do Limite). |
| **Distribuições Não Normais** | Amostras $n \ge 100$ | Garante que o **Bootstrap** tenha "matéria-prima" suficiente para reamostrar as caudas. |
| **Efeitos Pequenos** | Amostras Elevadas ($n > 400$) | Efeitos sutis (d < 0.2) são facilmente mascarados pelo ruído estatístico em amostras pequenas. |

O <a href="https://github.com/rodfloripa/Significancia_estatistica_com_bootstrap/blob/main/Bootstrap.py">código</a> avisa se o número de amostras for menor que o necessário.


--- EXEMPLO DE USO COM DISTRIBUIÇÕES NÃO NORMAIS ---

Gerando dados não normais para teste

np.random.seed(42)

Grupo 1: Normal | Grupo 2: Exponencial (Não Normal)

g1 = np.random.normal(100, 15, 50)

g2 = np.random.exponential(scale=110, size=50)

Informamos à função a natureza das distribuições

resultado = bootstrap_efeito(g1, g2, normal1=True, normal2=False)





