// Fires every plugin command of HD2D_Diorama:
//   1. each command with the arguments the editor inserts by default,
//   2. every option of every select argument,
//   3. semantic checks of what the commands change.
// Fails on any error, unexpected warning, render failure or failed check.
// Expects a map with an event 6 (Erdenkreis: QUERY="map=5&x=15&y=20&noevents=1").
const fs = require("fs");
const path = require("path");

/** Reads every @command with its @arg defaults and select options from the plugin header. */
const readCommands = file => {
    const src = fs.readFileSync(file, "utf8");
    const lines = src.slice(0, src.indexOf("*/") + 2).split("\n").map(l => l.replace(/^\s*\*\s?/, "").trim());
    const cmds = {};
    let cmd = null;
    let arg = null;
    for (const l of lines) {
        let m;
        if ((m = l.match(/^@command\s+(\S+)/))) {
            cmd = m[1];
            cmds[cmd] = { args: {}, options: {} };
            arg = null;
        } else if (/^@param\s+/.test(l)) {
            cmd = null;
            arg = null;
        } else if (cmd && (m = l.match(/^@arg\s+(\S+)/))) {
            arg = m[1];
            cmds[cmd].args[arg] = "";
            cmds[cmd].options[arg] = [];
        } else if (cmd && arg) {
            const opts = cmds[cmd].options[arg];
            if ((m = l.match(/^@default\s?(.*)$/))) cmds[cmd].args[arg] = m[1];
            else if ((m = l.match(/^@option\s+(.*)$/))) opts.push(m[1]);
            else if ((m = l.match(/^@value\s?(.*)$/))) opts[opts.length - 1] = { label: opts[opts.length - 1], value: m[1] };
        }
    }
    return cmds;
};

const EXPECTED_WARNINGS = [/Unknown preset 'Nope'/, /Unknown setting 'blom\.intensity'/];

module.exports = async h => {
    const CMDS = readCommands(process.env.PLUGIN || path.join(__dirname, "..", "..", "HD2D_Diorama.js"));
    console.log("commands:", Object.keys(CMDS).length);
    await h.mapReady();
    await h.eval(() => {
        window.__hd2dMsgs = [];
        const error = console.error;
        const warn = console.warn;
        console.error = function(...a) {
            window.__hd2dMsgs.push("E " + a.map(x => (x && x.stack) || String(x)).join(" "));
            error.apply(console, a);
        };
        console.warn = function(...a) {
            window.__hd2dMsgs.push("W " + a.map(String).join(" "));
            warn.apply(console, a);
        };
        window.__call = (name, args, eventId = 6) => {
            const it = new Game_Interpreter();
            it.setup([{ code: 0, indent: 0, parameters: [] }], eventId);
            PluginManager.callCommand(it, "HD2D_Diorama", name, args);
            return it;
        };
    });
    const problems = [];
    const status = async label => {
        const r = await h.eval(() => {
            const p = SceneManager._scene._spriteset._hd2dPipeline;
            const out = { failed: !p || p.failed, err: HD2D.lastError ? String(HD2D.lastError) : null, msgs: window.__hd2dMsgs.splice(0) };
            HD2D.lastError = null;
            return out;
        });
        const msgs = r.msgs.filter(m => !EXPECTED_WARNINGS.some(re => re.test(m)));
        if (r.failed || r.err || msgs.length) problems.push(label + " " + JSON.stringify({ failed: r.failed, err: r.err, msgs }));
    };
    if (!(await h.eval(() => HD2D.TimeOfDay.hour() === null))) problems.push("time of day should start off");

    // 1. Defaults exactly as inserted by the editor.
    for (const [name, def] of Object.entries(CMDS)) {
        await h.eval(([n, a]) => window.__call(n, a), [name, def.args]);
        await h.frames(2);
        await status("default " + name);
    }
    await h.shot("commands_defaults");
    await h.eval(() => {
        __call("DebugView", { overlay: "true", view: "Off" });
        __call("ScreenFade", { color: "#000000", opacity: "0", duration: "0" });
        __call("SetLetterbox", { size: "0", duration: "0" });
        __call("ResetVisualValues", { path: "all", duration: "0" });
        __call("SetPreset", { preset: "HD2D", duration: "0" });
    });

    // 2. Every option of every select argument.
    let calls = 0;
    for (const [name, def] of Object.entries(CMDS)) {
        for (const [arg, opts] of Object.entries(def.options)) {
            for (const o of opts) {
                const value = typeof o === "string" ? o : o.value;
                const args = Object.assign({}, def.args, { [arg]: value });
                if (name === "SetParallax") args.image = "Clouds";
                if (name === "ScreenFade") args.opacity = "0";
                if (name === "CreateLight" || name === "SetParticles") args.id = "opt" + calls;
                await h.eval(([n, a]) => window.__call(n, a), [name, args]);
                calls++;
                if (calls % 6 === 0) await h.frames(1);
                await status("option " + name + "." + arg + "=" + value);
            }
        }
    }
    await h.frames(5);
    await status("after options");
    console.log("option calls:", calls);
    await h.shot("commands_options");
    await h.eval(() => {
        for (const [n, a] of [
            ["DebugView", { overlay: "true", view: "Off" }], ["SetQuality", { quality: "Default" }], ["SetShadows", { quality: "Auto" }],
            ["EnableEffect", { effect: "All" }], ["RemoveLight", { id: "all" }], ["RemoveParticles", { id: "all" }],
            ["RemoveParallax", { id: "all" }], ["SetCameraZoom", { zoom: "1", duration: "0" }], ["CameraRotation", { angle: "0", duration: "0" }],
            ["SetLetterbox", { size: "0", duration: "0" }], ["ScreenFade", { opacity: "0", duration: "0" }],
            ["ResetVisualValues", { path: "all", duration: "0" }], ["SetPreset", { preset: "HD2D", duration: "0" }],
            ["SetCameraFocus", { target: "Player", duration: "0" }], ["CameraOffset", { x: "0", y: "0", duration: "0" }]
        ]) __call(n, a);
    });
    await h.frames(10);

    // 3. Semantic checks.
    const failures = await h.eval(() => {
        const bad = [];
        const ok = (label, cond, info) => {
            if (!cond) bad.push(label + " " + JSON.stringify(info));
        };
        const d = () => HD2D.State.data();
        const near = (a, b) => Math.abs(a - b) < 1e-3;
        __call("SetPreset", { preset: "Night", duration: "0" });
        ok("SetPreset", d().preset === "Night", d().preset);
        __call("SetPreset", { preset: "forest", duration: "0" });
        ok("SetPreset ignores case", d().preset === "Forest", d().preset);
        __call("SetPreset", { preset: "Nope", duration: "0" });
        ok("unknown preset keeps the current one", d().preset === "Forest", d().preset);
        __call("SetPreset", { preset: "Town", duration: "30", remember: "true" });
        ok("SetPreset remember + transition", d().mapPresets[$gameMap.mapId()] === "Town" && d().trans && d().trans.dur === 30, d().mapPresets);
        __call("ResetDepth", { target: "All" });
        __call("SetDepth", { target: "This Event", depth: "20" });
        const keys = Object.keys(d().depth);
        ok("SetDepth this event", keys.length === 1 && d().depth[keys[0]].depth === 20, d().depth);
        __call("SetDepth", { target: "Picture", pictureId: "3", depth: "70" });
        ok("SetDepth picture", d().pictures[3] && d().pictures[3].depth === 70, d().pictures);
        __call("SetEmissive", { target: "Player", strength: "2" });
        ok("SetEmissive player", Object.values(d().depth).some(e => e.emissive === 2), d().depth);
        __call("ResetDepth", { target: "This Event" });
        ok("ResetDepth this event", d().depth[keys[0]].depth === undefined, d().depth);
        __call("ResetDepth", { target: "All" });
        ok("ResetDepth all", !Object.keys(d().depth).length && !Object.keys(d().pictures).length, d().depth);
        __call("SetFocusDepth", { depth: "20", duration: "0" });
        ok("SetFocusDepth", near(HD2D.get("dof.focus"), 20), HD2D.get("dof.focus"));
        __call("FocusOnTarget", { target: "Event", eventId: "6", speed: "0.5", enabled: "true" });
        ok("FocusOnTarget", d().autoFocus && d().autoFocus.target === "event" && d().autoFocus.eventId === 6, d().autoFocus);
        __call("FocusOnTarget", { enabled: "false" });
        ok("FocusOnTarget off", d().autoFocus === null, d().autoFocus);
        __call("SetDepthOfField", { enabled: "false", duration: "0" });
        ok("SetDepthOfField off", HD2D.get("dof.weight") === 0 && HD2D.get("dof.enabled") === false, HD2D.get("dof"));
        __call("SetDepthOfField", { enabled: "true", focusRange: "12", farBlur: "0.7", duration: "0" });
        ok("SetDepthOfField values", HD2D.get("dof.weight") === 1 && HD2D.get("dof.focusRange") === 12 && HD2D.get("dof.farBlur") === 0.7, HD2D.get("dof"));
        __call("SetBokeh", { quality: "high", maxCount: "40", duration: "0" });
        ok("SetBokeh", HD2D.get("bokeh.quality") === "high" && HD2D.get("bokeh.maxCount") === 40, HD2D.get("bokeh"));
        __call("SetAmbientLight", { color: "#336699", intensity: "0.5", duration: "0" });
        const ac = HD2D.get("ambient.color");
        ok("SetAmbientLight", near(ac[0], 0.2) && near(ac[2], 0.6) && HD2D.get("ambient.intensity") === 0.5, ac);
        __call("SetDirectionalLight", { angle: "90", elevation: "30", duration: "0" });
        ok("SetDirectionalLight", HD2D.get("sun.angle") === 90 && HD2D.get("sun.elevation") === 30, HD2D.get("sun"));
        __call("SetBloom", { threshold: "0.5", intensity: "0.9", duration: "0" });
        ok("SetBloom", HD2D.get("bloom.threshold") === 0.5 && HD2D.get("bloom.intensity") === 0.9, HD2D.get("bloom"));
        __call("SetVignette", { color: "#ff0000", intensity: "0.6", duration: "0" });
        ok("SetVignette", HD2D.get("vignette.color")[0] === 1 && HD2D.get("vignette.intensity") === 0.6, HD2D.get("vignette"));
        __call("SetFog", { layer: "All", opacity: "0.3", duration: "0" });
        ok("SetFog all layers", ["near", "mid", "far"].every(l => HD2D.get("fog." + l + "Opacity") === 0.3), HD2D.get("fog"));
        __call("SetColorGrade", { preset: "Sepia", duration: "0" });
        ok("SetColorGrade preset", near(HD2D.get("grade.saturation"), HD2D.gradePreset("Sepia").saturation) && HD2D.get("grade.weight") === 1, HD2D.get("grade"));
        __call("SetColorGrade", { preset: "(custom)", exposure: "0.2", duration: "0" });
        ok("SetColorGrade value", HD2D.get("grade.exposure") === 0.2, HD2D.get("grade.exposure"));
        __call("SetShadows", { opacity: "0.7", quality: "Off", duration: "0" });
        ok("SetShadows", HD2D.get("shadows.opacity") === 0.7 && HD2D.State.quality().shadowMode === 0, HD2D.get("shadows"));
        __call("SetShadows", { quality: "Auto", duration: "0" });
        ok("SetShadows quality auto", HD2D.State.shadowQualityKey() === "auto", HD2D.State.shadowQualityKey());
        __call("SetRimLight", { followSun: "false", angle: "45", duration: "0" });
        ok("SetRimLight", HD2D.get("rim.followSun") === false && HD2D.get("rim.angle") === 45, HD2D.get("rim"));
        __call("SetVisualValue", { path: "Bloom.Intensity", value: "0.25", duration: "0" });
        ok("SetVisualValue ignores case", HD2D.get("bloom.intensity") === 0.25, HD2D.get("bloom.intensity"));
        __call("SetVisualValue", { path: "depth of field.near blur", value: "0.4", duration: "0" });
        ok("SetVisualValue spaced path", HD2D.get("dof.nearBlur") === 0.4, HD2D.get("dof"));
        const before = Object.keys(d().overrides).length;
        __call("SetVisualValue", { path: "blom.intensity", value: "0.4", duration: "0" });
        ok("unknown path ignored", Object.keys(d().overrides).length === before, Object.keys(d().overrides));
        __call("SetVisualValue", { path: "ambient.color", value: "#ffffff", duration: "0" });
        ok("SetVisualValue color", String(HD2D.get("ambient.color")) === "1,1,1", HD2D.get("ambient.color"));
        __call("SetVisualValue", { path: "grade.enabled", value: "false", duration: "0" });
        ok("SetVisualValue enabled", HD2D.get("grade.weight") === 0, HD2D.get("grade"));
        __call("ResetVisualValues", { path: "bloom", duration: "0" });
        ok("ResetVisualValues section", !Object.keys(d().overrides).some(k => k.startsWith("bloom.")) && Object.keys(d().overrides).length > 0, Object.keys(d().overrides));
        __call("ResetVisualValues", { path: "All", duration: "0" });
        ok("ResetVisualValues all", !Object.keys(d().overrides).length, Object.keys(d().overrides));
        const zoom = __call("SetCameraZoom", { zoom: "1.5", duration: "20", wait: "true" });
        ok("SetCameraZoom wait", zoom._waitCount === 20 && HD2D.Camera.data().zoomTween, zoom._waitCount);
        __call("SetCameraFocus", { target: "Map Position", x: "10", y: "12", duration: "0" });
        ok("SetCameraFocus point", JSON.stringify(HD2D.Camera.data().follow).includes("point"), HD2D.Camera.data().follow);
        __call("SetCameraFocus", { target: "This Event", duration: "0" });
        ok("SetCameraFocus this event", HD2D.Camera.data().follow && HD2D.Camera.data().follow.id === 6, HD2D.Camera.data().follow);
        __call("SmoothCamera", { mode: "Off" });
        ok("SmoothCamera off", HD2D.Camera.data().smooth === false, HD2D.Camera.data().smooth);
        __call("SmoothCamera", { mode: "Default" });
        ok("SmoothCamera default", HD2D.Camera.data().smooth === null, HD2D.Camera.data().smooth);
        __call("CreateLight", { id: "t1", type: "Spot", attach: "Player", radius: "200", color: "#ff8800", cone: "40", facing: "true" });
        ok("CreateLight", d().lights.t1 && d().lights.t1.type === "spot" && d().lights.t1.attach === "player", d().lights);
        __call("RemoveLight", { id: "t1" });
        ok("RemoveLight", !d().lights.t1 || d().lights.t1.removing, d().lights.t1);
        __call("CreateLight", { id: "t2", attach: "Map Position", x: "10", y: "10" });
        __call("RemoveLight", { id: "all", fadeDuration: "0" });
        ok("RemoveLight all", !Object.keys(d().lights).length, Object.keys(d().lights));
        __call("DisableEffect", { effect: "Bloom" });
        ok("DisableEffect", !HD2D.State.effectOn("bloom"), d().toggles);
        __call("EnableEffect", { effect: "Bloom" });
        ok("EnableEffect", HD2D.State.effectOn("bloom"), d().toggles);
        __call("SetParallax", { id: "sky", image: "Clouds", depth: "95", loop: "Both", scrollX: "1" });
        ok("SetParallax", d().layers.sky && d().layers.sky.loopX && d().layers.sky.loopY, d().layers.sky);
        __call("SetParticles", { id: "ff", type: "Fireflies", amount: "20", attach: "Event", eventId: "6", radius: "40" });
        ok("SetParticles", d().emitters.ff && d().emitters.ff.area === "event" && d().emitters.ff.eventId === 6, d().emitters.ff);
        __call("SetQuality", { quality: "Low" });
        ok("SetQuality", HD2D.State.qualityKey() === "low", HD2D.State.qualityKey());
        __call("SetQuality", { quality: "Default" });
        ok("SetQuality default", d().quality === null, d().quality);
        __call("DebugView", { overlay: "false", view: "Lighting" });
        ok("DebugView", HD2D.Debug.view === 3 && HD2D.Debug.overlay === false, [HD2D.Debug.view, HD2D.Debug.overlay]);
        __call("DebugView", { overlay: "true", view: "Off" });
        __call("SetTimeOfDay", { time: "Off", duration: "0" });
        __call("SetTimeOfDay", { time: "Sunset", duration: "0" });
        ok("SetTimeOfDay turns time on", HD2D.TimeOfDay.hour() === 18, d().time);
        __call("SetTimeOfDay", { time: "Morning", duration: "60" });
        ok("time moves forward", d().timeTween && d().timeTween.from === 18 && d().timeTween.to === 32, d().timeTween);
        __call("SetTimeOfDay", { time: "Off", duration: "30" });
        ok("SetTimeOfDay off", HD2D.TimeOfDay.hour() === null && d().trans && d().trans.dur === 30, d().time);
        return bad;
    });
    await h.frames(20);
    await status("after checks");
    for (const f of failures) problems.push("check failed: " + f);
    if (problems.length) throw new Error(problems.length + " problem(s):\n" + problems.join("\n"));
    console.log("all commands ok");
};
