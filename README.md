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
