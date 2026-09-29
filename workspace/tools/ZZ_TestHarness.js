// Test-only helpers (never shipped): silent audio, no battle animations,
// optional auto-advance of messages, error capture.
(() => {
    class FakeAudio {
        constructor(url) { this.url = url; this.volume = 100; this.pitch = 100; this.pan = 0; this.name = ""; this.frameCount = 0; }
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
    AudioManager.createBuffer = (folder, name) => new FakeAudio(folder + name);
    AudioManager.checkErrors = () => {};
    Spriteset_Base.prototype.createAnimation = function() {};
    window.__errors = [];
    window.addEventListener("error", e => window.__errors.push(String(e.error && e.error.stack || e.message)));
    const _catch = SceneManager.catchException;
    SceneManager.catchException = function(e) {
        window.__errors.push(String(e && e.stack || e));
        _catch.call(this, e);
    };
    window.__autoMsg = false;
    const _trig = Window_Message.prototype.isTriggered;
    window.__holdMsg = null; // regex: stop auto-advancing once matching text is on screen
    const _eot = Window_Message.prototype.onEndOfText;
    Window_Message.prototype.onEndOfText = function() {
        this.__lastText = this._textState ? this._textState.text : "";
        _eot.call(this);
    };
    const _sm = Window_Message.prototype.startMessage;
    Window_Message.prototype.startMessage = function() {
        this.__lastText = "";
        _sm.call(this);
    };
    Window_Message.prototype.shownText = function() {
        const ts = this._textState;
        return ts ? ts.text.slice(0, ts.index) : this.__lastText || "";
    };
    Window_Message.prototype.isTriggered = function() {
        const shown = this.shownText();
        if (window.__holdMsg && window.__holdMsg.test(shown)) return _trig.call(this);
        return window.__autoMsg || _trig.call(this);
    };
    // choice windows: take the next answer from window.__choices when auto
    window.__choices = [];
    const _cl = Window_ChoiceList.prototype.update;
    Window_ChoiceList.prototype.update = function() {
        _cl.call(this);
        if (window.__autoMsg && this.active && this.isOpen() && window.__choices.length) {
            this.select(window.__choices.shift());
            this.processOk();
        }
    };
    // name input: accept the default name
    const _sn = Scene_Name.prototype.start;
    Scene_Name.prototype.start = function() {
        _sn.call(this);
        if (window.__autoMsg) this.onInputOk();
    };
    // record every message line
    window.__messages = [];
    const _add = Game_Message.prototype.add;
    Game_Message.prototype.add = function(text) {
        window.__messages.push(text);
        _add.call(this, text);
    };
})();
