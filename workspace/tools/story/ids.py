"""Map ids of the story build (one place, so maps can link to each other)."""
# Prologue
CAVE, RIDGE, ROAD, TREES = 1, 2, 3, 4
# Chapter 1: Rabenau
RABENAU, INN, ELDER, HERBS, SMITHY, FARM, RABENHOLZ, DEEPWOOD, RUIN, TOWERTOP = 5, 6, 7, 8, 9, 10, 11, 12, 13, 14

# Chapter 2: Eisfurt
OSTSTRASSE, SHRINE_CAMP, EISFURT, FURT_INN, VOGTEI, KUZE_SHOP, FROSTPFAD, HOCHWEG, EISFALL, EISFALL_HEART = \
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29

# Chapter 3: Wachtburg
KOENIGSSTRASSE, WACHTBURG, GILDE, WACHTFEUER, KAJI, AUSRUESTER, KORNSPEICHER, NORDSTRASSE, WOLFSGRUBE = \
    40, 41, 42, 43, 44, 45, 46, 47, 48

# Act II: the Wall
WALLSTRASSE, FRONTPOSTEN, BRESCHE = 60, 61, 62
# Chapter 4: Die Wallfeste
WALLWEG, WALLFESTE, MARSCHALLHALLE, KASERNE, LAZARETT, ZEUGHAUS, FP5_TURM, ZISTERNE = 63, 64, 65, 66, 67, 68, 69, 70
# Chapter 5: Weißenfels
GRAUKLAMM, HEERLAGER, WF_UNTERSTADT, AQUAEDUKT, HUELLENSCHMIEDE, DRACHENHALLE = 75, 76, 77, 78, 79, 80
GRAUKLAMM_ENTRY = (30, 44)          # where the march from the Wallfeste arrives (chapter 4 transfers here)
# Chapter 6: Der Messingtyrann
TORTURM, ASCHENLAGER, WALLFESTE_SIEGE, FP3_SIEGE = 90, 91, 92, 93
# Act III, chapter 7: Die Kaiserstadt
KAISERSTRASSE, LICHTENHALL, PALAST, ARENA, MORGENDOM, KATAKOMBEN, SPINNENHALLE, GILDE_LH, GASTHAUS_LH = \
    100, 101, 102, 103, 104, 105, 106, 107, 108
# Chapter 8: Wald und Tiefe
WALDWEG, HIRSCHHEIM, FUCHSSCHREIN, URWALD, HIRSCHTHRON, EISENBERG, TIEFGRUBE, TIEFGRUBE_UNTEN, TROLLHALLE = \
    110, 111, 112, 113, 114, 115, 116, 117, 118
# Chapter 9: Morgenröte
SALZHAFEN, SCHIFF, KNOCHENRIFF, VERSUNKENE_HALLE, URWALD_BRAND, HIRSCHTHRON_NACHT = 120, 121, 122, 123, 124, 125
EPILOG_WALL, EPILOG_WEISSENFELS, EPILOG_RABENAU, EPILOG_KAMM = 126, 127, 128, 129
TAVERNE_SH = 130

NAMES = {
    CAVE: "Erwachenshöhle", RIDGE: "Kiefernkamm", ROAD: "Karrenweg", TREES: "Kiefernwald",
    RABENAU: "Rabenau", INN: "Zum Schwarzen Raben", ELDER: "Haus Okuda", HERBS: "Kräuterstube Saeki",
    SMITHY: "Schmiede Matsuda", FARM: "Hof am Feldrain", RABENHOLZ: "Rabenholz", DEEPWOOD: "Tiefes Rabenholz",
    RUIN: "Alter Wachturm", TOWERTOP: "Turmkrone",
    OSTSTRASSE: "Oststraße", SHRINE_CAMP: "Wegschrein", EISFURT: "Eisfurt", FURT_INN: "Zur Furt", VOGTEI: "Vogtei",
    KUZE_SHOP: "Handelshaus Kuze", FROSTPFAD: "Frostpfad", HOCHWEG: "Hochweg", EISFALL: "Eisfallhöhle",
    EISFALL_HEART: "Herz des Eisfalls",
    KOENIGSSTRASSE: "Königsstraße", WACHTBURG: "Wachtburg", GILDE: "Gildenhaus Wachtburg",
    WACHTFEUER: "Zum Wachtfeuer", KAJI: "Königliche Schmiede", AUSRUESTER: "Ausrüster Aoyagi",
    KORNSPEICHER: "Kornspeicher-Gewölbe", NORDSTRASSE: "Nordstraße", WOLFSGRUBE: "Wolfsgrube",
    WALLSTRASSE: "Wallstraße", FRONTPOSTEN: "Frontposten 3", BRESCHE: "Die Bresche",
    WALLWEG: "Wallweg", WALLFESTE: "Wallfeste", MARSCHALLHALLE: "Marschallhalle", KASERNE: "Kaserne",
    LAZARETT: "Lazarett", ZEUGHAUS: "Zeughaus", FP5_TURM: "Frontposten 5", ZISTERNE: "Alte Zisterne",
    GRAUKLAMM: "Grauklamm", HEERLAGER: "Heerlager", WF_UNTERSTADT: "Weißenfels", AQUAEDUKT: "Alter Aquädukt",
    HUELLENSCHMIEDE: "Hüllenschmiede", DRACHENHALLE: "Drachenhalle",
    TORTURM: "Torturm", ASCHENLAGER: "Heerlager der Asche", WALLFESTE_SIEGE: "Wallfeste (Belagerung)",
    FP3_SIEGE: "Frontposten 3 (Belagerung)",
    KAISERSTRASSE: "Kaiserstraße", LICHTENHALL: "Lichtenhall", PALAST: "Kaiserpalast", ARENA: "Kaiserarena",
    MORGENDOM: "Morgendom", KATAKOMBEN: "Unterhallen", SPINNENHALLE: "Spinnenhalle", GILDE_LH: "Gilde Lichtenhall",
    GASTHAUS_LH: "Zur Arenatreppe",
    WALDWEG: "Waldweg", HIRSCHHEIM: "Hirschheim", FUCHSSCHREIN: "Fuchsschrein", URWALD: "Urwald",
    HIRSCHTHRON: "Hirschthron", EISENBERG: "Eisenberg", TIEFGRUBE: "Tiefgrube", TIEFGRUBE_UNTEN: "Untere Tiefgrube",
    TROLLHALLE: "Trollhalle",
    SALZHAFEN: "Salzhafen", SCHIFF: "Die Seeschwalbe", KNOCHENRIFF: "Knochenriff", VERSUNKENE_HALLE: "Versunkene Halle",
    URWALD_BRAND: "Brennender Urwald", HIRSCHTHRON_NACHT: "Hirschthron (Nacht)",
    EPILOG_WALL: "Epilog: Wallfeste", EPILOG_WEISSENFELS: "Epilog: Weißenfels", EPILOG_RABENAU: "Epilog: Rabenau",
    EPILOG_KAMM: "Epilog: Kiefernkamm", TAVERNE_SH: "Der Ertrunkene Mann",
}

# Act III travel (common event "Reisen"): label, map, x, y, direction, switch that unlocks it
TRAVEL = [
    ("Lichtenhall", LICHTENHALL, 22, 3, 2, 'C7: Chapter Done'),
    ("Waldweg (Tiefenwald)", WALDWEG, 1, 20, 6, 'C7: Chapter Done'),
    ("Hirschheim", HIRSCHHEIM, 21, 36, 8, 'C8: Hirschheim'),
    ("Eisenberg", EISENBERG, 20, 30, 8, 'C8: Eisenberg'),
    ("Salzhafen", SALZHAFEN, 1, 11, 6, 'C9: Salzhafen'),
    ("Wachtburg", WACHTBURG, 24, 46, 8, 'C7: Chapter Done'),
    ("Wallfeste", WALLFESTE, 21, 32, 8, 'C7: Chapter Done'),
]
