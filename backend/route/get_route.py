import requests
import json
import urllib.parse
import sys
import os

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

def decode_polyline(polyline_str):
    """Google polyline decoding"""
    index, lat, lng, coordinates = 0, 0, 0, []
    length = len(polyline_str)

    while index < length:
        shift, result = 0, 0
        while True:
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        dlat = ~(result >> 1) if (result & 1) else (result >> 1)
        lat += dlat

        shift, result = 0, 0
        while True:
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        dlng = ~(result >> 1) if (result & 1) else (result >> 1)
        lng += dlng

        coordinates.append({
            "lat": lat / 1e5,
            "lng": lng / 1e5
        })
    return coordinates


def get_route(start, end, output="coords.json"):
    start_enc = urllib.parse.quote(start)
    end_enc   = urllib.parse.quote(end)

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={start_enc}&destination={end_enc}&key={GOOGLE_MAPS_API_KEY}"
    )

    print("📡 Requesting route from Google Directions API...")
    res = requests.get(url)
    data = res.json()

    if data.get("status") != "OK":
        print("❌ Error:", data)
        return

    polyline = data["routes"][0]["overview_polyline"]["points"]
    coords = decode_polyline(polyline)

    with open(output, "w") as f:
        json.dump(coords, f, indent=2)

    print(f"✅ Saved {len(coords)} coordinate points to {output}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python get_route.py \"Start Address\" \"End Address\"")
        sys.exit(1)

    start = sys.argv[1]
    end = sys.argv[2]
    get_route(start, end)
