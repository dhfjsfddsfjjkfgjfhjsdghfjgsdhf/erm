"""People of Acts II and III who appear in more than one chapter (faces and sprites share sheet and index)."""
from story.common import Speaker, npc_speaker

MORI = npc_speaker("Mori Daisuke", "Evil", 1)
KOSAKA = npc_speaker("Kōsaka Tetsuji", "People3", 4)
RIN = npc_speaker("Asahina Rin", "Actor2", 2)      # fights in the party as a guest: masculine look (the player-character rule)
SAKI = npc_speaker("Yukimura Saki", "People2", 3)
NISHIKI = npc_speaker("Nishiki Eiji", "People3", 5)
HERALD = npc_speaker("Herold", "People3", 7)
SOMA = npc_speaker("Takamura Sōma", "Actor3", 0)
HIKARI = npc_speaker("Mizushima Hikari", "Actor1", 7)
HAYATO = npc_speaker("Asahina Hayato", "Actor1", 6)
SHIRANUI = Speaker("Shiranui", "", 0, ("$BigMonster2", 0))
GOEN = npc_speaker("Gōen", "Evil", 3)
YUKINO = npc_speaker("Tsukishiro Yukino", "Actor3", 2)  # joins the party in Act III: masculine look
ROYAL_GUARD = npc_speaker("Königliche Garde", "Actor3", 6)
WALL_SOLDIER = npc_speaker("Wallsoldat", "People3", 6)
