# -*- coding: utf-8 -*-
# 一次性脚本：把 data.py 里现有的 9 本书导入 Supabase 的 products 表
# 用法： python3 seed_products.py

import json
import os
import urllib.request

from data import PRODUCTS

SITE_BASE = "https://www.monpremierlivre.com"


def load_env():
    env = {}
    with open(os.path.join(os.path.dirname(__file__), ".env"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def main():
    env = load_env()
    url = env["SUPABASE_URL"] + "/rest/v1/products"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]

    rows = []
    for p in PRODUCTS:
        rows.append({
            "slug": p["slug"],
            "name": p["name"],
            "name_en": p["name_en"],
            "price": p["price"],
            "age": p.get("age"),
            "age_en": p.get("age_en"),
            "short": p.get("short"),
            "short_en": p.get("short_en"),
            "long_desc": p.get("long"),
            "long_desc_en": p.get("long_en"),
            "care": p.get("care"),
            "care_en": p.get("care_en"),
            "tags": p.get("tags", []),
            "image_url": f"{SITE_BASE}/{p['image']}" if p.get("image") else None,
            "published": True,
        })

    body = json.dumps(rows).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=representation",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"OK - {len(result)} produits importés/mis à jour.")
    except urllib.error.HTTPError as e:
        print("ERREUR", e.code, e.read().decode("utf-8"))


if __name__ == "__main__":
    main()
