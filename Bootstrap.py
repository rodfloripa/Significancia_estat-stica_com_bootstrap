import numpy as np
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower

def interpretar_estatisticamente(d):
    """Calcula métricas de probabilidade baseadas no d de Cohen."""
    d_abs = abs(d)
    superioridade = norm.cdf(d_abs / np.sqrt(2))
    sobreposicao = 2 * norm.cdf(-d_abs / 2)
    return superioridade * 100, sobreposicao * 100

def calcular_n_necessario(efeito_esperado=0.5, alpha=0.05, poder=0.80):
    """Calcula o n necessário por grupo para planejamento."""
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=efeito_esperado, 
                             alpha=alpha, 
                             power=poder, 
                             ratio=1.0, 
                             alternative='two-sided')
    return round(n)

def cohen_d(dados1, dados2):
    """Cálculo robusto do d de Cohen utilizando DP agrupado."""
    n1, n2 = len(dados1), len(dados2)
    diff = np.mean(dados1) - np.mean(dados2)
    var1 = np.var(dados1, ddof=1)
    var2 = np.var(dados2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return diff / pooled_sd

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05, exibir_relatorio=True):
    """
    Executa análise completa com Bootstrap e imprime o relatório formatado.
    """
    n1, n2 = len(dados1), len(dados2)
    efeito_obs = cohen_d(dados1, dados2)
    
    # Bootstrap para o Intervalo de Confiança (IC)
    efeitos_boot = [cohen_d(np.random.choice(dados1, n1, replace=True), 
                            np.random.choice(dados2, n2, replace=True)) for _ in range(n_boot)]
    
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
    
    # Métricas e Classificação
    d_abs = abs(efeito_obs)
    if d_abs < 0.2: cl = "desprezível"
    elif d_abs < 0.5: cl = "pequeno"
    elif d_abs < 0.8: cl = "médio"
    else: cl = "grande"

    sup, sov = interpretar_estatisticamente(efeito_obs)
    vencedor = "Grupo 1" if efeito_obs > 0 else "Grupo 2"
    perdedor = "Grupo 2" if efeito_obs > 0 else "Grupo 1"

    if exibir_relatorio:
        n_ideal = calcular_n_necessario(efeito_esperado=0.5)
        print("-" * 55)
        print(f"ANÁLISE ESTATÍSTICA (n={n1} e n={n2})")
        print("-" * 55)
        print(f"D de Cohen: {efeito_obs:.3f} ({cl.upper()})")
        print(f"IC 95%: [{ic[0]:.3f} a {ic[1]:.3f}]")
        print("-" * 55)
        print(f"INTERPRETAÇÃO PRÁTICA:")
        print(f"* Probabilidade de Superioridade: {sup:.1f}%")
        print(f"  (Chance de um indivíduo do {vencedor} ser superior ao do {perdedor})")
        print(f"* Sobreposição entre grupos: {sov:.1f}%")
        
        if n1 < n_ideal or n2 < n_ideal:
            print(f"\n⚠️ AVISO: Amostra abaixo do n sugerido ({n_ideal}) para efeitos médios.")
        print("-" * 55)

    return {
        'd': efeito_obs, 'ic': ic, 'interpretacao': cl,
        'superioridade_pct': sup, 'sobreposicao_pct': sov
    }

