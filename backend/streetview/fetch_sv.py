import json
import os
import math
import argparse
import requests

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")


def compute_heading(lat1, lng1, lat2, lng2):
    """두 지점의 방향(heading) 계산"""
    d_lng = math.radians(lng2 - lng1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    y = math.sin(d_lng) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lng)
    brng = math.degrees(math.atan2(y, x))
    return (brng + 360) % 360


def fetch_streetview(coords_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with open(coords_file) as f:
        coords = json.load(f)

    print(f"📥 Loaded {len(coords)} coordinates")

    for i, (c1, c2) in enumerate(zip(coords, coords[1:])):
        lat, lng = c1["lat"], c1["lng"]
        next_lat, next_lng = c2["lat"], c2["lng"]
        heading = compute_heading(lat, lng, next_lat, next_lng)

        url = (
            "https://maps.googleapis.com/maps/api/streetview"
            f"?size=640x640&location={lat},{lng}&heading={heading}"
            f"&pitch=0&fov=90&key={GOOGLE_MAPS_API_KEY}"
        )

        path = f"{output_folder}/frame_{i:04d}.jpg"

        img = requests.get(url).content
        with open(path, "wb") as f:
            f.write(img)

        print(f"📸 Saved {path}")

    print("🎉 StreetView download complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    fetch_streetview(args.input, args.output)
