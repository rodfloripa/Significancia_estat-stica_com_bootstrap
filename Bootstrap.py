import numpy as np

def cohen_d(dados1, dados2):
    # Cálculo do d de Cohen: (M1 - M2) / DP_agrupado
    d = (np.mean(dados1) - np.mean(dados2)) / np.sqrt((np.var(dados1, ddof=1) + np.var(dados2, ddof=1)) / 2)
    return d

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05):
    efeito_obs = cohen_d(dados1, dados2)
    
    efeitos_boot = []
    for _ in range(n_boot):
        boot1 = np.random.choice(dados1, len(dados1), replace=True)
        boot2 = np.random.choice(dados2, len(dados2), replace=True)
        efeitos_boot.append(cohen_d(boot1, boot2))
    
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
    
    # Classificação do tamanho do efeito (Critérios de Cohen)
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
        'interpretacao': interpretacao
    }


