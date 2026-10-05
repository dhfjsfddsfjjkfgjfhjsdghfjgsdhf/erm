//=============================================================================
// ZZ_HD2DTest.js - TEST ONLY, never ship this with a game.
//=============================================================================
/*:
 * @target MZ
 * @plugindesc [test only] Helpers for the HD2D_Diorama headless tests.
 * @author HD2D Diorama
 * @orderAfter HD2D_Diorama
 *
 * @help
 * Place below HD2D_Diorama in a COPY of the game used for testing.
 * - silent audio (headless browsers have no audio device)
 * - collects errors in window.__errors for the test runner
 * - URL options:  ?map=ID&x=X&y=Y  start a new game on that map
 *                 &noevents=1      no autorun / parallel events (no cutscenes)
 *                 &webgl1=1        force a WebGL 1 context
 *                 &ldr=1           pretend half-float textures are unsupported
 */
(() => {
    class SilentAudio {
        constructor(url) {
            this.url = url;
            this.volume = 100;
            this.pitch = 100;
            this.pan = 0;
            this.name = "";
            this.frameCount = 0;
        }
        isReady() { return true; }
        isError() { return false; }
        isPlaying() { return false; }
        play() {}
        stop() {}
        destroy() {}
        fadeIn() {}
        fadeOut() {}
        seek() { return 0; }
        addLoadListener(f) { f(); }
        addStopListener() {}
        retry() {}
    }
    AudioManager.createBuffer = (folder, name) => new SilentAudio(folder + name);
    AudioManager.checkErrors = () => {};

    window.__errors = [];
    window.addEventListener("error", e => window.__errors.push(String((e.error && e.error.stack) || e.message)));
    const _catchException = SceneManager.catchException;
    SceneManager.catchException = function(e) {
        window.__errors.push(String((e && e.stack) || e));
        _catchException.call(this, e);
    };
    const _catchUnknownError = SceneManager.catchUnknownError;
    SceneManager.catchUnknownError = function(e) {
        window.__errors.push("unknown: " + String((e && e.stack) || e));
        _catchUnknownError.call(this, e);
    };

    const q = new URLSearchParams(location.search);
    if (q.get("map")) {
        Scene_Boot.prototype.startNormalGame = function() {
            this.checkPlayerLocation();
            DataManager.setupNewGame();
            $gamePlayer.reserveTransfer(Number(q.get("map")), Number(q.get("x") || 5), Number(q.get("y") || 5), 2, 0);
            SceneManager.goto(Scene_Map);
        };
    }
    if (q.get("webgl1")) PIXI.settings.PREFER_ENV = PIXI.ENV.WEBGL;
    if (q.get("ldr") && window.HD2D) HD2D.GPU.probeHalfFloat = () => false;
    if (q.get("noevents")) {
        Game_Event.prototype.update = function() {
            Game_Character.prototype.update.call(this);
        };
        Game_Event.prototype.checkEventTriggerAuto = function() {};
        Game_Event.prototype.updateParallel = function() {};
        Game_CommonEvent.prototype.update = function() {};
        Game_Map.prototype.setupStartingEvent = function() {
            return false;
        };
    }
})();
