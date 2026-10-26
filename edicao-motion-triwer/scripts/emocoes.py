"""Emoções da trilha: o vocabulário que o roteiro usa (projeto.json -> musica.trechos[].emocao) e como cada faixa da biblioteca
pontua em cada uma. Pontuação = tags do Mixkit (mood/tag/genre, ponderadas) + perfil de áudio (modo, energia, andamento).

Intensidade 1-3 (calma / média / forte) vira alvo de energia relativo à biblioteca (percentis da energia 8-30 s).
"""
EMOCOES = {
    "tensao": {
        "desc": "problema, alerta, algo errado, dor de mercado (gancho e quebra de crença)",
        "tags": {"dramatic": 2, "ominous": 2, "serious": 1.5, "restless": 1.5, "insistent": 1.2, "disturbing": 1, "scary": 0.8,
                 "aggressive": 1, "tension": 2, "suspense": 2, "thriller": 1.5, "dark": 1.5, "trailer": 0.8, "epic": 0.5},
        "modo": "menor", "bpm": (85, 135)},
    "misterio": {
        "desc": "curiosidade, segredo, 'ninguém te contou', bastidor",
        "tags": {"mysterious": 2.2, "eerie": 1.5, "atmospheric": 1.5, "hypnotic": 1.5, "mystical": 1.5, "ethereal": 1, "suspense": 1,
                 "ambient": 1},
        "modo": "menor", "bpm": (60, 125)},
    "dor": {
        "desc": "frustração, cansaço, injustiça, perda (cena da dor do público)",
        "tags": {"sad": 2, "melancholic": 2, "tragic": 2, "emotional": 1.5, "sentimental": 1.5, "reflective": 1, "piano": 0.6},
        "modo": "menor", "bpm": (60, 110)},
    "reflexao": {
        "desc": "pausa, pensar junto, explicação calma, bastidor tranquilo",
        "tags": {"reflective": 2, "mellow": 1.5, "peaceful": 1.5, "meditative": 1, "soothing": 1.5, "relaxed": 1.5, "warm": 1,
                 "contented": 1, "smooth": 1, "neutral": 0.6, "chill": 1, "lo-fi": 1},
        "modo": None, "bpm": (60, 110)},
    "confianca": {
        "desc": "autoridade, prova, firmeza, 'eu já sentei nessas reuniões'",
        "tags": {"confident": 2.2, "determined": 2, "serious": 1, "proud": 1.5, "powerful": 1, "driving": 1, "propulsive": 1,
                 "corporate": 1, "hip-hop": 0.5},
        "modo": None, "bpm": (85, 130)},
    "esperanca": {
        "desc": "virada, 'existe saída', a história começa a melhorar",
        "tags": {"hopeful": 2.5, "uplifting": 2, "warm": 1, "emotional": 1, "sentimental": 0.8, "inspiring": 2, "innocent": 0.5},
        "modo": "maior", "bpm": (75, 130)},
    "motivacao": {
        "desc": "ação, método, 'tu consegue', energia pra fazer",
        "tags": {"motivating": 2.5, "upbeat": 1.5, "driving": 1.5, "lively": 1.5, "determined": 1, "energetic": 1.5, "powerful": 1,
                 "motivational": 2, "sport": 1},
        "modo": "maior", "bpm": (95, 140)},
    "triunfo": {
        "desc": "resultado, conquista, promoção, prova forte (clímax positivo)",
        "tags": {"triumphant": 2.5, "glorious": 2, "euphoric": 2, "proud": 1.5, "powerful": 1.5, "epic": 1.5, "anthemic": 1.5},
        "modo": "maior", "bpm": (90, 140)},
    "urgencia": {
        "desc": "agora, última chance, CTA forte, ritmo de contagem",
        "tags": {"insistent": 2, "propulsive": 2, "restless": 1.5, "driving": 1.5, "aggressive": 1, "action": 1.5, "energetic": 1},
        "modo": None, "bpm": (110, 160)},
    "leveza": {
        "desc": "humor, descontração, bastidor leve, ironia",
        "tags": {"happy": 2, "fun": 2, "playful": 2, "carefree": 2, "whimsical": 1.5, "lighthearted": 2, "quirky": 1.5, "humorous": 1.5,
                 "silly": 1, "friendly": 1},
        "modo": "maior", "bpm": (85, 135)},
    "neutro": {
        "desc": "cama discreta que não puxa emoção (explicação técnica longa)",
        "tags": {"neutral": 2, "smooth": 1.5, "chill": 1, "corporate": 1.5, "lounge": 1, "minimal": 1},
        "modo": None, "bpm": (80, 125)},
}


def slugs(faixa: dict) -> set:
    return {t[1] for t in faixa.get("tags", [])} | {t[2].lower() for t in faixa.get("tags", [])}


def pontuar(faixa: dict, an: dict | None) -> dict:
    """0..1 por emoção. faixa = item do indice.json; an = item do analise.json (pode faltar)."""
    s = slugs(faixa)
    out = {}
    for k, e in EMOCOES.items():
        tags = sum(w for t, w in e["tags"].items() if t in s)
        base = min(1.0, tags / 4.0)
        if an:
            modo = "maior" if an.get("cam", "").endswith("B") else "menor"
            if e["modo"] and e["modo"] == modo:
                base += 0.08
            elif e["modo"]:
                base -= 0.08
            lo, hi = e["bpm"]
            bpm = an.get("bpm", 0)
            if bpm and not (lo <= bpm <= hi or lo <= bpm * 2 <= hi or lo <= bpm / 2 <= hi):
                base -= 0.1
        out[k] = round(max(0.0, min(1.0, base)), 3)
    return out


def alvo_energia(intensidade: int, percentis: tuple) -> float:
    """percentis = (p20, p50, p80) da energia 8-30 s da biblioteca -> alvo em dB para a intensidade 1/2/3"""
    p20, p50, p80 = percentis
    return {1: p20, 2: p50, 3: p80}.get(int(intensidade), p50)
