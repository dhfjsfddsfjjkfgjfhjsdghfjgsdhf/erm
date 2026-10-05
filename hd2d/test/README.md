# HD2D Diorama — headless tests

These scripts run the game in headless Chromium with software WebGL
(SwiftShader), so they work on any machine without a GPU. They were used to
verify the plugin on the Erdenkreis project.

## Setup

1. Make a **test copy** of the game as a web build: either RPG Maker's
   *Deployment → Web browsers* output, or a copy of the project folder that has
   `index.html`, `js/`, `data/`, `img/`, `audio/`, `fonts/`, `css/` and
   `effects/`.
2. Copy `../HD2D_Diorama.js` and `ZZ_HD2DTest.js` into its `js/plugins/`
   folder and add both to `js/plugins.js`, with **ZZ_HD2DTest last**:

   ```js
   {"name":"HD2D_Diorama","status":true,"description":"","parameters":{"Debug Mode":"Always"}},
   {"name":"ZZ_HD2DTest","status":true,"description":"","parameters":{}}
   ```

   `ZZ_HD2DTest` silences audio, records errors and can start a new game
   directly on a map. Never ship it with the game.
3. Install Playwright with its Chromium build, in this folder or globally:

   ```
   npm install playwright
   npx playwright install chromium
   ```

## Running

```
WEBROOT=/path/to/test/copy QUERY="map=5&x=15&y=20&noevents=1" node run.js scenarios/commands.js
WEBROOT=/path/to/test/copy QUERY="map=5&x=15&y=20&noevents=1" node run.js scenarios/lifecycle.js
WEBROOT=/path/to/test/copy QUERY="map=5&x=15&y=20&noevents=1" node run.js scenarios/examples.js
```

The exit code is 0 when everything passed. Screenshots go to `shots/` (or the
folder given as the second argument).

| Scenario | What it checks |
|---|---|
| `commands.js` | Every plugin command with the editor's default arguments, every option of every select argument, and the effect of each command. The command list is read from the plugin header, so new commands are covered automatically. |
| `lifecycle.js` | Battle and back, save/load (preset, values, zoom and lights persist), map transfer with a preset cross-fade, an Effekseer animation drawn unlit and cleaned up. |
| `examples.js` | Renders the four example scenes from the main README (forest, town, dungeon, night). |

`QUERY` options understood by `ZZ_HD2DTest`: `map`, `x`, `y` (start
position), `noevents=1` (no autorun/parallel events, so story cutscenes do not
interfere), `webgl1=1` (force WebGL 1), `ldr=1` (pretend half-float textures are
unsupported). The scenarios use Erdenkreis maps and database entries (map 5 with
an event 6, maps 1, 3, 41 and 70, troop 1, animation 41); adjust them for
another project.

The software renderer is slow (a few frames per second), so a full run takes
several minutes. The frame rate shown by the debug overlay in these tests says
nothing about performance on real hardware.
