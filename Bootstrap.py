import numpy as np
from scipy.stats import norm
from statsmodels.stats.power import TTestIndPower

def interpretar_estatisticamente(valor_efeito):
    """Calcula métricas de probabilidade baseadas na magnitude do efeito."""
    abs_eff = abs(valor_efeito)
    # Probabilidade de Superioridade
    superioridade = norm.cdf(abs_eff / np.sqrt(2))
    # Sobreposição (Overlap)
    sobreposicao = 2 * norm.cdf(-abs_eff / 2)
    return superioridade * 100, sobreposicao * 100

def calcular_n_necessario(efeito_esperado=0.5, alpha=0.05, poder=0.80, e_normal=True):
    """Calcula o n necessário por grupo com ajuste para não-normalidade."""
    analysis = TTestIndPower()
    n = analysis.solve_power(effect_size=efeito_esperado, 
                             alpha=alpha, 
                             power=poder, 
                             ratio=1.0, 
                             alternative='two-sided')
    if not e_normal:
        n = n * 1.15  # Ajuste de Lehmann para distribuições não normais
    return round(n)

def cohen_d(g1, g2):
    """D de Cohen para dados contínuos."""
    n1, n2 = len(g1), len(g2)
    diff = np.mean(g1) - np.mean(g2)
    var1, var2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return diff / pooled_sd if pooled_sd != 0 else 0

def cohen_h(g1, g2):
    """H de Cohen para dados binários (proporções)."""
    p1, p2 = np.mean(g1), np.mean(g2)
    # Transformação de Arcsin para estabilizar variância
    return 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))

def bootstrap_efeito(dados1, dados2, n_boot=10000, alpha=0.05, normal1=True, normal2=True, exibir_relatorio=True):
    """Executa a análise estatística completa e integrada."""
    d1 = np.array(dados1)
    d2 = np.array(dados2)
    n1, n2 = len(d1), len(d2)
    
    # Identifica se os dados são binários (0 ou 1)
    is_binario = np.isin(d1, [0, 1]).all() and np.isin(d2, [0, 1]).all()
    
    # Seleciona métrica e calcula observado
    calc_func = cohen_h if is_binario else cohen_d
    label_metrica = "h de Cohen" if is_binario else "d de Cohen"
    efeito_obs = calc_func(d1, d2)
    
    # Bootstrap para Intervalo de Confiança
    efeitos_boot = [calc_func(np.random.choice(d1, n1, True), 
                              np.random.choice(d2, n2, True)) for _ in range(n_boot)]
    ic = np.percentile(efeitos_boot, [alpha/2*100, (1-alpha/2)*100])
    
    # Classificação e Probabilidades
    abs_eff = abs(efeito_obs)
    if abs_eff < 0.2: cl = "desprezível"
    elif abs_eff < 0.5: cl = "pequeno"
    elif abs_eff < 0.8: cl = "médio"
    else: cl = "grande"

    sup, sov = interpretar_estatisticamente(efeito_obs)
    vencedor = "Grupo 1" if efeito_obs > 0 else "Grupo 2"
    perdedor = "Grupo 2" if efeito_obs > 0 else "Grupo 1"

    if exibir_relatorio:
        # Define N ideal (para binários, n_normal costuma ser False pelo bootstrap)
        n_ideal1 = calcular_n_necessario(e_normal=normal1 if not is_binario else False)
        n_ideal2 = calcular_n_necessario(e_normal=normal2 if not is_binario else False)

        print("-" * 65)
        print(f"RELATÓRIO DE EFEITO ({'DADOS BINÁRIOS' if is_binario else 'DADOS CONTÍNUOS'})")
        print("-" * 65)
        print(f"{label_metrica}: {efeito_obs:.3f} ({cl.upper()})")
        print(f"IC {100*(1-alpha):.0f}%: [{ic[0]:.3f} a {ic[1]:.3f}]")
        print("-" * 65)
        print(f"INTERPRETAÇÃO PRÁTICA:")
        print(f"* Probabilidade de Superioridade: {sup:.1f}%")
        print(f"  (Chance de um indivíduo do {vencedor} ser superior ao do {perdedor})")
        print(f"* Sobreposição entre grupos: {sov:.1f}%")
        
        # Alertas de Amostra
        if n1 < n_ideal1:
            tipo1 = "normal" if (normal1 and not is_binario) else "Não-Normal/Binário"
            print(f"\n⚠️ AVISO: Amostra n1 ({n1}) < Ideal ({n_ideal1}) para {tipo1}.")
        if n2 < n_ideal2:
            tipo2 = "normal" if (normal2 and not is_binario) else "Não-Normal/Binário"
            print(f"\n⚠️ AVISO: Amostra n2 ({n2}) < Ideal ({n_ideal2}) para {tipo2}.")
        print("-" * 65)

    return {
        'efeito': efeito_obs, 'ic': ic, 'interpretacao': cl,
        'superioridade': sup, 'sobreposicao': sov, 'is_binario': is_binario
    }

