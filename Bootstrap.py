import numpy as np
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower

def interpretar_estatisticamente(d):
    d_abs = abs(d)
    superioridade = norm.cdf(d_abs / np.sqrt(2))
    sobreposicao = 2 * norm.cdf(-d_abs / 2)
    return superioridade * 100, sobreposicao * 100

def calcular_n_necessario(efeito_esperado=0.5, alpha=0.05, poder=0.80, e_normal=True):
    """
    Calcula o n necessário. Se e_normal=False, aplica correção de 15% 
    para compensar a perda de eficiência em testes não-paramétricos/bootstrap.
    """
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=efeito_esperado, 
                             alpha=alpha, 
                             power=poder, 
                             ratio=1.0, 
                             alternative='two-sided')
    
    if not e_normal:
        n = n * 1.15  # Correção de Lehmann para distribuições não normais
        
    return round(n)

def cohen_d(dados1, dados2):
    n1, n2 = len(dados1), len(dados2)
    diff = np.mean(dados1) - np.mean(dados2)
    var1 = np.var(dados1, ddof=1)
    var2 = np.var(dados2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return diff / pooled_sd

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05, normal1=True, normal2=True, exibir_relatorio=True):
    """
    Executa análise completa considerando a normalidade de cada grupo para validar o n.
    """
    n1, n2 = len(dados1), len(dados2)
    efeito_obs = cohen_d(dados1, dados2)
    
    # Bootstrap
    efeitos_boot = [cohen_d(np.random.choice(dados1, n1, replace=True), 
                            np.random.choice(dados2, n2, replace=True)) for _ in range(n_boot)]
    
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
    
    # Classificação e métricas
    d_abs = abs(efeito_obs)
    if d_abs < 0.2: cl = "desprezível"
    elif d_abs < 0.5: cl = "pequeno"
    elif d_abs < 0.8: cl = "médio"
    else: cl = "grande"

    sup, sov = interpretar_estatisticamente(efeito_obs)
    vencedor = "Grupo 1" if efeito_obs > 0 else "Grupo 2"
    perdedor = "Grupo 2" if efeito_obs > 0 else "Grupo 1"

    if exibir_relatorio:
        # Calcula n ideal específico para cada grupo baseada na sua normalidade
        n_ideal1 = calcular_n_necessario(efeito_esperado=0.5, e_normal=normal1)
        n_ideal2 = calcular_n_necessario(efeito_esperado=0.5, e_normal=normal2)

        print("-" * 60)
        print(f"ANÁLISE ESTATÍSTICA (n1={n1}, n2={n2})")
        print("-" * 60)
        print(f"D de Cohen(tam. do efeito): {efeito_obs:.3f} ({cl.upper()})")
        print(f"IC 95%: [{ic[0]:.3f} a {ic[1]:.3f}]")
        print("-" * 60)
        print(f"INTERPRETAÇÃO PRÁTICA:")
        print(f"* Probabilidade de Superioridade: {sup:.1f}%")
        print(f"  (Chance de um indivíduo do {vencedor} ser superior ao do {perdedor})")
        print(f"* Sobreposição entre grupos: {sov:.1f}%")
        
        # Alertas personalizados por grupo e tipo de distribuição
        if n1 < n_ideal1:
            tipo1 = "normal" if normal1 else "NÃO normal"
            print(f"\n⚠️ AVISO: Amostra n1 ({n1}) abaixo do n sugerido ({n_ideal1}) para dist. {tipo1}.")
        
        if n2 < n_ideal2:
            tipo2 = "normal" if normal2 else "NÃO normal"
            print(f"\n⚠️ AVISO: Amostra n2 ({n2}) abaixo do n sugerido ({n_ideal2}) para dist. {tipo2}.")
        print("-" * 60)

    return {
        'd': efeito_obs, 'ic': ic, 'interpretacao': cl,
        'superioridade_pct': sup, 'sobreposicao_pct': sov
    }
