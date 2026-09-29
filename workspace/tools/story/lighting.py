"""TausiLighting data (data/Lighting.json, format v4) built from the lights placed on each MapBuild."""
from story.common import MapBuild

def ambient(color, weight=100, exposure=0, saturation=0, contrast=0, power=(255, 255, 255, 255), brightness=0):
    return {"typeName": "Data_Lighting_AmbientLight", "color": list(color), "weight": weight, "exposure": exposure,
            "saturation": saturation, "contrast": contrast, "power": list(power), "brightness": brightness}

def point(color, intensity=10, radius=300, smoothness=100, flicker=0, flicker_speed=10):
    return {"typeName": "Data_Lighting_PointLight", "color": list(color), "intensity": intensity, "radius": radius,
            "smoothness": smoothness, "flickerStrength": flicker, "flickerSpeed": flicker_speed}

def layer(url, width, height, opacity=255, scale=1, filter_mode=0, blend_mode=0):
    return {"typeName": "Data_Lighting_Layer", "width": width, "height": height, "url": url, "urlContent": None,
            "urlContentHash": None, "scale": scale, "filterMode": filter_mode, "blendMode": blend_mode,
            "shaderOverlay": 0, "opacity": opacity, "power": 100, "noise": 0, "noiseScale": 100, "noiseSpeedX": 0,
            "noiseSpeedY": 0}

# name -> light object (ids are assigned in this order)
OBJECTS = {
    "cave_dark": ambient((26, 28, 46, 255)),
    "beam": point((150, 200, 255, 255), intensity=22, radius=250, smoothness=80, flicker=4, flicker_speed=6),
    "daylight": point((255, 244, 214, 255), intensity=26, radius=420, smoothness=120),
    "crack": point((220, 230, 255, 255), intensity=12, radius=260, smoothness=140),
    "pool": point((110, 170, 255, 255), intensity=5, radius=160, smoothness=160),
    "hearth": point((255, 170, 90, 255), intensity=10, radius=280, smoothness=120, flicker=12, flicker_speed=8),
    "brazier": point((255, 150, 70, 255), intensity=14, radius=300, smoothness=120, flicker=15, flicker_speed=9),
    "torch": point((255, 160, 80, 255), intensity=10, radius=200, smoothness=110, flicker=12, flicker_speed=10),
    "ice_dark": ambient((46, 62, 104, 255)),
    "ice_glow": point((160, 220, 255, 255), intensity=8, radius=240, smoothness=150),
    "dusk_wood": ambient((150, 150, 170, 255), weight=55),
    "ash_night": ambient((96, 64, 66, 255)),
    "gate_fire": point((255, 140, 70, 255), intensity=6, radius=190, smoothness=120, flicker=14, flicker_speed=9),
    "eisfurt_ice": layer("img/pictures/Ground_Eisfurt_Ice.png", 31 * 48, 30 * 48, opacity=255),
}

def build():
    names = list(OBJECTS)
    objects = []
    for i, n in enumerate(names, start=1):
        o = dict(OBJECTS[n])
        o["id"] = i
        objects.append(o)
    maps = []
    moid = 0
    for map_id in sorted(MapBuild.registry):
        mb = MapBuild.registry[map_id]
        if not mb.lights:
            continue
        mobjs = []
        for L in mb.lights:
            moid += 1
            mobjs.append({"id": moid, "objectId": names.index(L["obj"]) + 1, "enabled": L["enabled"],
                          "x": L["x"], "y": L["y"], "referenceEventId": L["ref"]})
        maps.append({"id": map_id, "objects": mobjs, "events": []})
    return {"version": 4, "objects": objects, "maps": maps}
