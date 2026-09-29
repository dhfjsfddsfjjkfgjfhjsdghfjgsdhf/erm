// Runs the web copy of the game in headless Chromium and executes a scenario.
// usage: node tools/run_game.js <scenario.js> [outdir]
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = process.env.WEBROOT || "/home/claude/mz/web";
const scenarioPath = path.resolve(process.argv[2]);
const OUT = process.argv[3] || "/tmp/claude-0/-home-claude/e205e0a3-bd62-5461-b21e-25640739d4b9/scratchpad/shots";
fs.mkdirSync(OUT, { recursive: true });

const MIME = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".png": "image/png",
    ".css": "text/css", ".woff": "font/woff", ".wasm": "application/wasm", ".ogg": "audio/ogg" };

const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split("?")[0]);
    const file = path.join(ROOT, url === "/" ? "index.html" : url);
    fs.readFile(file, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end("not found");
            if (!url.endsWith("favicon.ico")) console.log("[404]", url);
            return;
        }
        res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
        res.end(data);
    });
});

(async () => {
    const PORT = Number(process.env.PORT || 8123);
    await new Promise(r => server.listen(PORT, r));
    const browser = await chromium.launch({
        args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"]
    });
    const page = await browser.newPage({ viewport: { width: 816, height: 624 } });
    const logs = [];
    page.on("console", m => logs.push("[" + m.type() + "] " + m.text()));
    page.on("pageerror", e => logs.push("[pageerror] " + e.message + "\n" + e.stack));
    await page.goto("http://localhost:" + PORT + "/index.html");

    const h = {
        page,
        out: OUT,
        logs,
        sleep: ms => new Promise(r => setTimeout(r, ms)),
        eval: (fn, arg) => page.evaluate(fn, arg),
        async until(fn, timeout = 20000, arg) {
            const t0 = Date.now();
            while (Date.now() - t0 < timeout) {
                try {
                    if (await page.evaluate(fn, arg)) return true;
                } catch (e) { /* not ready */ }
                await new Promise(r => setTimeout(r, 100));
            }
            throw new Error("timeout waiting for " + fn.toString().slice(0, 120));
        },
        async frames(n) {
            const f0 = await page.evaluate(() => Graphics.frameCount);
            await h.until(t => Graphics.frameCount >= t, 30000, f0 + n);
        },
        async shot(name) {
            const file = path.join(OUT, name + ".png");
            await page.screenshot({ path: file });
            console.log("shot", file);
            return file;
        },
        async key(k, times = 1, delay = 120) {
            for (let i = 0; i < times; i++) {
                await page.keyboard.down(k);
                await h.sleep(60);
                await page.keyboard.up(k);
                await h.sleep(delay);
            }
        },
        // step the game logic n frames synchronously (no rendering)
        async run(n) {
            return page.evaluate(n => {
                for (let i = 0; i < n; i++) {
                    SceneManager.updateMain();
                    if (window.__errors.length) break;
                }
                return Graphics.frameCount;
            }, n);
        },
        async runUntil(fn, maxFrames = 20000, arg) {
            for (let done = 0; done < maxFrames; done += 200) {
                if (await page.evaluate(fn, arg)) return true;
                await h.run(200);
                const errs = await page.evaluate(() => window.__errors.length);
                if (errs) throw new Error("game error while running");
            }
            throw new Error("runUntil gave up: " + fn.toString().slice(0, 120));
        },
        async errors() {
            return page.evaluate(() => window.__errors || []);
        }
    };

    let failed = false;
    try {
        await h.until(() => window.SceneManager && SceneManager._scene && SceneManager._scene.constructor.name === "Scene_Title", 60000);
        const scenario = require(scenarioPath);
        await scenario(h);
    } catch (e) {
        failed = true;
        console.log("SCENARIO ERROR:", e.stack || e);
        try { await h.shot("error_state"); } catch (e2) { /* ignore */ }
    }
    const errs = await page.evaluate(() => window.__errors || []).catch(() => []);
    if (errs.length) {
        failed = true;
        console.log("GAME ERRORS:\n" + errs.join("\n---\n"));
    }
    const interesting = logs.filter(l => !/Download the React DevTools|GL Driver Message|WebGL|CanvasTextAlign|willReadFrequently/.test(l));
    if (interesting.length) console.log("CONSOLE:\n" + interesting.slice(0, 80).join("\n"));
    await browser.close();
    server.close();
    process.exit(failed ? 1 : 0);
})();
