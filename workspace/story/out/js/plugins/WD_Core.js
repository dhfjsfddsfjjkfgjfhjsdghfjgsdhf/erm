//=============================================================================
// WD_Core.js  (stand-in)
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [stand-in v1.3.0] Minimal WD_Core text API so WD_Quest runs. Replace with the official WD_Core if you get it.
 * @author Claude (stand-in for Winthorp Darkrites' WD_Core)
 *
 * @help WD_Core.js — STAND-IN
 *
 * WD_Quest (by Winthorp Darkrites) needs his free plugin WD_Core v1.3+,
 * which wasn't in the project. This file provides only the functions
 * WD_Quest calls, under the same name, so the quest log works:
 *
 *   requiredCoreVersion  resolveLanguage (single language: the default text)
 *   realTextDimensions   drawTextExSize   autoTextSize
 *   autoWrap (word wrap + shrink to fit)  improvedTextExAligner
 *
 * If you download the official WD_Core (itch.io / ko-fi, free), just
 * replace this file with it: same file name, same place in the list
 * (above WD_Quest). Nothing else needs to change.
 */

(() => {
    "use strict";
    const VERSION = { major: 1, minor: 3, hotfix: 0 };

    // measure text with escape codes at a given font size
    const withFont = (win, size, fn) => {
        const oldReset = win.resetFontSettings;
        win.resetFontSettings = function() {
            oldReset.call(this);
            this.contents.fontSize = size;
        };
        try {
            return fn();
        } finally {
            win.resetFontSettings = oldReset;
        }
    };

    const measure = (win, text, size) =>
        withFont(win, size, () => {
            const r = win.textSizeEx(String(text));
            return { width: r.width, height: r.height };
        });

    // split text into lines that fit width at size (keeps explicit newlines)
    const wrapLines = (win, text, width, size) => {
        const out = [];
        for (const para of String(text).split("\n")) {
            const words = para.split(" ");
            let line = "";
            for (const w of words) {
                const test = line ? line + " " + w : w;
                if (line && measure(win, test, size).width > width) {
                    out.push(line);
                    line = w;
                } else {
                    line = test;
                }
            }
            out.push(line);
        }
        return out;
    };

    const Core = {
        version: VERSION,
        isStandIn: true,
        requiredCoreVersion(req) {
            const v = VERSION;
            if (v.major !== req.major) return v.major > req.major;
            if (v.minor !== req.minor) return v.minor > req.minor;
            return v.hotfix >= (req.hotfix || 0);
        },
        resolveLanguage(defaults /*, translations */) {
            return defaults;
        },
        realTextDimensions(win, text, fontSize) {
            return measure(win, text, fontSize || win.contents.fontSize);
        },
        drawTextExSize(win, text, x, y, width, fontSize) {
            return withFont(win, fontSize || win.contents.fontSize, () => win.drawTextEx(String(text), x, y, width));
        },
        autoTextSize(win, text, width, height) {
            let size = win.contents.fontSize;
            while (size > 10) {
                const d = measure(win, text, size);
                if (d.width <= width && (!height || d.height <= height)) break;
                size--;
            }
            return size;
        },
        autoWrap(win, x, y, width, height, text, maxFont, align) {
            text = String(text ?? "");
            let size = Math.max(10, Math.floor(maxFont || win.contents.fontSize));
            let lines = wrapLines(win, text, width, size);
            const lineH = s => Math.ceil(s * 1.35);
            while (size > 10 && lines.length * lineH(size) > height) {
                size--;
                lines = wrapLines(win, text, width, size);
            }
            let ly = y;
            for (const line of lines) {
                const w = measure(win, line, size).width;
                let lx = x;
                if (align === "center") lx = x + Math.max(0, (width - w) / 2);
                else if (align === "right") lx = x + Math.max(0, width - w);
                withFont(win, size, () => win.drawTextEx(line, lx, ly, width));
                ly += lineH(size);
            }
            win.contents.fontSize = size;
            return size;
        },
        improvedTextExAligner(win, text /*, align */) {
            return String(text ?? "");
        }
    };

    window.WD_Interplugin_Core = Object.assign(window.WD_Interplugin_Core || {}, Core);
})();
