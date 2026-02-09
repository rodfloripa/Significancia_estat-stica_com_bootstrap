import numpy as np
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower

def interpretar_estatisticamente(d):
    """Calcula métricas de probabilidade baseadas no d de Cohen."""
    d_abs = abs(d)
    # Probabilidade de Superioridade (CL - Common Language Effect Size)
    superioridade = norm.cdf(d_abs / np.sqrt(2))
    # Sobreposição (Overlap) - Área comum entre as duas distribuições
    sobreposicao = 2 * norm.cdf(-d_abs / 2)
    return superioridade * 100, sobreposicao * 100

def calcular_n_necessario(efeito_esperado=0.5, alpha=0.05, poder=0.80):
    """Calcula o n necessário por grupo (Planejamento)."""
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=efeito_esperado,
                             alpha=alpha,
                             power=poder,
                             ratio=1.0,
                             alternative='two-sided')
    return round(n)

def cohen_d(dados1, dados2):
    """Cálculo do d de Cohen: (M1 - M2) / DP_agrupado."""
    n1, n2 = len(dados1), len(dados2)
    diff = np.mean(dados1) - np.mean(dados2)
    var1 = np.var(dados1, ddof=1)
    var2 = np.var(dados2, ddof=1)
    # Desvio padrão agrupado (pooled)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return diff / pooled_sd

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05):
    """Executa análise completa com Bootstrap e interpretações."""
    n1, n2 = len(dados1), len(dados2)
    efeito_obs = cohen_d(dados1, dados2)
   
    # Bootstrap para o Intervalo de Confiança (IC)
    efeitos_boot = []
    for _ in range(n_boot):
        boot1 = np.random.choice(dados1, n1, replace=True)
        boot2 = np.random.choice(dados2, n2, replace=True)
        efeitos_boot.append(cohen_d(boot1, boot2))
   
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
   
    # Classificação do tamanho do efeito
    d_abs = abs(efeito_obs)
    if d_abs < 0.2: cl = "desprezível"
    elif d_abs < 0.5: cl = "pequeno"
    elif d_abs < 0.8: cl = "médio"
    else: cl = "grande"

    # Probabilidades e Direção
    sup, sov = interpretar_estatisticamente(efeito_obs)
    if efeito_obs > 0:
        vencedor, perdedor = "Grupo 1", "Grupo 2"
    elif efeito_obs < 0:
        vencedor, perdedor = "Grupo 2", "Grupo 1"
    else:
        vencedor, perdedor = "Empate", "Empate"

    return {
        'd': efeito_obs,
        'ic': ic,
        'interpretacao': cl,
        'superioridade_pct': sup,
        'sobreposicao_pct': sov,
        'vencedor': vencedor,
        'perdedor': perdedor,
        'n_atual': (n1, n2)
    }


