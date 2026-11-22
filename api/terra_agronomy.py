"""Vercel-compatible Python HTTP function exposing transparent agronomy estimates."""
import json
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from python_agronomy.penman_monteith_vpd import leaf_vpd, reference_et0, daily_light_integral

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
            temp = float(payload.get('temperature_c', 25)); rh = float(payload.get('relative_humidity', 60))
            answer = {'vpd_kpa': leaf_vpd(temp, rh, float(payload.get('leaf_offset_c', -1.5))), 'et0_mm_day': reference_et0(temp, rh, float(payload.get('wind_m_s', 2)), float(payload.get('radiation_mj_m2_day', 12)), float(payload.get('elevation_m', 0))), 'dli_mol_m2_day': daily_light_integral(float(payload.get('ppfd_umol_m2_s', 450)), float(payload.get('photoperiod_hours', 12)))}
            body = json.dumps(answer).encode(); self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            body = json.dumps({'error': str(error)}).encode(); self.send_response(400); self.send_header('Content-Type', 'application/json'); self.end_headers(); self.wfile.write(body)
