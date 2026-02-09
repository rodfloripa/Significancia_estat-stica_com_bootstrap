import numpy as np

def cohen_d(dados1, dados2):
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
    p_valor = np.mean(np.abs(efeitos_boot) >= np.abs(efeito_obs))
    
    return {
        'd': efeito_obs,
        'ic': ic,
        'p_valor': p_valor
    }
