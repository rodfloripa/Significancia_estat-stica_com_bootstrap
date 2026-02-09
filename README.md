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

Exemplo de uso:
Definindo a semente para reprodutibilidade
np.random.seed(42)

1. Criando distribuições NÃO NORMAIS (Exponenciais)

Grupo A: Tempo de resposta médio de 200ms

dados_a = np.random.exponential(scale=200, size=100)

Grupo B: Tempo de resposta médio de 350ms (um sistema mais lento)

dados_b = np.random.exponential(scale=350, size=100)

res = bootstrap_efeito(dados_a, dados_b)

print(f"D de Cohen: {res['d']:.2f} ({res['interpretacao']})")
