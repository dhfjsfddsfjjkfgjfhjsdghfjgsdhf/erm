"""Helpers to write RPG Maker MZ data files the way the editor does."""
import json
import copy

def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

def write_list(path, arr):
    """Top-level database arrays: one record per line (editor style)."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write('[\n' + ',\n'.join(dumps(x) for x in arr) + '\n]')

def write_map(path, m):
    """Maps: properties on one line, data on one line, events one per line."""
    head = {k: v for k, v in m.items() if k not in ('data', 'events')}
    out = '{\n' + dumps(head)[1:-1] + ',\n"data":' + dumps(m['data']) + ',\n"events":[\n'
    out += ',\n'.join(dumps(e) for e in m['events']) + '\n]\n}'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)

def write_obj(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dumps(obj))

# ---------------------------------------------------------------- event lists
class EventList:
    """Builds an event command list with correct indents."""
    def __init__(self):
        self.cmds = []
        self.indent = 0

    def add(self, code, params=None, indent=None):
        self.cmds.append({"code": code, "indent": self.indent if indent is None else indent,
                          "parameters": params if params is not None else []})
        return self

    def text(self, lines, face="", face_index=0, name="", background=0, position=2):
        if isinstance(lines, str):
            lines = lines.split('\n')
        # a message window shows 4 lines; split longer text into windows
        for i in range(0, len(lines), 4):
            self.add(101, [face, face_index, background, position, name])
            for line in lines[i:i + 4]:
                self.add(401, [line])
        return self

    def choices(self, options, branches, cancel=-2, default=0):
        """options: list of labels; branches: list of callables(EventList) (None = empty)."""
        self.add(102, [options, cancel, default, 2, 0])
        for i, label in enumerate(options):
            self.add(402, [i, label])
            self.indent += 1
            if branches[i]:
                branches[i](self)
            self.add(0, [])
            self.indent -= 1
        if cancel == -2:
            self.add(403, [6, None])
            self.indent += 1
            self.add(0, [])
            self.indent -= 1
        self.add(404, [])
        return self

    def battle(self, troop_id, can_escape=True, can_lose=True, win=None, escape=None, lose=None):
        self.add(301, [0, troop_id, can_escape, can_lose])
        if can_escape or can_lose:
            for code, body, used in ((601, win, True), (602, escape, can_escape), (603, lose, can_lose)):
                if not used:
                    continue
                self.add(code, [])
                self.indent += 1
                if body:
                    body(self)
                self.add(0, [])
                self.indent -= 1
            self.add(604, [])
        return self

    def plugin(self, plugin, command, label, args, arg_lines=None):
        self.add(357, [plugin, command, label, args])
        for line in (arg_lines or []):
            self.add(657, [line])
        return self

    def se(self, name, volume=90, pitch=100):
        return self.add(250, [{"name": name, "volume": volume, "pitch": pitch, "pan": 0}])

    def me(self, name, volume=90, pitch=100):
        return self.add(249, [{"name": name, "volume": volume, "pitch": pitch, "pan": 0}])

    def self_switch(self, ch="A", on=True):
        return self.add(123, [ch, 0 if on else 1])

    def transfer(self, map_id, x, y, direction=0, fade=0):
        return self.add(201, [0, map_id, x, y, direction, fade])

    def move_route(self, char_id, moves, wait=True, repeat=False, skippable=False):
        route = {"list": [{"code": c, "parameters": p} for c, p in moves] + [{"code": 0, "parameters": []}],
                 "repeat": repeat, "skippable": skippable, "wait": wait}
        self.add(205, [char_id, route])
        for c, p in moves:
            self.add(505, [{"code": c, "parameters": p}])
        return self

    def done(self):
        return self.cmds + [{"code": 0, "indent": 0, "parameters": []}]

# ---------------------------------------------------------------- pages/events
def conditions(self_switch=None):
    c = {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A",
         "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1,
         "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0}
    if self_switch:
        c["selfSwitchCh"] = self_switch
        c["selfSwitchValid"] = True
    return c

def page(lst=None, char="", index=0, direction=2, pattern=1, trigger=0, priority=1,
         self_switch=None, move_type=0, step_anime=False, walk_anime=True, direction_fix=False,
         through=False):
    return {
        "conditions": conditions(self_switch),
        "directionFix": direction_fix,
        "image": {"tileId": 0, "characterName": char, "direction": direction,
                  "pattern": pattern if char else 0, "characterIndex": index},
        "list": lst if lst is not None else [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": 3,
        "moveType": move_type,
        "priorityType": priority,
        "stepAnime": step_anime,
        "through": through,
        "trigger": trigger,
        "walkAnime": walk_anime,
    }

def event(eid, name, x, y, pages, note=""):
    return {"id": eid, "name": name, "note": note, "pages": pages, "x": x, "y": y}

# ---------------------------------------------------------------- plugin params
def plugin_defaults(path):
    """Reads @param names and @default values from a plugin header (English block)."""
    src = open(path, encoding='utf-8').read()
    start = src.index('/*:')
    end = src.index('*/', start)
    block = src[start:end]
    params = {}
    cur = None
    in_command = False
    for raw in block.split('\n'):
        line = raw.strip().lstrip('*').strip()
        if line.startswith('@command'):
            in_command = True
            cur = None
        elif line.startswith('@param'):
            if in_command:
                # @param after @command blocks never happens in these plugins
                pass
            cur = line[len('@param'):].strip()
            params[cur] = ""
            in_command = False
        elif line.startswith('@arg'):
            cur = None
        elif line.startswith('@default') and cur is not None and not in_command:
            params[cur] = line[len('@default'):].strip()
    desc = ''
    for raw in block.split('\n'):
        line = raw.strip().lstrip('*').strip()
        if line.startswith('@plugindesc'):
            desc = line[len('@plugindesc'):].strip()
            break
    return desc, params
