"""FAO-56 reference ET and Tetens leaf-to-air VPD helpers. SI units throughout."""
from math import exp

def saturation_vapor_pressure(temp_c: float) -> float:
    return 0.6108 * exp(17.27 * temp_c / (temp_c + 237.3))

def leaf_vpd(temp_c: float, relative_humidity: float, leaf_offset_c: float = -1.5) -> float:
    if not 0 <= relative_humidity <= 100: raise ValueError('relative_humidity must be 0..100')
    return max(0.0, saturation_vapor_pressure(temp_c + leaf_offset_c) - saturation_vapor_pressure(temp_c) * relative_humidity / 100)

def reference_et0(temp_c: float, relative_humidity: float, wind_m_s: float = 2.0, net_radiation_mj_m2_day: float = 12.0, elevation_m: float = 0.0) -> float:
    """Daily FAO-56 Penman-Monteith reference crop ET₀ (mm/day)."""
    es = saturation_vapor_pressure(temp_c); ea = es * relative_humidity / 100
    delta = 4098 * es / (temp_c + 237.3) ** 2
    pressure = 101.3 * ((293 - 0.0065 * elevation_m) / 293) ** 5.26
    gamma = 0.000665 * pressure
    result = (0.408 * delta * net_radiation_mj_m2_day + gamma * 900 / (temp_c + 273) * wind_m_s * (es - ea)) / (delta + gamma * (1 + 0.34 * wind_m_s))
    return max(0.0, result)

def daily_light_integral(ppfd_umol_m2_s: float, photoperiod_hours: float) -> float:
    return ppfd_umol_m2_s * photoperiod_hours * 3600 / 1_000_000
