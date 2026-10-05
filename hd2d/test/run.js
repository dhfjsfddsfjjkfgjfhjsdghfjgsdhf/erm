// Headless test runner for HD2D_Diorama.
// Serves a web build of the game, opens it in headless Chromium (software
// WebGL through SwiftShader) and runs one scenario file against it.
//
//   WEBROOT=/path/to/web/build node run.js scenarios/commands.js [screenshot dir]
//
// Environment:
//   WEBROOT  folder with index.html, js/, data/, img/ ... (required)
//   QUERY    URL query for the helper plugin, e.g. "map=5&x=15&y=20&noevents=1"
//   PORT     HTTP port (default 8131)
// Exit code 1 when the scenario throws or the game reports an error.
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

if (!process.env.WEBROOT) {
    console.error("Set WEBROOT to the game's web build folder.");
    process.exit(2);
}
const ROOT = path.resolve(process.env.WEBROOT);
const scenarioPath = path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3] || path.join(__dirname, "shots"));
fs.mkdirSync(OUT, { recursive: true });

const MIME = {
    ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".png": "image/png",
    ".css": "text/css", ".woff": "font/woff", ".ttf": "font/ttf", ".wasm": "application/wasm",
    ".ogg": "audio/ogg", ".m4a": "audio/mp4", ".efkefc": "application/octet-stream"
};

const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split("?")[0]);
    const file = path.join(ROOT, url === "/" ? "index.html" : url);
    if (!file.startsWith(ROOT)) {
        res.writeHead(403);
        res.end();
        return;
    }
    fs.readFile(file, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end("not found");
            // Missing normal maps are expected when auto-detection is on.
            if (!/favicon|_normal\.png/.test(url)) console.log("[404]", url);
            return;
        }
        res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
        res.end(data);
    });
});

(async () => {
    const PORT = Number(process.env.PORT || 8131);
    await new Promise(resolve => server.listen(PORT, resolve));
    const browser = await chromium.launch({
        args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required", "--ignore-gpu-blocklist"]
    });
    const page = await browser.newPage({ viewport: { width: 816, height: 624 } });
    const logs = [];
    page.on("console", m => logs.push("[" + m.type() + "] " + m.text()));
    page.on("pageerror", e => logs.push("[pageerror] " + e.message + "\n" + e.stack));
    const query = process.env.QUERY ? "?" + process.env.QUERY : "";
    await page.goto("http://localhost:" + PORT + "/index.html" + query);

    // Helpers passed to every scenario.
    const h = {
        page, out: OUT, logs,
        sleep: ms => new Promise(r => setTimeout(r, ms)),
        eval: (fn, arg) => page.evaluate(fn, arg),
        async until(fn, timeout = 30000, arg) {
            const t0 = Date.now();
            while (Date.now() - t0 < timeout) {
                try {
                    if (await page.evaluate(fn, arg)) return true;
                } catch (e) {
                    // not ready yet
                }
                await new Promise(r => setTimeout(r, 100));
            }
            throw new Error("timeout waiting for " + fn.toString().slice(0, 160));
        },
        /** Waits until the game has rendered n more frames. */
        async frames(n) {
            const f0 = await page.evaluate(() => Graphics.frameCount);
            await h.until(t => Graphics.frameCount >= t, 120000, f0 + n);
        },
        async shot(name) {
            const file = path.join(OUT, name + ".png");
            await page.screenshot({ path: file });
            console.log("shot", file);
            return file;
        },
        async mapReady() {
            await h.until(() => SceneManager._scene && SceneManager._scene.constructor === Scene_Map && SceneManager._scene.isStarted() &&
                !$gamePlayer.isTransferring() && SceneManager._scene._fadeDuration === 0, 90000);
        }
    };

    let failed = false;
    try {
        await h.until(() => window.SceneManager && SceneManager._scene && /Scene_(Title|Map)/.test(SceneManager._scene.constructor.name), 120000);
        await require(scenarioPath)(h);
    } catch (e) {
        failed = true;
        console.log("SCENARIO ERROR:", e.stack || e);
        try {
            await h.shot("error_state");
        } catch (e2) {
            // ignore
        }
    }
    const errors = await page.evaluate(() => window.__errors || []).catch(() => []);
    if (errors.length) {
        failed = true;
        console.log("GAME ERRORS:\n" + errors.join("\n---\n"));
    }
    const noise = /DevTools|GL Driver Message|CanvasTextAlign|willReadFrequently|software WebGL|GPU stall|swiftshader|Failed to load resource/i;
    const interesting = logs.filter(l => !noise.test(l));
    if (interesting.length) console.log("CONSOLE:\n" + interesting.slice(0, 120).join("\n"));
    await browser.close();
    server.close();
    process.exit(failed ? 1 : 0);
})();
