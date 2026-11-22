"""Camera color-index research estimator; not a substitute for calibrated SPAD hardware."""
def indices(red: float, green: float, blue: float) -> dict:
    if min(red, green, blue) < 0 or max(red, green, blue) > 1: raise ValueError('RGB values must be normalized to 0..1')
    return {'vari': (green-red)/(green+red-blue) if green+red-blue else 0.0, 'exg': 2*green-red-blue, 'dgci': None if max(red,green,blue)==min(red,green,blue) else ((max(red,green,blue)-min(red,green,blue))/(max(red,green,blue)))}
def estimate_spad(red: float, green: float, blue: float) -> float:
    """Heuristic 0–60 display estimate requiring device/cultivar calibration."""
    return round(max(0.0, min(60.0, 60*(green-red+0.3*blue))), 1)
def classify_stress(spad: float, necrotic_percent: float) -> str:
    if necrotic_percent >= 12: return 'lesion-area alert: inspect for disease or injury'
    if spad < 26: return 'low greenness: investigate nitrogen, roots, and leaf age'
    if spad < 36: return 'moderate chlorosis: check pH and micronutrient availability'
    return 'no strong color stress signal'
