import numpy as np
from statsmodels.stats.power import TTestIndPower

def calcular_n_necessario(efeito_esperado=0.5, alpha=0.05, poder=0.80):
    """
    Calcula o tamanho de amostra necessário para detectar um efeito específico.
    """
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=efeito_esperado, 
                             alpha=alpha, 
                             power=poder, 
                             ratio=1.0, 
                             alternative='two-sided')
    return round(n)

def cohen_d(dados1, dados2):
    """Calcula o d de Cohen (M1 - M2) / DP_agrupado."""
    d = (np.mean(dados1) - np.mean(dados2)) / np.sqrt((np.var(dados1, ddof=1) + np.var(dados2, ddof=1)) / 2)
    return d

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05):
    """
    Calcula o d de Cohen, Intervalo de Confiança e Classificação.
    """
    n1, n2 = len(dados1), len(dados2)
    efeito_obs = cohen_d(dados1, dados2)
    
    # Bootstrap
    efeitos_boot = []
    for _ in range(n_boot):
        boot1 = np.random.choice(dados1, n1, replace=True)
        boot2 = np.random.choice(dados2, n2, replace=True)
        efeitos_boot.append(cohen_d(boot1, boot2))
    
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
    
    # Classificação baseada no d observado
    d_abs = abs(efeito_obs)
    if d_abs < 0.2:
        interpretacao = "desprezível"
    elif d_abs < 0.5:
        interpretacao = "pequeno"
    elif d_abs < 0.8:
        interpretacao = "médio"
    else:
        interpretacao = "grande"

    return {
        'd': efeito_obs,
        'ic': ic,
        'interpretacao': interpretacao,
        'n_amostra': (n1, n2)
    }
