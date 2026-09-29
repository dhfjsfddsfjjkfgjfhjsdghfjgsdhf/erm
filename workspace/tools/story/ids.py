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
}
