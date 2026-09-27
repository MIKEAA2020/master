import re, os

BASE = '/home/z/my-project/github_repos/general-sustainability/arena agent 1/paper rewrites/latex'
files = [
    'paper1_assessment_separation_v62.tex',
    'paper2_obstruction_calculus_v55_Automatica_routes.tex',
    'paper3_material_ledgers_v32.tex',
    'paper4_delay_dynamics_v41.tex',
    'paper5_sampled_governance_v47_blinded_NatSustain.tex',
    'paperE1_cod_forecast_ladder_v59.tex',
    'paperE2_cod_intervention_v23.tex',
    'paperE3_edwards_forecast_ladder_v16.tex',
    'paperE4_edwards_intervention_v15.tex',
    'successor_five_layer_v1.tex',
    'minimax_dual_certificates_v11.tex',
    'paper2_computational_certification_v18.tex',
    'paper2_worked_systems_v17.tex',
    'paper2_exact_belief_computation_v10.tex',
    'paper2_probabilistic_sufficiency_v11.tex',
    'applied_regime_viability_v9.tex',
]
out = open('/home/z/my-project/scripts/gs_manuscripts_summary.txt', 'w')
for f in files:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        out.write(f'==== {f}: MISSING ====\n\n'); continue
    src = open(p, encoding='utf-8', errors='replace').read()
    src = re.sub(r'(?<!\\)%.*', '', src)
    out.write(f'==== {f} ({len(src)} chars) ====\n')
    m = re.search(r'\\title\{([^}]*)\}', src)
    if m: out.write('TITLE: ' + re.sub(r'\s+', ' ', m.group(1)) + '\n')
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', src, re.DOTALL)
    if m:
        ab = re.sub(r'\s+', ' ', m.group(1))
        ab = re.sub(r'\\[a-zA-Z]+\{([^{}]*)\}', r'\1', ab)
        out.write('ABSTRACT: ' + ab[:1800] + '\n')
    secs = re.findall(r'\\section\{([^}]*)\}', src)
    out.write('SECTIONS: ' + ' | '.join(s for s in secs[:30]) + '\n')
    # theorem labels
    labels = re.findall(r'\\label\{(thm|prop|lem|cor|theo|Theorem):?([^}]*)\}', src)
    out.write(f'THEOREM-LIKE LABELS ({len(labels)}): ' + ', '.join(f'{k}:{v}' for k, v in labels[:40]) + '\n\n')
out.close()
print('done ->', '/home/z/my-project/scripts/gs_manuscripts_summary.txt')
