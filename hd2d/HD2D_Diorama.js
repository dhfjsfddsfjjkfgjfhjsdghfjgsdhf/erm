//=============================================================================
// HD2D_Diorama.js
//=============================================================================
// HD-2D inspired visual system for RPG Maker MZ: virtual depth for 2D
// objects, depth-based parallax, depth of field with bokeh, 2D lighting and
// shadows, ambient light, layered fog, bloom, color grading, vignette,
// atmospheric particles and a cinematic camera - all 2D, all PixiJS.
//=============================================================================

/*:
 * @target MZ
 * @plugindesc [v1.0.0] HD-2D style diorama look: virtual depth, DOF + bokeh, 2D lights & shadows, fog, bloom, grading, camera.
 * @author HD2D Diorama
 * @orderAfter TausiLighting
 * @orderAfter McKathlin_DayNight
 *
 * @help HD2D_Diorama.js  (version 1.0.0, RPG Maker MZ 1.0 - 1.9)
 * ============================================================================
 * WHAT IT DOES
 * ============================================================================
 * Makes a normal 2D RPG Maker map look like a miniature diorama seen through
 * a camera. The map stays 100% 2D (sprites, tiles, PixiJS shaders). Every
 * relevant object gets a VIRTUAL DEPTH, and depth drives parallax, depth of
 * field, fog, lighting, color and (optionally) scale.
 *
 * Depth scale:   0 = closest to the camera (foreground)
 *               50 = gameplay / focal plane
 *              100 = farthest background
 *
 * Without any setup, depth is derived from the vertical screen position
 * (top of the screen = farther, bottom = closer) with a configurable curve,
 * so ordinary maps work immediately with the default "HD2D" preset.
 *
 * ============================================================================
 * INSTALLATION
 * ============================================================================
 * 1. Copy HD2D_Diorama.js into your project's js/plugins folder.
 * 2. Add it in the Plugin Manager. Place it BELOW other plugins that change
 *    map rendering (e.g. TausiLighting, McKathlin_DayNight, map plugins).
 * 3. Play. Press F6 (playtest) for the debug overlay, F7 to cycle debug
 *    views (depth / blur / lighting / objects / bloom).
 * 4. Pick a look per map with a note tag, e.g.  <HD2DPreset: Forest>
 *
 * ============================================================================
 * PRESETS
 * ============================================================================
 * Built-in: HD2D (default), Forest, Town, Dungeon, Cave, Interior, Night,
 *           Sunset, Snow, Dream, Dark, Vanilla (everything off).
 * Color grades (Set Color Grade): Default, Neutral, Warm, Cold, Night,
 *           Sunset, Dungeon, Dream, Dark, Sepia, Vivid.
 * Custom presets: "Custom Presets" parameter. Blank fields inherit from the
 * Base preset. A custom preset named like a built-in one extends/replaces it.
 * Changing maps cross-fades between presets ("Map Transition Frames").
 *
 * ============================================================================
 * MAP NOTE TAGS
 * ============================================================================
 * <HD2DPreset: Forest>            visual preset of this map
 * <HD2DSet: dof.radius=6, bloom.intensity=0.5>
 *                                 override any preset value on this map
 *                                 (see "SETTING PATHS" below)
 * <HD2DFocus: 55>                 DOF focus depth for this map
 * <HD2DAmbient: #6070c0, 0.4>     ambient color and intensity
 * <HD2DDisable: dof, fog>         turn effects off on this map
 * <HD2DEnable: perspective>       turn preset-disabled effects on
 * <HD2DOff>                       no HD2D effects on this map
 * <HD2DTimeOfDay: off>            ignore the time of day on this map
 * <HD2DRegionDepth: 1=20, 2=80>   region depths (adds to the parameter)
 * <HD2DRegionEmissive: 7=1.5>     glowing regions (lava, crystals ...)
 * <HD2DBlockRegions: 5, 6>        regions that block light (tile shadows)
 * <HD2DBlockTerrain: 3>           terrain tags that block light
 * <HD2DLayer: Mountains, depth 85, loop x, scroll 0.2 0, y -40>
 *     Depth parallax layer from img/parallaxes. Options: depth n,
 *     loop x|y|xy|none, scroll sx sy (px/frame), x n, y n (offset),
 *     factor fx fy (scroll factor, default from depth), opacity 0-255,
 *     blend normal|add|multiply|screen, scale n, zoom n (0-1 zoom
 *     influence), front true|false, folder name, id name.
 *     Layers with depth < focal depth are drawn in front of the map.
 * <HD2DParallaxDepth: 95>         give the map's own parallax a depth
 *                                 (it then scrolls by depth and shows
 *                                 through empty tiles as background)
 * <HD2DParticles: dust, amount 30, depth 20-80, color #fff, size 1, speed 1>
 *     Types: dust, motes, light, mist, fog, rain, storm, snow, ash, embers,
 *     fireflies, magic, leaves, petals, sunbeams
 * <HD2DNoPresetParticles>         do not use the preset's particles
 * <HD2DLight: x, y, radius, color, intensity, options>
 *                                 static point light at tile x,y
 * <HD2DSpotLight: x, y, radius, color, intensity, direction, cone, options>
 * <HD2DLightRegion: region, radius, color, intensity, options>
 *                                 a light on every tile of a region
 * <HD2DZoom: 1.25>                camera zoom when entering the map
 *
 * ============================================================================
 * EVENT NOTE / COMMENT TAGS
 * ============================================================================
 * Tags can be in the event note (all pages) or in a Comment on a page
 * (only while that page is active).
 * <HD2DDepth: 25>                 fixed depth (no tag = automatic depth)
 * <HD2DDepthOffset: -10>          shift the automatic depth
 * <HD2DEmissive> / <HD2DEmissive: 1.5>
 *                                 glows (ignores darkness, feeds bloom)
 * <HD2DForeground> / <HD2DForeground: 12, parallax 1.2, scale 1.1, fade false>
 *     Foreground framing element (branches, rocks, pillars): drawn above
 *     the map with stronger parallax and near blur; fades while it covers
 *     the player (fade false to disable).
 * <HD2DParallax: 1.15>            parallax factor for foreground elements
 * <HD2DScale: 1.2>                manual scale   <HD2DNoScale> no depth scale
 * <HD2DLight: radius, color, intensity, options>
 * <HD2DSpotLight: radius, color, intensity, direction|facing, cone, options>
 *     Light options: falloff n, softness 0-1, flicker 0-1, speed n,
 *     offsetX n, offsetY n, shadows true|false, depth n, range n (depth
 *     range lit), glow 0-2, height n (normal maps), facing true.
 *     Example torch:  <HD2DLight: 160, #ff9a40, 1.2, flicker 0.35>
 * <HD2DShadowCaster>              this event blocks light (tile shadows)
 * <HD2DShadow> / <HD2DNoShadow>   force character shadow on / off
 * <HD2DRim: 0.5> / <HD2DNoRim>    rim light strength for this sprite
 * <HD2DNormalMap: Actor1_normal>  normal map in img/characters
 * <HD2DParticles: embers, amount 8, radius 16>
 *                                 particles emitted at this event
 * <HD2DSortByDepth>               sort by depth instead of screen Y
 *
 * Actor notes: <HD2DLight: ...> (lantern for the party leader),
 * <HD2DNormalMap: file>, <HD2DRim: n>, <HD2DNoShadow>.
 *
 * ============================================================================
 * PLUGIN COMMANDS (all value changes can transition over N frames)
 * ============================================================================
 * Set Visual Preset, Set Time Of Day, Set Depth, Reset Depth, Set Emissive,
 * Set Focus Depth, Focus On Target (auto focus), Set Depth Of Field,
 * Set Bokeh, Set Ambient Light, Set Directional Light, Create Light,
 * Remove Light, Enable Effect, Disable Effect, Set Bloom, Set Vignette,
 * Set Fog, Set Color Grade, Set Shadows, Set Rim Light, Set Visual Value,
 * Reset Visual Values, Set Camera Zoom, Set Camera Focus (pan / follow),
 * Camera Offset, Camera Shake, Camera Rotation, Smooth Camera, Letterbox,
 * Screen Fade, Set Parallax Layer, Remove Parallax Layer, Set Particles,
 * Remove Particles, Set Quality, Debug View.
 *
 * ============================================================================
 * SETTING PATHS (for <HD2DSet>, "Set Visual Value" and HD2D.set)
 * ============================================================================
 * depth.focalDepth nearDepth farDepth focalY followPlayer curve strength
 *       upperTileOffset backgroundDepth autoY enabled
 * parallax.foregroundBoost farFactor curve zoomInfluence enabled
 * dof.focus focusRange nearTransition farTransition nearBlur farBlur
 *     strength radius enabled
 * bokeh.intensity size threshold quality maxCount enabled
 * atmosphere.hazeColor hazeAmount farDesaturate farContrast farBrighten
 *     farTemperature nearSaturate nearContrast nearDarken enabled
 * ambient.color intensity temperature shadowTint shadowTintAmount
 *     highlightTint highlightTintAmount enabled
 * sun.angle elevation intensity color enabled   (directional light)
 * lights.intensity color dayFade glow enabled
 * shadows.opacity length softness contact lightShadows occlusion enabled
 * fog.color lit softness noise depthFog enabled
 *     fog.nearOpacity nearDepth nearScale nearSpeedX nearSpeedY
 *     (same for mid... and far...)
 * bloom.threshold knee intensity radius emissive enabled
 * grade.exposure contrast saturation brightness gamma hue temperature tint
 *     shadowColor shadowAmount highlightColor highlightAmount lut
 *     lutStrength enabled
 * vignette.intensity radius softness color pulse pulseSpeed enabled
 * rim.color intensity width angle followSun enabled
 * perspective.nearScale farScale enabled
 * Colors: #rrggbb or r,g,b (0-255).  Angles: 0 right, 90 down, 180 left,
 * 270 up (the direction the light comes FROM).
 *
 * ============================================================================
 * SCRIPT CALLS
 * ============================================================================
 * HD2D.setPreset("Night", 120);          HD2D.set("dof.focus", 70, 60);
 * HD2D.reset("dof", 30);                 HD2D.get("bloom.intensity");
 * HD2D.setEffect("bloom", false);        HD2D.setQuality("High");
 * HD2D.setTime(18.5, 600);               HD2D.Camera.setZoom(1.5, 60);
 * HD2D.addLight({ id: "a", attach: "player", radius: 200, intensity: 1 });
 * HD2D.removeLight("a", 30);
 * HD2D.registerSprite(mySprite, { depth: 30, emissive: 1 });
 *
 * ============================================================================
 * QUALITY LEVELS
 * ============================================================================
 * Low    : quarter-res light/blur, 12-tap DOF, no bokeh sprites, blob
 *          shadows, 2-level bloom, 1 fog layer, 8 lights, fewer particles.
 * Medium : half-res light, 20-tap DOF, light bokeh, sun/light silhouette
 *          shadows, 3-level bloom, 2 fog layers, 16 lights.   (default)
 * High   : 32-tap DOF + bokeh sprites, tile light occlusion (shadows from
 *          walls/regions), normal maps, 4-level bloom, 3 fog layers.
 * Ultra  : full-res light, 48-tap DOF, longer occlusion rays, 5 bloom
 *          levels, more particles. Only for strong GPUs.
 * Every effect can be switched off separately ("Effects" parameter and
 * Enable/Disable Effect commands) to find performance bottlenecks.
 *
 * ============================================================================
 * COMPATIBILITY NOTES
 * ============================================================================
 * - No core files are changed; everything uses aliases. Works with maps,
 *   events, player, followers, vehicles, pictures, animations, weather.
 *   Battles get color grading, bloom, vignette and blurred battlebacks.
 * - TausiLighting: by default (Auto) HD2D lighting stays off on maps where
 *   Tausi lights exist, all other HD2D effects still apply. Camera zoom is
 *   not known to TausiLighting, so keep zoom at 1 on Tausi-lit maps.
 * - McKathlin_DayNight / screen tint: HD2D keeps the map's screen tone. If
 *   you use HD2D time of day, set its "Hour Variable" to the same variable
 *   and make the tint plugin's tones neutral to avoid double darkening.
 * - If anything fails on a device, HD2D disables itself for that scene and
 *   logs the error instead of stopping the game.
 * - Pixel Perfect Mode keeps pixel art crisp (nearest filtering, rounded
 *   positions, camera snapped to whole pixels). Effects such as blur and
 *   bloom are smooth by nature but the sharp parts stay pixel-exact.
 *
 * ============================================================================
 * TERMS
 * ============================================================================
 * Free for commercial and non-commercial use.
 *
 * @param General
 * @text ---- General ----
 *
 * @param Default Preset
 * @parent General
 * @text Default Preset
 * @desc Preset used on maps without <HD2DPreset>. Built-in: HD2D, Forest, Town, Dungeon, Cave, Interior, Night, Sunset, Snow, Dream, Dark, Vanilla.
 * @type combo
 * @option HD2D
 * @option Forest
 * @option Town
 * @option Dungeon
 * @option Cave
 * @option Interior
 * @option Night
 * @option Sunset
 * @option Snow
 * @option Dream
 * @option Dark
 * @option Vanilla
 * @default HD2D
 *
 * @param Quality
 * @parent General
 * @desc Performance level. Low and Medium run on most hardware; High and Ultra enable expensive effects.
 * @type select
 * @option Low
 * @option Medium
 * @option High
 * @option Ultra
 * @default Medium
 *
 * @param Adaptive Quality
 * @parent General
 * @desc Automatically steps the quality down when the frame rate stays below 50 FPS.
 * @type boolean
 * @default false
 *
 * @param Effects
 * @parent General
 * @text Effect Toggles
 * @desc Turn whole systems on or off (can also be changed in game with Enable/Disable Effect).
 * @type struct<Effects>
 * @default {"Depth System":"true","Parallax":"true","Depth Of Field":"true","Bokeh":"true","Lighting":"true","Shadows":"true","Ambient Lighting":"true","Bloom":"true","Color Grading":"true","Vignette":"true","Fog":"true","Particles":"true","Normal Maps":"true","Rim Lighting":"true","Atmospheric Perspective":"true","Camera Effects":"true","Emissive":"true","Perspective Scaling":"true","Depth Weather":"true"}
 *
 * @param Pixel Perfect Mode
 * @parent General
 * @desc Nearest-neighbour filtering for map art, rounded sprite positions and pixel-snapped camera.
 * @type boolean
 * @default true
 *
 * @param Round Pixels
 * @parent Pixel Perfect Mode
 * @desc Round sprite vertex positions to whole pixels (only with Pixel Perfect Mode).
 * @type boolean
 * @default true
 *
 * @param Map Transition Frames
 * @parent General
 * @desc Frames used to cross-fade the look when moving to a map with a different preset (0 = instant).
 * @type number
 * @min 0
 * @default 40
 *
 * @param Keep Overrides On Transfer
 * @parent General
 * @desc Keep values changed by plugin commands when changing maps (otherwise each map starts from its preset).
 * @type boolean
 * @default false
 *
 * @param Post FX On Pictures
 * @parent General
 * @desc Apply grading / bloom / vignette to pictures too (off: pictures stay untouched, good for UI pictures).
 * @type boolean
 * @default false
 *
 * @param TausiLighting Compatibility
 * @parent General
 * @desc Auto: HD2D lighting is off on maps lit by TausiLighting. HD2D Off: always off when Tausi is installed. Both: keep both.
 * @type select
 * @option Auto
 * @option HD2D Off
 * @option Both
 * @default Auto
 *
 * @param Depth
 * @text ---- Depth ----
 *
 * @param Region Depths
 * @parent Depth
 * @desc Regions with a fixed depth (0 near - 50 focal - 100 far). Maps can add more with <HD2DRegionDepth: id=depth>.
 * @type struct<RegionDepth>[]
 * @default []
 *
 * @param Region Emissive
 * @parent Depth
 * @desc Regions whose tiles glow (unaffected by darkness, bloom). Maps can add more with <HD2DRegionEmissive>.
 * @type struct<RegionEmissive>[]
 * @default []
 *
 * @param Character Region Depth
 * @parent Depth
 * @desc Characters standing on a depth region take that region's depth (e.g. walking on a bridge).
 * @type boolean
 * @default true
 *
 * @param Sort Characters By Depth
 * @parent Depth
 * @desc Characters with an explicit depth are drawn in depth order instead of screen Y order.
 * @type boolean
 * @default false
 *
 * @param Lighting
 * @text ---- Lighting & Shadows ----
 *
 * @param Light Blocking Regions
 * @parent Lighting
 * @desc Region IDs that block light (tile shadows, High quality and above). Example: 5, 6, 10-12
 * @type string
 * @default
 *
 * @param Light Blocking Terrain Tags
 * @parent Lighting
 * @desc Terrain tags that block light. Example: 7
 * @type string
 * @default
 *
 * @param Wall Tiles Block Light
 * @parent Lighting
 * @desc A3/A4 wall and roof autotiles block light automatically.
 * @type boolean
 * @default false
 *
 * @param Object Characters Cast Shadows
 * @parent Lighting
 * @desc Object characters (file names starting with !) cast shadows too.
 * @type boolean
 * @default false
 *
 * @param Animations Unlit
 * @parent Lighting
 * @desc Skill/event animations are not darkened by ambient light and feed bloom.
 * @type boolean
 * @default true
 *
 * @param Light Height
 * @parent Lighting
 * @desc Height of lights above the ground (pixels), used with normal maps.
 * @type number
 * @min 1
 * @default 64
 *
 * @param Normal Map Suffix
 * @parent Lighting
 * @desc Suffix of normal map images (Actor1.png -> Actor1_normal.png).
 * @type string
 * @default _normal
 *
 * @param Auto-Detect Normal Maps
 * @parent Lighting
 * @desc Look for <name><suffix>.png for every character sheet. Off: only sheets tagged with <HD2DNormalMap>.
 * @type boolean
 * @default false
 *
 * @param Camera
 * @text ---- Camera ----
 *
 * @param Smooth Camera
 * @parent Camera
 * @desc The camera eases after the player instead of moving rigidly.
 * @type boolean
 * @default true
 *
 * @param Camera Follow Speed
 * @parent Camera
 * @desc Fraction of the remaining distance covered per frame (0.05 lazy - 1 rigid).
 * @type number
 * @decimals 2
 * @min 0.01
 * @max 1
 * @default 0.14
 *
 * @param Min Zoom
 * @parent Camera
 * @type number
 * @decimals 2
 * @min 0.25
 * @max 1
 * @default 0.50
 *
 * @param Max Zoom
 * @parent Camera
 * @type number
 * @decimals 2
 * @min 1
 * @default 3.00
 *
 * @param Rotation Overscan
 * @parent Camera
 * @desc Zoom in slightly while the camera is rotated so no empty corners show.
 * @type boolean
 * @default true
 *
 * @param Zoom DOF Influence
 * @parent Camera
 * @desc How much zooming in increases blur (0 = none, 1 = blur scales with zoom).
 * @type number
 * @decimals 2
 * @min 0
 * @max 2
 * @default 0.50
 *
 * @param Particles
 * @text ---- Particles ----
 *
 * @param Particle Density
 * @parent Particles
 * @desc Global multiplier for particle counts (also scaled by quality).
 * @type number
 * @decimals 2
 * @min 0
 * @max 4
 * @default 1.00
 *
 * @param TimeOfDay
 * @text ---- Time Of Day ----
 *
 * @param Time Of Day Mode
 * @parent TimeOfDay
 * @desc Off: no time of day. Manual: set with the Set Time Of Day command. Variable: read the hour from a variable.
 * @type select
 * @option Off
 * @option Manual
 * @option Variable
 * @default Off
 *
 * @param Hour Variable
 * @parent TimeOfDay
 * @desc Variable holding the hour (0-23) for Variable mode.
 * @type variable
 * @default 0
 *
 * @param Minute Variable
 * @parent TimeOfDay
 * @desc Optional variable holding the minutes (0-59) for smooth changes.
 * @type variable
 * @default 0
 *
 * @param Time Phases
 * @parent TimeOfDay
 * @desc Custom phases (leave empty for the built-in Dawn, Morning, Day, Afternoon, Sunset, Evening, Night).
 * @type struct<TimePhase>[]
 * @default []
 *
 * @param Presets
 * @text ---- Presets ----
 *
 * @param Custom Presets
 * @parent Presets
 * @desc Your own looks. Blank fields inherit from the Base preset.
 * @type struct<Preset>[]
 * @default []
 *
 * @param Battle
 * @text ---- Battle ----
 *
 * @param Battle Effects
 * @parent Battle
 * @desc Use grading, bloom, vignette and blurred battlebacks in battle.
 * @type boolean
 * @default true
 *
 * @param Battle Preset
 * @parent Battle
 * @desc Preset for battles. Empty = keep the current map look.
 * @type combo
 * @option HD2D
 * @option Forest
 * @option Town
 * @option Dungeon
 * @option Night
 * @option Sunset
 * @option Dream
 * @option Dark
 * @default
 *
 * @param Battle Background Blur
 * @parent Battle
 * @desc Battleback blur relative to the map DOF far blur (0 = sharp).
 * @type number
 * @decimals 2
 * @min 0
 * @max 4
 * @default 0.50
 *
 * @param Debug
 * @text ---- Debug ----
 *
 * @param Debug Mode
 * @parent Debug
 * @desc When the debug overlay keys work.
 * @type select
 * @option Off
 * @option Playtest
 * @option Always
 * @default Playtest
 *
 * @param Debug Overlay Key
 * @parent Debug
 * @desc Toggles the info overlay (FPS, depth, focus, lights, effects, render textures).
 * @type select
 * @option F6
 * @option F7
 * @option F10
 * @option F11
 * @option F12
 * @default F6
 *
 * @param Debug View Key
 * @parent Debug
 * @desc Cycles debug views: Depth (red near / green focal / blue far), Blur, Lighting, Objects, Bloom.
 * @type select
 * @option F6
 * @option F7
 * @option F10
 * @option F11
 * @option F12
 * @default F7
 *
 * @command SetPreset
 * @text Set Visual Preset
 * @desc Changes the whole look (with a smooth transition).
 *
 * @arg preset
 * @text Preset
 * @type combo
 * @option HD2D
 * @option Forest
 * @option Town
 * @option Dungeon
 * @option Cave
 * @option Interior
 * @option Night
 * @option Sunset
 * @option Snow
 * @option Dream
 * @option Dark
 * @option Vanilla
 * @default HD2D
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg keepOverrides
 * @text Keep Overrides
 * @desc Keep values set by other commands (otherwise they are cleared).
 * @type boolean
 * @default false
 *
 * @arg remember
 * @text Remember For This Map
 * @desc Use this preset whenever the player returns to this map.
 * @type boolean
 * @default false
 *
 * @command SetTimeOfDay
 * @text Set Time Of Day
 * @desc Manual time-of-day mode: moves the time to a phase or hour.
 *
 * @arg time
 * @text Time
 * @desc Phase name or hour (0-24, decimals allowed, e.g. 18.5).
 * @type combo
 * @option Dawn
 * @option Morning
 * @option Day
 * @option Afternoon
 * @option Sunset
 * @option Evening
 * @option Night
 * @default Day
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 120
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetDepth
 * @text Set Depth
 * @desc Gives a character or picture a fixed virtual depth (0 near, 50 focal, 100 far).
 *
 * @arg target
 * @text Target
 * @type select
 * @option This Event
 * @option Event
 * @option Player
 * @option Follower
 * @option Vehicle
 * @option Picture
 * @default This Event
 *
 * @arg eventId
 * @text Event / Follower / Vehicle ID
 * @desc Event ID, follower number (1 = first follower) or vehicle (0 boat, 1 ship, 2 airship).
 * @type number
 * @default 0
 *
 * @arg pictureId
 * @text Picture ID
 * @type number
 * @min 1
 * @default 1
 *
 * @arg depth
 * @text Depth
 * @type number
 * @min 0
 * @max 100
 * @default 50
 *
 * @command ResetDepth
 * @text Reset Depth
 * @desc Returns a target to automatic depth.
 *
 * @arg target
 * @text Target
 * @type select
 * @option This Event
 * @option Event
 * @option Player
 * @option Follower
 * @option Vehicle
 * @option Picture
 * @option All
 * @default This Event
 *
 * @arg eventId
 * @text Event / Follower / Vehicle ID
 * @type number
 * @default 0
 *
 * @arg pictureId
 * @text Picture ID
 * @type number
 * @min 1
 * @default 1
 *
 * @command SetEmissive
 * @text Set Emissive
 * @desc Makes a character or picture glow (ignores darkness, feeds bloom). 0 = off.
 *
 * @arg target
 * @text Target
 * @type select
 * @option This Event
 * @option Event
 * @option Player
 * @option Follower
 * @option Vehicle
 * @option Picture
 * @default This Event
 *
 * @arg eventId
 * @text Event / Follower / Vehicle ID
 * @type number
 * @default 0
 *
 * @arg pictureId
 * @text Picture ID
 * @type number
 * @min 1
 * @default 1
 *
 * @arg strength
 * @text Strength
 * @type number
 * @decimals 2
 * @min 0
 * @max 4
 * @default 1
 *
 * @command SetFocusDepth
 * @text Set Focus Depth
 * @desc Moves the depth-of-field focus (rack focus).
 *
 * @arg depth
 * @text Focus Depth
 * @type number
 * @min 0
 * @max 100
 * @default 50
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command FocusOnTarget
 * @text Focus On Target (Auto Focus)
 * @desc Keeps the DOF focus on a character's depth until turned off.
 *
 * @arg target
 * @text Target
 * @type select
 * @option Player
 * @option This Event
 * @option Event
 * @option Follower
 * @default Player
 *
 * @arg eventId
 * @text Event / Follower ID
 * @type number
 * @default 0
 *
 * @arg speed
 * @text Follow Speed
 * @type number
 * @decimals 2
 * @min 0.01
 * @max 1
 * @default 0.10
 *
 * @arg enabled
 * @text Enabled
 * @type boolean
 * @default true
 *
 * @command SetDepthOfField
 * @text Set Depth Of Field
 * @desc Changes DOF values. Leave a field blank to keep it.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg focusRange
 * @text Focus Range
 * @desc +/- depth that stays sharp (default 7).
 * @type string
 * @default
 *
 * @arg nearBlur
 * @text Near Blur (0-1)
 * @type string
 * @default
 *
 * @arg farBlur
 * @text Far Blur (0-1)
 * @type string
 * @default
 *
 * @arg strength
 * @text Blur Strength
 * @type string
 * @default
 *
 * @arg radius
 * @text Blur Radius (px)
 * @type string
 * @default
 *
 * @arg nearTransition
 * @text Near Transition Range
 * @type string
 * @default
 *
 * @arg farTransition
 * @text Far Transition Range
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetBokeh
 * @text Set Bokeh
 * @desc Bokeh highlights in blurred areas. Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg intensity
 * @text Intensity
 * @type string
 * @default
 *
 * @arg size
 * @text Size
 * @type string
 * @default
 *
 * @arg threshold
 * @text Threshold (0-1)
 * @type string
 * @default
 *
 * @arg quality
 * @text Quality
 * @type select
 * @option (unchanged)
 * @value
 * @option Auto
 * @value auto
 * @option Low
 * @value low
 * @option Medium
 * @value medium
 * @option High
 * @value high
 * @default
 *
 * @arg maxCount
 * @text Max Bokeh Count
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @command SetAmbientLight
 * @text Set Ambient Light
 * @desc Global light color. Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg color
 * @text Color
 * @desc #rrggbb or r,g,b
 * @type string
 * @default
 *
 * @arg intensity
 * @text Intensity
 * @desc 1 = normal daylight, 0.35 = night, 0.25 = dungeon.
 * @type string
 * @default
 *
 * @arg temperature
 * @text Temperature
 * @desc -1 (cold) .. 1 (warm)
 * @type string
 * @default
 *
 * @arg shadowTint
 * @text Shadow Tint
 * @type string
 * @default
 *
 * @arg highlightTint
 * @text Highlight Tint
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetDirectionalLight
 * @text Set Directional Light
 * @desc Sun / moon light (direction, color, shadows). Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg angle
 * @text Angle
 * @desc Direction the light comes from: 0 right, 90 bottom, 180 left, 270 top.
 * @type string
 * @default
 *
 * @arg elevation
 * @text Elevation
 * @desc 90 = overhead (short shadows), 10 = low sun (long shadows).
 * @type string
 * @default
 *
 * @arg intensity
 * @text Intensity
 * @type string
 * @default
 *
 * @arg color
 * @text Color
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command CreateLight
 * @text Create Light
 * @desc Creates or replaces a light (saved with the game).
 *
 * @arg id
 * @text Light ID
 * @desc Name used to change or remove the light later.
 * @type string
 * @default light1
 *
 * @arg type
 * @text Type
 * @type select
 * @option Point
 * @option Spot
 * @default Point
 *
 * @arg attach
 * @text Attach To
 * @type select
 * @option This Event
 * @option Event
 * @option Player
 * @option Follower
 * @option Map Position
 * @option Screen Position
 * @default This Event
 *
 * @arg eventId
 * @text Event / Follower ID
 * @type number
 * @default 0
 *
 * @arg x
 * @text X
 * @desc Tile X (Map Position) or pixel X (Screen Position).
 * @type number
 * @decimals 2
 * @default 0
 *
 * @arg y
 * @text Y
 * @type number
 * @decimals 2
 * @default 0
 *
 * @arg offsetX
 * @text Offset X (px)
 * @type number
 * @min -9999
 * @default 0
 *
 * @arg offsetY
 * @text Offset Y (px)
 * @type number
 * @min -9999
 * @default 0
 *
 * @arg radius
 * @text Radius (px)
 * @type number
 * @min 1
 * @default 160
 *
 * @arg color
 * @text Color
 * @type string
 * @default #ffc890
 *
 * @arg intensity
 * @text Intensity
 * @type number
 * @decimals 2
 * @min 0
 * @default 1.00
 *
 * @arg falloff
 * @text Falloff
 * @desc Shape of the fade (1 linear, 2 smooth, 3 tight).
 * @type number
 * @decimals 2
 * @min 0.2
 * @default 2.00
 *
 * @arg softness
 * @text Softness (0-1)
 * @type number
 * @decimals 2
 * @min 0
 * @max 1
 * @default 0.50
 *
 * @arg direction
 * @text Spot Direction
 * @desc Degrees: 0 right, 90 down, 180 left, 270 up.
 * @type number
 * @max 360
 * @default 90
 *
 * @arg facing
 * @text Spot Follows Facing
 * @desc The spot turns with the character's facing direction.
 * @type boolean
 * @default false
 *
 * @arg cone
 * @text Spot Cone Angle
 * @type number
 * @min 1
 * @max 359
 * @default 50
 *
 * @arg flicker
 * @text Flicker (0-1)
 * @type number
 * @decimals 2
 * @min 0
 * @max 1
 * @default 0
 *
 * @arg shadows
 * @text Casts Tile Shadows
 * @desc Blocked by light-blocking tiles / events (High quality and above).
 * @type boolean
 * @default true
 *
 * @arg glow
 * @text Glow (blank = preset)
 * @type string
 * @default
 *
 * @arg depth
 * @text Depth (blank = auto)
 * @desc Lights only affect objects at a similar depth.
 * @type string
 * @default
 *
 * @arg scope
 * @text Scope
 * @type select
 * @option This Map
 * @option All Maps
 * @default This Map
 *
 * @arg fadeDuration
 * @text Fade In (frames)
 * @type number
 * @min 0
 * @default 0
 *
 * @command RemoveLight
 * @text Remove Light
 * @desc Removes a light created with Create Light ("all" removes all).
 *
 * @arg id
 * @text Light ID
 * @type string
 * @default light1
 *
 * @arg fadeDuration
 * @text Fade Out (frames)
 * @type number
 * @min 0
 * @default 0
 *
 * @command EnableEffect
 * @text Enable Effect
 * @desc Turns an effect system on.
 *
 * @arg effect
 * @text Effect
 * @type select
 * @option All
 * @option Depth System
 * @option Parallax
 * @option Depth Of Field
 * @option Bokeh
 * @option Lighting
 * @option Shadows
 * @option Ambient Lighting
 * @option Bloom
 * @option Color Grading
 * @option Vignette
 * @option Fog
 * @option Particles
 * @option Normal Maps
 * @option Rim Lighting
 * @option Atmospheric Perspective
 * @option Camera Effects
 * @option Emissive
 * @option Perspective Scaling
 * @option Depth Weather
 * @default Depth Of Field
 *
 * @command DisableEffect
 * @text Disable Effect
 * @desc Turns an effect system off.
 *
 * @arg effect
 * @text Effect
 * @type select
 * @option All
 * @option Depth System
 * @option Parallax
 * @option Depth Of Field
 * @option Bokeh
 * @option Lighting
 * @option Shadows
 * @option Ambient Lighting
 * @option Bloom
 * @option Color Grading
 * @option Vignette
 * @option Fog
 * @option Particles
 * @option Normal Maps
 * @option Rim Lighting
 * @option Atmospheric Perspective
 * @option Camera Effects
 * @option Emissive
 * @option Perspective Scaling
 * @option Depth Weather
 * @default Depth Of Field
 *
 * @command SetBloom
 * @text Set Bloom
 * @desc Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg threshold
 * @text Threshold (0-1)
 * @type string
 * @default
 *
 * @arg intensity
 * @text Intensity
 * @type string
 * @default
 *
 * @arg radius
 * @text Radius
 * @type string
 * @default
 *
 * @arg emissiveBoost
 * @text Emissive Boost
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetVignette
 * @text Set Vignette
 * @desc Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg intensity
 * @text Intensity (0-1)
 * @type string
 * @default
 *
 * @arg radius
 * @text Radius
 * @type string
 * @default
 *
 * @arg softness
 * @text Softness
 * @type string
 * @default
 *
 * @arg color
 * @text Color
 * @type string
 * @default
 *
 * @arg pulse
 * @text Pulse (animated)
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetFog
 * @text Set Fog
 * @desc Fog layers sit at a depth: everything behind them is fogged. Blank = unchanged.
 *
 * @arg layer
 * @text Layer
 * @type select
 * @option Near
 * @option Mid
 * @option Far
 * @option All
 * @default Far
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg opacity
 * @text Opacity (0-1)
 * @type string
 * @default
 *
 * @arg depth
 * @text Depth
 * @type string
 * @default
 *
 * @arg color
 * @text Color (all layers)
 * @type string
 * @default
 *
 * @arg noise
 * @text Patchiness (0-1, all layers)
 * @type string
 * @default
 *
 * @arg scale
 * @text Noise Scale
 * @type string
 * @default
 *
 * @arg speedX
 * @text Speed X
 * @type string
 * @default
 *
 * @arg speedY
 * @text Speed Y
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetColorGrade
 * @text Set Color Grade
 * @desc Applies a grade preset and/or individual values (blank = unchanged).
 *
 * @arg preset
 * @text Grade Preset
 * @type combo
 * @option (custom)
 * @option Default
 * @option Neutral
 * @option Warm
 * @option Cold
 * @option Night
 * @option Sunset
 * @option Dungeon
 * @option Dream
 * @option Dark
 * @option Sepia
 * @option Vivid
 * @default (custom)
 *
 * @arg exposure
 * @text Exposure (stops)
 * @type string
 * @default
 *
 * @arg contrast
 * @text Contrast (1 = normal)
 * @type string
 * @default
 *
 * @arg saturation
 * @text Saturation (1 = normal)
 * @type string
 * @default
 *
 * @arg brightness
 * @text Brightness (0 = normal)
 * @type string
 * @default
 *
 * @arg gamma
 * @text Gamma (1 = normal)
 * @type string
 * @default
 *
 * @arg hue
 * @text Hue Shift (degrees)
 * @type string
 * @default
 *
 * @arg temperature
 * @text Temperature (-1..1)
 * @type string
 * @default
 *
 * @arg tint
 * @text Tint (-1 green .. 1 magenta)
 * @type string
 * @default
 *
 * @arg lut
 * @text LUT Image
 * @desc Image in img/pictures (256x16 or 1024x32 strip). Blank = unchanged.
 * @type file
 * @dir img/pictures
 * @default
 *
 * @arg lutStrength
 * @text LUT Strength (0-1)
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetShadows
 * @text Set Shadows
 * @desc Character / tile shadow settings. Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg opacity
 * @text Opacity (0-1)
 * @type string
 * @default
 *
 * @arg length
 * @text Length
 * @type string
 * @default
 *
 * @arg softness
 * @text Softness
 * @type string
 * @default
 *
 * @arg contact
 * @text Contact Shadow (0-1)
 * @type string
 * @default
 *
 * @arg occlusion
 * @text Tile Occlusion (0-1)
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @command SetRimLight
 * @text Set Rim Light
 * @desc Bright edge on characters facing the light. Blank = unchanged.
 *
 * @arg enabled
 * @text Enabled
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg color
 * @text Color
 * @type string
 * @default
 *
 * @arg intensity
 * @text Intensity
 * @type string
 * @default
 *
 * @arg width
 * @text Width (px)
 * @type string
 * @default
 *
 * @arg angle
 * @text Light Angle
 * @type string
 * @default
 *
 * @arg followSun
 * @text Follow Directional Light
 * @type select
 * @option (unchanged)
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @command SetVisualValue
 * @text Set Visual Value
 * @desc Changes any setting by path, e.g. dof.radius, fog.farOpacity, grade.hue (see help).
 *
 * @arg path
 * @text Setting Path
 * @type string
 * @default bloom.intensity
 *
 * @arg value
 * @text Value
 * @desc Number, true/false, or color (#rrggbb).
 * @type string
 * @default 0.5
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command ResetVisualValues
 * @text Reset Visual Values
 * @desc Returns values changed by commands to the preset (blank path = everything).
 *
 * @arg path
 * @text Setting Path / Section
 * @desc e.g. dof, bloom.intensity. Blank = all.
 * @type string
 * @default
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @command SetCameraZoom
 * @text Set Camera Zoom
 * @desc Zooms the world (pictures and windows stay). Parallax and depth react to zoom.
 *
 * @arg zoom
 * @text Zoom
 * @type number
 * @decimals 2
 * @min 0.25
 * @default 1.00
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @option Ease Out Back
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command SetCameraFocus
 * @text Set Camera Focus (Pan)
 * @desc Pans the camera to a target and follows it.
 *
 * @arg target
 * @text Target
 * @type select
 * @option Player
 * @option This Event
 * @option Event
 * @option Map Position
 * @option None (hold position)
 * @default Player
 *
 * @arg eventId
 * @text Event ID
 * @type number
 * @default 0
 *
 * @arg x
 * @text Tile X
 * @type number
 * @default 0
 *
 * @arg y
 * @text Tile Y
 * @type number
 * @default 0
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command CameraOffset
 * @text Camera Offset
 * @desc Shifts the framing in pixels (e.g. look ahead or frame a cutscene).
 *
 * @arg x
 * @text Offset X (px)
 * @type number
 * @min -9999
 * @default 0
 *
 * @arg y
 * @text Offset Y (px)
 * @type number
 * @min -9999
 * @default 0
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command CameraShake
 * @text Camera Shake
 * @desc Smooth 2D camera shake (in addition to the normal Shake Screen).
 *
 * @arg power
 * @text Power (px)
 * @type number
 * @min 0
 * @default 6
 *
 * @arg speed
 * @text Speed
 * @type number
 * @min 1
 * @default 6
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 1
 * @default 30
 *
 * @arg direction
 * @text Direction
 * @type select
 * @option Both
 * @option Horizontal
 * @option Vertical
 * @default Both
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command CameraRotation
 * @text Camera Rotation
 * @desc Rolls the camera (degrees, positive = clockwise).
 *
 * @arg angle
 * @text Angle
 * @type number
 * @decimals 1
 * @min -360
 * @max 360
 * @default 0
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 60
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command SmoothCamera
 * @text Smooth Camera
 * @desc Turns camera easing on/off (Default = parameter).
 *
 * @arg mode
 * @text Mode
 * @type select
 * @option Default
 * @option On
 * @option Off
 * @default Default
 *
 * @command SetLetterbox
 * @text Letterbox
 * @desc Cinematic black bars (percent of screen height per bar, 0 = off).
 *
 * @arg size
 * @text Bar Size (%)
 * @type number
 * @min 0
 * @max 45
 * @default 10
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command ScreenFade
 * @text Screen Fade
 * @desc Fades the map (not windows) to a color. Opacity 0 fades back.
 *
 * @arg color
 * @text Color
 * @type string
 * @default #000000
 *
 * @arg opacity
 * @text Opacity (0-255)
 * @type number
 * @min 0
 * @max 255
 * @default 255
 *
 * @arg duration
 * @text Duration (frames)
 * @type number
 * @min 0
 * @default 30
 *
 * @arg easing
 * @text Easing
 * @type select
 * @option Linear
 * @option Smooth
 * @option Ease In
 * @option Ease Out
 * @option Ease In-Out
 * @option Sine
 * @default Smooth
 *
 * @arg wait
 * @text Wait For Completion
 * @type boolean
 * @default false
 *
 * @command SetParallax
 * @text Set Parallax Layer
 * @desc Adds or changes a depth parallax layer.
 *
 * @arg id
 * @text Layer ID
 * @type string
 * @default layer1
 *
 * @arg image
 * @text Image
 * @type file
 * @dir img/parallaxes
 * @default
 *
 * @arg folder
 * @text Folder
 * @desc Image folder inside img/ (parallaxes or pictures).
 * @type select
 * @option parallaxes
 * @option pictures
 * @default parallaxes
 *
 * @arg depth
 * @text Depth
 * @desc 0 near (in front of the map) .. 100 far (sky).
 * @type number
 * @min 0
 * @max 100
 * @default 85
 *
 * @arg loop
 * @text Loop
 * @type select
 * @option Horizontal
 * @option Vertical
 * @option Both
 * @option None
 * @default Horizontal
 *
 * @arg scrollX
 * @text Auto Scroll X (px/frame)
 * @type number
 * @decimals 2
 * @min -999
 * @default 0
 *
 * @arg scrollY
 * @text Auto Scroll Y (px/frame)
 * @type number
 * @decimals 2
 * @min -999
 * @default 0
 *
 * @arg x
 * @text Offset X (px)
 * @type number
 * @min -99999
 * @default 0
 *
 * @arg y
 * @text Offset Y (px)
 * @type number
 * @min -99999
 * @default 0
 *
 * @arg factorX
 * @text Scroll Factor X (blank = from depth)
 * @type string
 * @default
 *
 * @arg factorY
 * @text Scroll Factor Y (blank = from depth)
 * @type string
 * @default
 *
 * @arg opacity
 * @text Opacity
 * @type number
 * @min 0
 * @max 255
 * @default 255
 *
 * @arg blend
 * @text Blend Mode
 * @type select
 * @option Normal
 * @option Add
 * @option Multiply
 * @option Screen
 * @default Normal
 *
 * @arg scale
 * @text Scale
 * @type number
 * @decimals 2
 * @min 0.01
 * @default 1.00
 *
 * @arg scope
 * @text Scope
 * @type select
 * @option This Map
 * @option All Maps
 * @default This Map
 *
 * @command RemoveParallax
 * @text Remove Parallax Layer
 * @desc Removes a layer (also map-note layers). "all" removes all.
 *
 * @arg id
 * @text Layer ID
 * @type string
 * @default layer1
 *
 * @command SetParticles
 * @text Set Particles
 * @desc Adds or changes an atmospheric particle emitter.
 *
 * @arg id
 * @text Emitter ID
 * @type string
 * @default particles1
 *
 * @arg type
 * @text Type
 * @type select
 * @option Dust
 * @option Motes
 * @option Light
 * @option Mist
 * @option Fog
 * @option Rain
 * @option Storm
 * @option Snow
 * @option Ash
 * @option Embers
 * @option Fireflies
 * @option Magic
 * @option Leaves
 * @option Petals
 * @option Sunbeams
 * @default Dust
 *
 * @arg amount
 * @text Amount
 * @type number
 * @min 0
 * @default 30
 *
 * @arg depthMin
 * @text Depth Min (blank = type default)
 * @type string
 * @default
 *
 * @arg depthMax
 * @text Depth Max (blank = type default)
 * @type string
 * @default
 *
 * @arg color
 * @text Color (blank = type default)
 * @type string
 * @default
 *
 * @arg attach
 * @text Area
 * @type select
 * @option Screen
 * @option This Event
 * @option Event
 * @default Screen
 *
 * @arg eventId
 * @text Event ID
 * @type number
 * @default 0
 *
 * @arg radius
 * @text Spawn Radius (px)
 * @type number
 * @default 20
 *
 * @arg scope
 * @text Scope
 * @type select
 * @option This Map
 * @option All Maps
 * @default This Map
 *
 * @command RemoveParticles
 * @text Remove Particles
 * @desc Removes an emitter created with Set Particles ("all" removes all).
 *
 * @arg id
 * @text Emitter ID
 * @type string
 * @default particles1
 *
 * @command SetQuality
 * @text Set Quality
 * @desc Changes the quality level in game (e.g. from an options menu event).
 *
 * @arg quality
 * @text Quality
 * @type select
 * @option Default
 * @option Low
 * @option Medium
 * @option High
 * @option Ultra
 * @default Default
 *
 * @command DebugView
 * @text Debug View
 * @desc Shows the debug overlay / depth views from an event.
 *
 * @arg overlay
 * @text Overlay
 * @type boolean
 * @default true
 *
 * @arg view
 * @text View
 * @type select
 * @option Off
 * @option Depth
 * @option Blur
 * @option Lighting
 * @option Objects
 * @option Bloom
 * @default Depth
 */

/*~struct~Effects:
 * @param Depth System
 * @type boolean
 * @default true
 *
 * @param Parallax
 * @type boolean
 * @default true
 *
 * @param Depth Of Field
 * @type boolean
 * @default true
 *
 * @param Bokeh
 * @type boolean
 * @default true
 *
 * @param Lighting
 * @desc Point, spot and directional lights.
 * @type boolean
 * @default true
 *
 * @param Shadows
 * @type boolean
 * @default true
 *
 * @param Ambient Lighting
 * @type boolean
 * @default true
 *
 * @param Bloom
 * @type boolean
 * @default true
 *
 * @param Color Grading
 * @type boolean
 * @default true
 *
 * @param Vignette
 * @type boolean
 * @default true
 *
 * @param Fog
 * @type boolean
 * @default true
 *
 * @param Particles
 * @type boolean
 * @default true
 *
 * @param Normal Maps
 * @type boolean
 * @default true
 *
 * @param Rim Lighting
 * @type boolean
 * @default true
 *
 * @param Atmospheric Perspective
 * @type boolean
 * @default true
 *
 * @param Camera Effects
 * @desc Smooth follow, zoom, rotation, letterbox, fades.
 * @type boolean
 * @default true
 *
 * @param Emissive
 * @type boolean
 * @default true
 *
 * @param Perspective Scaling
 * @desc Allows depth-based scaling (still needs perspective.enabled in a preset).
 * @type boolean
 * @default true
 *
 * @param Depth Weather
 * @desc Draw RPG Maker weather as depth particles (rain / storm / snow).
 * @type boolean
 * @default true
 */

/*~struct~RegionDepth:
 * @param Region
 * @type number
 * @min 1
 * @max 255
 * @default 1
 *
 * @param Depth
 * @desc 0 near, 50 focal, 100 far.
 * @type number
 * @min 0
 * @max 100
 * @default 50
 */

/*~struct~RegionEmissive:
 * @param Region
 * @type number
 * @min 1
 * @max 255
 * @default 1
 *
 * @param Strength
 * @type number
 * @decimals 2
 * @min 0
 * @max 4
 * @default 1
 */

/*~struct~TimePhase:
 * @param Name
 * @type string
 * @default Day
 *
 * @param Hour
 * @desc Hour at which this phase is at full strength (0-24, decimals allowed).
 * @type number
 * @decimals 2
 * @min 0
 * @max 24
 * @default 12
 *
 * @param Ambient Tint
 * @desc Multiplies the map's ambient color (#ffffff = unchanged).
 * @type string
 * @default #ffffff
 *
 * @param Ambient Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Sun Tint
 * @type string
 * @default #ffffff
 *
 * @param Sun Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Sun Angle
 * @desc Blank = keep the preset's angle.
 * @type string
 * @default
 *
 * @param Sun Elevation
 * @desc Blank = keep the preset's elevation.
 * @type string
 * @default
 *
 * @param Exposure Offset
 * @type number
 * @decimals 2
 * @min -4
 * @default 0
 *
 * @param Temperature Offset
 * @type number
 * @decimals 2
 * @min -1
 * @default 0
 *
 * @param Saturation Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Contrast Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Fog Tint
 * @type string
 * @default #ffffff
 *
 * @param Fog Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Bloom Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Light Multiplier
 * @desc Strength of point/spot lights (lamps are brighter at night).
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Light Tint
 * @type string
 * @default #ffffff
 *
 * @param DOF Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Vignette Multiplier
 * @type number
 * @decimals 2
 * @min 0
 * @default 1
 *
 * @param Particles
 * @desc Extra particle type during this phase (e.g. fireflies). Blank = none.
 * @type string
 * @default
 *
 * @param Particle Amount
 * @type number
 * @min 0
 * @default 0
 */

/*~struct~Preset:
 * @param Name
 * @desc Use it with <HD2DPreset: Name> or Set Visual Preset.
 * @type string
 * @default MyPreset
 *
 * @param Base
 * @desc Preset to inherit from (blank fields below keep its values).
 * @type combo
 * @option HD2D
 * @option Forest
 * @option Town
 * @option Dungeon
 * @option Cave
 * @option Interior
 * @option Night
 * @option Sunset
 * @option Snow
 * @option Dream
 * @option Dark
 * @option Vanilla
 * @default HD2D
 *
 * @param Uses Time Of Day
 * @type select
 * @option inherit
 * @value
 * @option yes
 * @value true
 * @option no
 * @value false
 * @default
 *
 * @param Depth
 * @type struct<PresetDepth>
 * @default {}
 *
 * @param Parallax
 * @type struct<PresetParallax>
 * @default {}
 *
 * @param Depth Of Field
 * @type struct<PresetDof>
 * @default {}
 *
 * @param Bokeh
 * @type struct<PresetBokeh>
 * @default {}
 *
 * @param Atmosphere
 * @text Atmospheric Perspective
 * @type struct<PresetAtmosphere>
 * @default {}
 *
 * @param Ambient
 * @type struct<PresetAmbient>
 * @default {}
 *
 * @param Sun
 * @text Directional Light (Sun/Moon)
 * @type struct<PresetSun>
 * @default {}
 *
 * @param Lights
 * @text Point / Spot Lights
 * @type struct<PresetLights>
 * @default {}
 *
 * @param Shadows
 * @type struct<PresetShadows>
 * @default {}
 *
 * @param Fog
 * @type struct<PresetFog>
 * @default {}
 *
 * @param Bloom
 * @type struct<PresetBloom>
 * @default {}
 *
 * @param Color Grading
 * @type struct<PresetGrade>
 * @default {}
 *
 * @param Vignette
 * @type struct<PresetVignette>
 * @default {}
 *
 * @param Rim Light
 * @type struct<PresetRim>
 * @default {}
 *
 * @param Perspective
 * @text Perspective Scaling
 * @type struct<PresetPerspective>
 * @default {}
 *
 * @param Particles
 * @type struct<Emitter>[]
 * @default []
 *
 * @param Particle Mode
 * @desc Inherit: listed emitters replace the base list (empty keeps it). Add: append. Replace: always replace. None: no particles.
 * @type select
 * @option Inherit
 * @option Add
 * @option Replace
 * @option None
 * @default Inherit
 *
 * @param Extra Settings
 * @desc Any other values as path=value, separated by commas, e.g. dof.radius=6, fog.midOpacity=0.1
 * @type multiline_string
 * @default
 */

/*~struct~PresetDepth:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Auto Y Depth
 * @desc Derive depth from the vertical screen position.
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Focal Depth
 * @desc Depth of the gameplay plane (default 50).
 * @type string
 * @default
 *
 * @param Near Depth (Bottom)
 * @desc Depth at the bottom screen edge (default 30).
 * @type string
 * @default
 *
 * @param Far Depth (Top)
 * @desc Depth at the top screen edge (default 85).
 * @type string
 * @default
 *
 * @param Focal Y
 * @desc Screen position of the focal plane, 0 top - 1 bottom (default 0.56).
 * @type string
 * @default
 *
 * @param Focus Follows Player
 * @desc Keep the focal plane on the player's feet.
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Depth Curve
 * @desc 1 = linear, >1 = flat in the middle and steeper at the edges (default 1.4).
 * @type string
 * @default
 *
 * @param Depth Strength
 * @desc Scales the whole depth range (default 1).
 * @type string
 * @default
 *
 * @param Upper Tile Offset
 * @desc Depth offset for upper-layer (star) tiles such as tree tops (default -4).
 * @type string
 * @default
 *
 * @param Background Depth
 * @desc Depth of empty map areas where a background layer shows (default 96).
 * @type string
 * @default
 */

/*~struct~PresetParallax:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Foreground Boost
 * @desc Extra speed of layers in front of the focal plane (0.25 = 1.25x at depth 0).
 * @type string
 * @default
 *
 * @param Far Factor
 * @desc Scroll factor at depth 100 (default 0.1).
 * @type string
 * @default
 *
 * @param Curve
 * @type string
 * @default
 *
 * @param Zoom Influence
 * @desc 1 = far layers zoom less than the map (perspective), 0 = all zoom alike.
 * @type string
 * @default
 */

/*~struct~PresetDof:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Focus Depth
 * @type string
 * @default
 *
 * @param Focus Range
 * @desc +/- depth that stays sharp (default 7).
 * @type string
 * @default
 *
 * @param Near Transition
 * @type string
 * @default
 *
 * @param Far Transition
 * @type string
 * @default
 *
 * @param Near Blur
 * @desc 0-1 (default 0.85)
 * @type string
 * @default
 *
 * @param Far Blur
 * @desc 0-1 (default 1)
 * @type string
 * @default
 *
 * @param Blur Strength
 * @type string
 * @default
 *
 * @param Blur Radius
 * @desc Maximum blur in pixels (default 4.5).
 * @type string
 * @default
 */

/*~struct~PresetBokeh:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Size
 * @type string
 * @default
 *
 * @param Threshold
 * @type string
 * @default
 *
 * @param Quality
 * @type select
 * @option inherit
 * @value
 * @option auto
 * @option low
 * @option medium
 * @option high
 * @default
 *
 * @param Max Count
 * @type string
 * @default
 */

/*~struct~PresetAtmosphere:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Haze Color
 * @type string
 * @default
 *
 * @param Haze Amount
 * @type string
 * @default
 *
 * @param Far Desaturate
 * @type string
 * @default
 *
 * @param Far Contrast
 * @desc Contrast reduction of far objects.
 * @type string
 * @default
 *
 * @param Far Brighten
 * @type string
 * @default
 *
 * @param Far Temperature
 * @type string
 * @default
 *
 * @param Near Saturate
 * @type string
 * @default
 *
 * @param Near Contrast
 * @type string
 * @default
 *
 * @param Near Darken
 * @type string
 * @default
 */

/*~struct~PresetAmbient:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Color
 * @type string
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Temperature
 * @type string
 * @default
 *
 * @param Shadow Tint
 * @type string
 * @default
 *
 * @param Shadow Tint Amount
 * @type string
 * @default
 *
 * @param Highlight Tint
 * @type string
 * @default
 *
 * @param Highlight Tint Amount
 * @type string
 * @default
 */

/*~struct~PresetSun:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Angle
 * @desc Direction the light comes from (0 right, 90 bottom, 180 left, 270 top).
 * @type string
 * @default
 *
 * @param Elevation
 * @type string
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Color
 * @type string
 * @default
 */

/*~struct~PresetLights:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Color
 * @desc Tint for all lights.
 * @type string
 * @default
 *
 * @param Day Fade
 * @desc How much lights fade in bright ambient light (0-1).
 * @type string
 * @default
 *
 * @param Glow
 * @type string
 * @default
 */

/*~struct~PresetShadows:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Opacity
 * @type string
 * @default
 *
 * @param Length
 * @type string
 * @default
 *
 * @param Softness
 * @type string
 * @default
 *
 * @param Contact Shadow
 * @type string
 * @default
 *
 * @param Light Shadows
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Tile Occlusion
 * @type string
 * @default
 */

/*~struct~PresetFog:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Color
 * @type string
 * @default
 *
 * @param Lit
 * @desc How much ambient/lights color the fog (0-1).
 * @type string
 * @default
 *
 * @param Softness
 * @type string
 * @default
 *
 * @param Noise
 * @desc Patchiness 0-1.
 * @type string
 * @default
 *
 * @param Depth Fog
 * @desc Extra haze growing with depth.
 * @type string
 * @default
 *
 * @param Near Opacity
 * @type string
 * @default
 *
 * @param Near Depth
 * @type string
 * @default
 *
 * @param Near Scale
 * @type string
 * @default
 *
 * @param Near Speed X
 * @type string
 * @default
 *
 * @param Near Speed Y
 * @type string
 * @default
 *
 * @param Mid Opacity
 * @type string
 * @default
 *
 * @param Mid Depth
 * @type string
 * @default
 *
 * @param Mid Scale
 * @type string
 * @default
 *
 * @param Mid Speed X
 * @type string
 * @default
 *
 * @param Mid Speed Y
 * @type string
 * @default
 *
 * @param Far Opacity
 * @type string
 * @default
 *
 * @param Far Depth
 * @type string
 * @default
 *
 * @param Far Scale
 * @type string
 * @default
 *
 * @param Far Speed X
 * @type string
 * @default
 *
 * @param Far Speed Y
 * @type string
 * @default
 */

/*~struct~PresetBloom:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Threshold
 * @type string
 * @default
 *
 * @param Knee
 * @type string
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Radius
 * @type string
 * @default
 *
 * @param Emissive Boost
 * @type string
 * @default
 */

/*~struct~PresetGrade:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Exposure
 * @type string
 * @default
 *
 * @param Contrast
 * @type string
 * @default
 *
 * @param Saturation
 * @type string
 * @default
 *
 * @param Brightness
 * @type string
 * @default
 *
 * @param Gamma
 * @type string
 * @default
 *
 * @param Hue
 * @type string
 * @default
 *
 * @param Temperature
 * @type string
 * @default
 *
 * @param Tint
 * @type string
 * @default
 *
 * @param Shadow Color
 * @type string
 * @default
 *
 * @param Shadow Amount
 * @type string
 * @default
 *
 * @param Highlight Color
 * @type string
 * @default
 *
 * @param Highlight Amount
 * @type string
 * @default
 *
 * @param LUT
 * @type file
 * @dir img/pictures
 * @default
 *
 * @param LUT Strength
 * @type string
 * @default
 */

/*~struct~PresetVignette:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Radius
 * @type string
 * @default
 *
 * @param Softness
 * @type string
 * @default
 *
 * @param Color
 * @type string
 * @default
 *
 * @param Pulse
 * @type string
 * @default
 *
 * @param Pulse Speed
 * @type string
 * @default
 */

/*~struct~PresetRim:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Color
 * @type string
 * @default
 *
 * @param Intensity
 * @type string
 * @default
 *
 * @param Width
 * @type string
 * @default
 *
 * @param Angle
 * @type string
 * @default
 *
 * @param Follow Sun
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 */

/*~struct~PresetPerspective:
 * @param Enabled
 * @type select
 * @option inherit
 * @value
 * @option ON
 * @value true
 * @option OFF
 * @value false
 * @default
 *
 * @param Near Scale
 * @desc Scale at depth 0 (default 1.08).
 * @type string
 * @default
 *
 * @param Far Scale
 * @desc Scale at depth 100 (default 0.9).
 * @type string
 * @default
 */

/*~struct~Emitter:
 * @param Type
 * @type select
 * @option dust
 * @option motes
 * @option light
 * @option mist
 * @option fog
 * @option rain
 * @option storm
 * @option snow
 * @option ash
 * @option embers
 * @option fireflies
 * @option magic
 * @option leaves
 * @option petals
 * @option sunbeams
 * @default dust
 *
 * @param Amount
 * @type number
 * @min 0
 * @default 20
 *
 * @param Depth Min
 * @desc Blank = type default.
 * @type string
 * @default
 *
 * @param Depth Max
 * @type string
 * @default
 *
 * @param Size
 * @desc Size multiplier (blank = 1).
 * @type string
 * @default
 *
 * @param Speed
 * @type string
 * @default
 *
 * @param Opacity
 * @type string
 * @default
 *
 * @param Wind
 * @desc Extra horizontal speed.
 * @type string
 * @default
 *
 * @param Color
 * @type string
 * @default
 *
 * @param Emissive
 * @type select
 * @option default
 * @value
 * @option yes
 * @value true
 * @option no
 * @value false
 * @default
 */

(() => {
"use strict";

//=============================================================================
// 0. Bootstrap
//-----------------------------------------------------------------------------
// The plugin name is read from the script file name so that the plugin keeps
// working (and its plugin commands keep resolving) if the file is renamed.
//=============================================================================

const PLUGIN_NAME = (() => {
    const script = document.currentScript;
    const src = script && script.src ? script.src : "";
    const match = src.match(/([^/\\]+)\.js(?:\?.*)?$/);
    return match ? decodeURIComponent(match[1]) : "HD2D_Diorama";
})();

const HD2D = (window.HD2D = window.HD2D || {});
HD2D.VERSION = "1.0.0";
HD2D.PLUGIN_NAME = PLUGIN_NAME;

//=============================================================================
// 1. Utilities
//=============================================================================

const U = (HD2D.Utils = {});

U.clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
U.saturate = v => (v < 0 ? 0 : v > 1 ? 1 : v);
U.lerp = (a, b, t) => a + (b - a) * t;
U.smoothstep = (a, b, x) => {
    if (a === b) return x < a ? 0 : 1;
    const t = U.saturate((x - a) / (b - a));
    return t * t * (3 - 2 * t);
};
U.isNum = v => typeof v === "number" && Number.isFinite(v);

/** Parses a number; returns def for blank/invalid input. */
U.num = (v, def) => {
    if (v === undefined || v === null) return def;
    if (typeof v === "number") return Number.isFinite(v) ? v : def;
    const s = String(v).trim();
    if (s === "") return def;
    const n = Number(s);
    return Number.isFinite(n) ? n : def;
};

/** Parses a boolean ("true/on/yes/1" and "false/off/no/0"); returns def otherwise. */
U.bool = (v, def) => {
    if (v === true || v === false) return v;
    if (v === undefined || v === null) return def;
    const s = String(v).trim().toLowerCase();
    if (["true", "on", "yes", "1", "enable", "enabled"].includes(s)) return true;
    if (["false", "off", "no", "0", "disable", "disabled"].includes(s)) return false;
    return def;
};

U.str = (v, def) => (v === undefined || v === null ? def : String(v));

/** Safe JSON parse used for Plugin Manager structs (which are nested JSON strings). */
U.json = (v, def) => {
    if (v === undefined || v === null || v === "") return def;
    if (typeof v !== "string") return v;
    try {
        return JSON.parse(v);
    } catch (e) {
        return def;
    }
};

/** Parses a JSON array of JSON strings (a Plugin Manager struct list). */
U.structList = v => {
    const list = U.json(v, []);
    if (!Array.isArray(list)) return [];
    return list.map(item => U.json(item, null)).filter(item => item && typeof item === "object");
};

/**
 * Parses a color. Accepts "#rgb", "#rrggbb", "r,g,b" (0-255), "rgb(r,g,b)" and
 * arrays. Returns [r, g, b] in 0..1 or def.
 */
U.color = (v, def) => {
    if (v === undefined || v === null) return def;
    if (Array.isArray(v)) {
        if (v.length < 3) return def;
        const big = v[0] > 1 || v[1] > 1 || v[2] > 1;
        return [0, 1, 2].map(i => U.saturate(Number(v[i]) / (big ? 255 : 1)));
    }
    let s = String(v).trim();
    if (s === "") return def;
    const m = s.match(/^rgba?\((.*)\)$/i);
    if (m) s = m[1];
    if (s[0] === "#") {
        let hex = s.slice(1);
        if (hex.length === 3) hex = hex.split("").map(c => c + c).join("");
        if (!/^[0-9a-f]{6}$/i.test(hex)) return def;
        const n = parseInt(hex, 16);
        return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
    }
    const parts = s.split(/[\s,]+/).filter(p => p !== "").map(Number);
    if (parts.length >= 3 && parts.slice(0, 3).every(Number.isFinite)) {
        const big = parts[0] > 1 || parts[1] > 1 || parts[2] > 1;
        return parts.slice(0, 3).map(p => U.saturate(p / (big ? 255 : 1)));
    }
    return def;
};

U.colorHex = c => {
    const h = x => Math.round(U.saturate(x) * 255).toString(16).padStart(2, "0");
    return "#" + h(c[0]) + h(c[1]) + h(c[2]);
};
U.colorInt = c => (Math.round(U.saturate(c[0]) * 255) << 16) | (Math.round(U.saturate(c[1]) * 255) << 8) | Math.round(U.saturate(c[2]) * 255);
U.luma = c => c[0] * 0.299 + c[1] * 0.587 + c[2] * 0.114;
U.isColor = v => Array.isArray(v) && v.length === 3 && v.every(U.isNum);

/**
 * Applies a white-balance style temperature shift to a color.
 * t > 0 warms (more red / less blue), t < 0 cools.
 */
U.temperature = (c, t) => [
    U.saturate(c[0] * (1 + t * 0.35)),
    U.saturate(c[1] * (1 + t * 0.05)),
    U.saturate(c[2] * (1 - t * 0.35))
];

/** Easing curves for transitions. Names are case-insensitive. */
U.EASINGS = {
    linear: t => t,
    smooth: t => t * t * (3 - 2 * t),
    "ease in": t => t * t,
    "ease out": t => 1 - (1 - t) * (1 - t),
    "ease in-out": t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    sine: t => 0.5 - Math.cos(Math.PI * t) / 2,
    "ease out back": t => {
        const c1 = 1.70158;
        const c3 = c1 + 1;
        return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    }
};
U.ease = (name, t) => {
    const key = String(name || "smooth").trim().toLowerCase().replace(/[_]+/g, " ").replace("easeinout", "ease in-out");
    const fn = U.EASINGS[key] || U.EASINGS[key.replace(/-/g, " ")] || U.EASINGS.smooth;
    return fn(U.saturate(t));
};

/** Deterministic hash / 1D value noise (used for light flicker and particles). */
U.hash = n => {
    const s = Math.sin(n * 127.1 + 311.7) * 43758.5453123;
    return s - Math.floor(s);
};
U.noise1 = x => {
    const i = Math.floor(x);
    const f = x - i;
    const u = f * f * (3 - 2 * f);
    return U.lerp(U.hash(i), U.hash(i + 1), u);
};
U.rand = (a, b) => a + Math.random() * (b - a);

U.deepClone = obj => {
    if (Array.isArray(obj)) return obj.map(U.deepClone);
    if (obj && typeof obj === "object") {
        const out = {};
        for (const k of Object.keys(obj)) out[k] = U.deepClone(obj[k]);
        return out;
    }
    return obj;
};

/** Recursively merges src into dst (arrays are replaced, not merged). Returns dst. */
U.deepMerge = (dst, src) => {
    if (!src || typeof src !== "object") return dst;
    for (const k of Object.keys(src)) {
        const v = src[k];
        if (v === undefined) continue;
        if (v && typeof v === "object" && !Array.isArray(v)) {
            if (!dst[k] || typeof dst[k] !== "object" || Array.isArray(dst[k])) dst[k] = {};
            U.deepMerge(dst[k], v);
        } else {
            dst[k] = U.deepClone(v);
        }
    }
    return dst;
};

U.getPath = (obj, path) => {
    let cur = obj;
    for (const key of path.split(".")) {
        if (cur === null || cur === undefined) return undefined;
        cur = cur[key];
    }
    return cur;
};
U.setPath = (obj, path, value) => {
    const keys = path.split(".");
    let cur = obj;
    for (let i = 0; i < keys.length - 1; i++) {
        if (!cur[keys[i]] || typeof cur[keys[i]] !== "object") cur[keys[i]] = {};
        cur = cur[keys[i]];
    }
    cur[keys[keys.length - 1]] = value;
};

/**
 * Parses "key value, key2: value2; key3=value3, positional" style option strings
 * used by note tags. Returns { args: [positional...], opts: {key: value} }.
 */
U.parseOptions = text => {
    const result = { args: [], opts: {} };
    if (text === true || text === undefined || text === null) return result;
    const parts = String(text).split(/[,;]/).map(s => s.trim()).filter(s => s !== "");
    for (const part of parts) {
        const m = part.match(/^([A-Za-z][\w.-]*)\s*(?:[:=]\s*|\s+)(.+)$/);
        if (m && !/^#/.test(part)) {
            result.opts[m[1].toLowerCase()] = m[2].trim();
        } else {
            result.args.push(part);
        }
    }
    return result;
};

/** Parses "1,2, 5-7" into [1,2,5,6,7]. */
U.parseIdList = text => {
    const out = [];
    for (const part of String(text || "").split(/[,\s]+/)) {
        if (!part) continue;
        const range = part.match(/^(\d+)-(\d+)$/);
        if (range) {
            for (let i = Number(range[1]); i <= Number(range[2]); i++) out.push(i);
        } else if (/^\d+$/.test(part)) {
            out.push(Number(part));
        }
    }
    return out;
};

/** Collects all repeated tags <Name: value> from a note string. */
U.noteTags = (note, name) => {
    const out = [];
    if (!note) return out;
    const re = new RegExp("<" + name + "(?:\\s*:\\s*([^>]*))?>", "gi");
    let m;
    while ((m = re.exec(note))) out.push(m[1] === undefined ? true : m[1].trim());
    return out;
};
U.noteTag = (note, name) => {
    const list = U.noteTags(note, name);
    return list.length ? list[list.length - 1] : undefined;
};

/** Logs a warning only once per key. */
const warned = new Set();
U.warnOnce = (key, ...args) => {
    if (warned.has(key)) return;
    warned.add(key);
    console.warn("[HD2D] " + key, ...args);
};

U.isPlaytest = () => {
    try {
        return !!($gameTemp && $gameTemp.isPlaytest());
    } catch (e) {
        return false;
    }
};

U.renderer = () => (Graphics.app ? Graphics.app.renderer : null);

/** Column-major mat3 from a 2D affine transform (a, b, c, d, tx, ty). */
U.mat3 = (out, a, b, c, d, tx, ty) => {
    out[0] = a;
    out[1] = b;
    out[2] = 0;
    out[3] = c;
    out[4] = d;
    out[5] = 0;
    out[6] = tx;
    out[7] = ty;
    out[8] = 1;
    return out;
};
U.mat3FromPixi = (out, m) => U.mat3(out, m.a, m.b, m.c, m.d, m.tx, m.ty);

//=============================================================================
// 2. Plugin parameters
//=============================================================================

const RAW = PluginManager.parameters(PLUGIN_NAME);

const EFFECT_KEYS = [
    "depth", "parallax", "dof", "bokeh", "lighting", "shadows", "ambient", "bloom", "grade",
    "vignette", "fog", "particles", "normalMaps", "rim", "atmosphere", "camera", "emissive",
    "perspective", "weather"
];

// Accepted spellings for effect names in commands, notetags and parameters.
const EFFECT_ALIASES = {
    depth: "depth", "depth system": "depth", "simulated depth": "depth",
    parallax: "parallax",
    dof: "dof", "depth of field": "dof",
    bokeh: "bokeh",
    lighting: "lighting", lights: "lighting", "2d lighting": "lighting", "dynamic lighting": "lighting",
    shadows: "shadows", shadow: "shadows",
    ambient: "ambient", "ambient lighting": "ambient",
    bloom: "bloom", glow: "bloom",
    grade: "grade", "color grading": "grade", "colour grading": "grade", grading: "grade",
    vignette: "vignette",
    fog: "fog", mist: "fog",
    particles: "particles",
    "normal maps": "normalMaps", normalmaps: "normalMaps", normals: "normalMaps",
    rim: "rim", "rim light": "rim", "rim lighting": "rim",
    atmosphere: "atmosphere", "atmospheric perspective": "atmosphere",
    camera: "camera", "camera effects": "camera",
    emissive: "emissive",
    perspective: "perspective", "perspective scaling": "perspective",
    weather: "weather", "depth weather": "weather"
};
HD2D.effectKey = name => EFFECT_ALIASES[String(name || "").trim().toLowerCase()] || null;

const P = (HD2D.Params = (() => {
    const p = {};
    p.defaultPreset = U.str(RAW["Default Preset"], "HD2D").trim() || "HD2D";
    p.quality = U.str(RAW["Quality"], "Medium").trim();
    p.adaptiveQuality = U.bool(RAW["Adaptive Quality"], false);
    const toggles = U.json(RAW["Effects"], {}) || {};
    p.toggles = {};
    const toggleNames = {
        depth: "Depth System", parallax: "Parallax", dof: "Depth Of Field", bokeh: "Bokeh",
        lighting: "Lighting", shadows: "Shadows", ambient: "Ambient Lighting", bloom: "Bloom",
        grade: "Color Grading", vignette: "Vignette", fog: "Fog", particles: "Particles",
        normalMaps: "Normal Maps", rim: "Rim Lighting", atmosphere: "Atmospheric Perspective",
        camera: "Camera Effects", emissive: "Emissive", perspective: "Perspective Scaling",
        weather: "Depth Weather"
    };
    for (const key of EFFECT_KEYS) p.toggles[key] = U.bool(toggles[toggleNames[key]], true);
    p.pixelPerfect = U.bool(RAW["Pixel Perfect Mode"], true);
    p.roundPixels = U.bool(RAW["Round Pixels"], true);
    p.mapTransitionFrames = Math.max(0, U.num(RAW["Map Transition Frames"], 40));
    p.keepOverrides = U.bool(RAW["Keep Overrides On Transfer"], false);
    p.postOnPictures = U.bool(RAW["Post FX On Pictures"], false);
    p.tausiMode = U.str(RAW["TausiLighting Compatibility"], "Auto").trim().toLowerCase();

    p.regionDepths = {};
    for (const s of U.structList(RAW["Region Depths"])) {
        const id = U.num(s["Region"], 0);
        if (id > 0) p.regionDepths[id] = U.clamp(U.num(s["Depth"], 50), 0, 100);
    }
    p.regionEmissive = {};
    for (const s of U.structList(RAW["Region Emissive"])) {
        const id = U.num(s["Region"], 0);
        if (id > 0) p.regionEmissive[id] = U.clamp(U.num(s["Strength"], 1), 0, 4);
    }
    p.characterRegionDepth = U.bool(RAW["Character Region Depth"], true);
    p.sortByDepth = U.bool(RAW["Sort Characters By Depth"], false);

    p.blockRegions = U.parseIdList(RAW["Light Blocking Regions"]);
    p.blockTerrainTags = U.parseIdList(RAW["Light Blocking Terrain Tags"]);
    p.wallsBlockLight = U.bool(RAW["Wall Tiles Block Light"], false);
    p.objectShadows = U.bool(RAW["Object Characters Cast Shadows"], false);

    p.smoothCamera = U.bool(RAW["Smooth Camera"], true);
    p.cameraSpeed = U.clamp(U.num(RAW["Camera Follow Speed"], 0.14), 0.01, 1);
    p.minZoom = U.clamp(U.num(RAW["Min Zoom"], 0.5), 0.25, 1);
    p.maxZoom = Math.max(1, U.num(RAW["Max Zoom"], 3));
    p.rotationOverscan = U.bool(RAW["Rotation Overscan"], true);
    p.zoomDofInfluence = U.clamp(U.num(RAW["Zoom DOF Influence"], 0.5), 0, 2);

    p.normalSuffix = U.str(RAW["Normal Map Suffix"], "_normal");
    p.autoNormalMaps = U.bool(RAW["Auto-Detect Normal Maps"], false);
    p.lightHeight = Math.max(1, U.num(RAW["Light Height"], 64));
    p.unlitAnimations = U.bool(RAW["Animations Unlit"], true);

    p.particleDensity = U.clamp(U.num(RAW["Particle Density"], 1), 0, 4);

    p.timeMode = U.str(RAW["Time Of Day Mode"], "Off").trim().toLowerCase();
    p.hourVariable = U.num(RAW["Hour Variable"], 0);
    p.minuteVariable = U.num(RAW["Minute Variable"], 0);
    p.timePhases = U.structList(RAW["Time Phases"]);

    p.customPresets = U.structList(RAW["Custom Presets"]);

    p.battleEffects = U.bool(RAW["Battle Effects"], true);
    p.battlePreset = U.str(RAW["Battle Preset"], "").trim();
    p.battleBlur = U.clamp(U.num(RAW["Battle Background Blur"], 0.5), 0, 4);

    p.debugMode = U.str(RAW["Debug Mode"], "Playtest").trim().toLowerCase();
    p.debugOverlayKey = U.str(RAW["Debug Overlay Key"], "F6").trim().toUpperCase();
    p.debugViewKey = U.str(RAW["Debug View Key"], "F7").trim().toUpperCase();
    return p;
})());


//=============================================================================
// 3. Visual state schema, built-in presets, quality levels, time of day
//-----------------------------------------------------------------------------
// A "visual state" is a plain object describing every tunable of every system.
// Presets are partial states merged over DEFAULT_STATE (which is the "HD2D"
// look). Every section has an "enabled" flag; at runtime each section also
// gets a "weight" (0..1) so that effects can fade in and out smoothly when a
// preset transition switches them on or off.
//
// Depth scale used everywhere: 0 = closest to the camera (foreground),
// 50 = gameplay / focal plane, 100 = farthest background.
//=============================================================================

const DEFAULT_STATE = {
    timeOfDay: true,
    depth: {
        enabled: true,
        autoY: true, // derive depth from the vertical screen position
        focalDepth: 50, // depth of the gameplay plane
        nearDepth: 30, // depth at the bottom edge of the screen
        farDepth: 85, // depth at the top edge of the screen
        focalY: 0.56, // screen position (0 = top, 1 = bottom) of the focal plane
        followPlayer: true, // keep the focal plane on the player's feet
        curve: 1.4, // >1 = flat around the focal plane, steeper at the edges
        strength: 1, // scales the whole auto-depth deviation
        upperTileOffset: -4, // upper-layer ("star") tiles are this much closer
        backgroundDepth: 96 // depth of empty map areas showing a background layer
    },
    parallax: {
        enabled: true,
        foregroundBoost: 0.25, // extra speed for layers in front of the focal plane
        farFactor: 0.1, // scroll factor of a layer at depth 100
        curve: 0.8, // shape of the depth -> scroll factor curve
        zoomInfluence: 1 // how much far layers follow the camera zoom
    },
    dof: {
        enabled: true,
        focus: 50, // focus depth
        focusRange: 7, // +/- depth range that stays perfectly sharp
        nearTransition: 20, // depth range over which near blur ramps up
        farTransition: 30, // depth range over which far blur ramps up
        nearBlur: 0.85, // max near (foreground) blur 0..1
        farBlur: 1, // max far (background) blur 0..1
        strength: 1, // global multiplier
        radius: 4.5 // max blur radius in screen pixels
    },
    bokeh: {
        enabled: true,
        intensity: 0.5,
        size: 1,
        threshold: 0.78, // luminance above which blurred highlights become discs
        quality: "auto", // auto / low / medium / high
        maxCount: 64 // max highlight discs (sprite-based bokeh)
    },
    atmosphere: {
        enabled: true,
        hazeColor: [0.78, 0.83, 0.9],
        hazeAmount: 0.12,
        farDesaturate: 0.18,
        farContrast: 0.15,
        farBrighten: 0.03,
        farTemperature: -0.04,
        nearSaturate: 0.08,
        nearContrast: 0.08,
        nearDarken: 0.05
    },
    ambient: {
        enabled: true,
        color: [0.96, 0.97, 1.0],
        intensity: 0.8,
        temperature: 0,
        shadowTint: [0.62, 0.68, 0.9],
        shadowTintAmount: 0.22,
        highlightTint: [1.0, 0.95, 0.85],
        highlightTintAmount: 0.12
    },
    sun: {
        enabled: true,
        angle: 240, // direction the light comes FROM (0 right, 90 bottom, 180 left, 270 top)
        elevation: 55, // 90 = straight above (short shadows), low = long shadows
        intensity: 0.25,
        color: [1.0, 0.95, 0.86]
    },
    lights: {
        enabled: true,
        intensity: 1, // multiplier for all point / spot lights
        color: [1, 1, 1], // tint for all lights (used by time of day)
        dayFade: 0.5, // lights fade by this much in bright ambient light
        glow: 0.35 // soft additive glow drawn around light sources
    },
    shadows: {
        enabled: true,
        opacity: 0.45, // character shadow strength
        length: 0.6, // character shadow length multiplier
        softness: 1, // blur of the shadow mask
        contact: 0.35, // dark contact shadow under characters
        lightShadows: true, // characters also cast shadows from point lights
        occlusion: 0.85 // strength of tile shadows (light blocking walls)
    },
    fog: {
        enabled: true,
        color: [0.87, 0.9, 0.95],
        lit: 0.75, // how much the fog is affected by ambient light and lights
        softness: 10, // depth range over which a fog layer fades in
        noise: 0.6, // 0 = flat fog, 1 = very patchy
        depthFog: 0, // extra exponential haze for deep background
        nearOpacity: 0,
        nearDepth: 18,
        nearScale: 0.8,
        nearSpeedX: 0.3,
        nearSpeedY: 0.04,
        midOpacity: 0,
        midDepth: 56,
        midScale: 1,
        midSpeedX: 0.16,
        midSpeedY: 0.02,
        farOpacity: 0.12,
        farDepth: 72,
        farScale: 1.3,
        farSpeedX: 0.08,
        farSpeedY: 0.01
    },
    bloom: {
        enabled: true,
        threshold: 0.74,
        knee: 0.18,
        intensity: 0.35,
        radius: 1,
        emissive: 1 // bloom multiplier for emissive objects
    },
    grade: {
        enabled: true,
        exposure: 0, // stops
        contrast: 1.05,
        saturation: 1.06,
        brightness: 0,
        gamma: 1,
        hue: 0, // degrees
        temperature: 0.03,
        tint: 0, // + magenta / - green
        shadowColor: [0.3, 0.36, 0.62],
        shadowAmount: 0.08,
        highlightColor: [1.0, 0.88, 0.72],
        highlightAmount: 0.06,
        lut: "", // optional LUT image in img/pictures (256x16 or 1024x32 strip)
        lutStrength: 1
    },
    vignette: {
        enabled: true,
        intensity: 0.25,
        radius: 0.78,
        softness: 0.45,
        color: [0.03, 0.02, 0.05],
        pulse: 0, // animated intensity amplitude
        pulseSpeed: 1
    },
    rim: {
        enabled: true,
        color: [1.0, 0.94, 0.84],
        intensity: 0.3,
        width: 1.5, // pixels
        angle: 240, // light direction (same convention as sun.angle)
        followSun: true
    },
    perspective: {
        enabled: false, // depth-based scaling of characters (off by default)
        nearScale: 1.08,
        farScale: 0.9
    },
    particles: [{ type: "motes", amount: 16 }]
};

// Built-in presets: partial states merged over DEFAULT_STATE.
const BUILTIN_PRESETS = {
    HD2D: {},
    Vanilla: {
        depth: { enabled: false }, dof: { enabled: false }, bokeh: { enabled: false },
        atmosphere: { enabled: false }, ambient: { enabled: false }, sun: { enabled: false },
        lights: { enabled: false }, shadows: { enabled: false }, fog: { enabled: false },
        bloom: { enabled: false }, grade: { enabled: false }, vignette: { enabled: false },
        rim: { enabled: false }, particles: []
    },
    Forest: {
        ambient: { color: "#eef6e6", intensity: 0.78, shadowTint: "#8fa8c0", shadowTintAmount: 0.28 },
        sun: { intensity: 0.3, color: "#fff2cc", angle: 235, elevation: 50 },
        dof: { radius: 5 },
        fog: { color: "#d8e6d4", midOpacity: 0.08, farOpacity: 0.3, noise: 0.7 },
        atmosphere: { hazeColor: "#cfdccf", hazeAmount: 0.2 },
        bloom: { intensity: 0.4, threshold: 0.72 },
        grade: { temperature: 0.02, tint: -0.03, saturation: 1.1, shadowColor: "#2e4a40", shadowAmount: 0.12 },
        particles: [{ type: "motes", amount: 20 }, { type: "leaves", amount: 6 }, { type: "sunbeams", amount: 4 }]
    },
    Town: {
        ambient: { color: "#fff8ee", intensity: 0.82 },
        sun: { intensity: 0.27 },
        dof: { radius: 4 },
        fog: { farOpacity: 0.14 },
        grade: { temperature: 0.05, saturation: 1.08, contrast: 1.06 },
        particles: [{ type: "dust", amount: 12 }]
    },
    Dungeon: {
        timeOfDay: false,
        ambient: { color: "#6466a8", intensity: 0.32, shadowTint: "#5a4a9a", shadowTintAmount: 0.3 },
        sun: { enabled: false },
        lights: { intensity: 1.15, dayFade: 0, glow: 0.5 },
        shadows: { contact: 0.45 },
        fog: { color: "#3c3c62", midOpacity: 0.12, farOpacity: 0.35, farDepth: 66, lit: 0.9 },
        atmosphere: { hazeColor: "#2a2a44", hazeAmount: 0.25, farBrighten: 0 },
        bloom: { threshold: 0.6, intensity: 0.5 },
        grade: { temperature: -0.06, saturation: 0.9, contrast: 1.1, exposure: 0.1 },
        vignette: { intensity: 0.42, radius: 0.68 },
        rim: { color: "#c8c0ff", intensity: 0.35 },
        particles: [{ type: "dust", amount: 22 }]
    },
    Cave: {
        timeOfDay: false,
        ambient: { color: "#7a6a5a", intensity: 0.3 },
        sun: { enabled: false },
        lights: { intensity: 1.2, dayFade: 0, glow: 0.5 },
        fog: { color: "#3a3028", midOpacity: 0.1, farOpacity: 0.4, farDepth: 64 },
        atmosphere: { hazeColor: "#2a2420", hazeAmount: 0.25, farBrighten: 0 },
        bloom: { threshold: 0.6, intensity: 0.45 },
        grade: { temperature: 0.06, saturation: 0.85, contrast: 1.12, exposure: 0.08 },
        vignette: { intensity: 0.5, radius: 0.64 },
        particles: [{ type: "dust", amount: 18 }]
    },
    Interior: {
        timeOfDay: false,
        ambient: { color: "#fff2e0", intensity: 0.74 },
        sun: { enabled: false },
        lights: { dayFade: 0.3 },
        dof: { radius: 3.5, farBlur: 0.8 },
        fog: { farOpacity: 0.05 },
        vignette: { intensity: 0.3 },
        particles: [{ type: "dust", amount: 10 }]
    },
    Night: {
        ambient: { color: "#4e62a6", intensity: 0.38, shadowTint: "#4050a0", shadowTintAmount: 0.3, highlightTint: "#ffe2b0" },
        sun: { color: "#a8bcff", intensity: 0.12, angle: 250, elevation: 60 },
        lights: { intensity: 1.2, dayFade: 0, glow: 0.55 },
        fog: { color: "#2e3c62", farOpacity: 0.3, lit: 0.9 },
        atmosphere: { hazeColor: "#22304e", hazeAmount: 0.2, farBrighten: 0 },
        bloom: { threshold: 0.6, intensity: 0.55 },
        grade: { temperature: -0.1, saturation: 0.85, contrast: 1.08 },
        vignette: { intensity: 0.38 },
        rim: { color: "#bcd0ff", intensity: 0.4 },
        particles: [{ type: "fireflies", amount: 16 }]
    },
    Sunset: {
        ambient: { color: "#ffb88a", intensity: 0.72 },
        sun: { color: "#ff9a4a", intensity: 0.36, angle: 195, elevation: 16 },
        fog: { color: "#f0a888", farOpacity: 0.3 },
        atmosphere: { hazeColor: "#f0b090", hazeAmount: 0.22 },
        bloom: { intensity: 0.5, threshold: 0.66 },
        grade: { temperature: 0.14, saturation: 1.08, highlightColor: "#ffb070", highlightAmount: 0.12 },
        rim: { color: "#ffb070", intensity: 0.45 },
        particles: [{ type: "motes", amount: 18 }]
    },
    Snow: {
        ambient: { color: "#eaf0ff", intensity: 0.86 },
        sun: { color: "#f4f8ff", intensity: 0.22 },
        fog: { color: "#e8eef8", midOpacity: 0.08, farOpacity: 0.36 },
        atmosphere: { hazeColor: "#e0e8f4", hazeAmount: 0.24 },
        grade: { temperature: -0.08, saturation: 0.92, exposure: 0.05 },
        bloom: { threshold: 0.82, intensity: 0.3 },
        particles: [{ type: "snow", amount: 60 }]
    },
    Dream: {
        dof: { radius: 6, focusRange: 4 },
        fog: { color: "#e8d8ff", midOpacity: 0.15 },
        bloom: { threshold: 0.5, intensity: 0.75, radius: 1.4 },
        grade: {
            saturation: 0.85, contrast: 0.92, exposure: 0.15, hue: 10,
            highlightColor: "#ffd6f4", highlightAmount: 0.2, shadowColor: "#6a5aa8", shadowAmount: 0.2
        },
        vignette: { color: "#2a1a40", intensity: 0.4 },
        particles: [{ type: "magic", amount: 30 }, { type: "motes", amount: 20 }]
    },
    Dark: {
        ambient: { color: "#5e5470", intensity: 0.46 },
        sun: { intensity: 0.1 },
        fog: { color: "#201820", farOpacity: 0.4 },
        bloom: { intensity: 0.25 },
        grade: { exposure: -0.15, saturation: 0.7, contrast: 1.15 },
        vignette: { intensity: 0.55, radius: 0.6 },
        particles: [{ type: "ash", amount: 24 }]
    }
};

// Color-grade looks usable with the "Set Color Grade" command.
const GRADE_PRESETS = {
    Default: {},
    Neutral: { exposure: 0, contrast: 1, saturation: 1, brightness: 0, gamma: 1, hue: 0, temperature: 0, tint: 0, shadowAmount: 0, highlightAmount: 0 },
    Warm: { temperature: 0.12, saturation: 1.08, highlightColor: "#ffd2a0", highlightAmount: 0.1 },
    Cold: { temperature: -0.12, saturation: 0.92, shadowColor: "#304a80", shadowAmount: 0.15 },
    Night: { temperature: -0.1, saturation: 0.85, contrast: 1.08, exposure: -0.05 },
    Sunset: { temperature: 0.14, saturation: 1.08, highlightColor: "#ffb070", highlightAmount: 0.12 },
    Dungeon: { temperature: -0.06, saturation: 0.9, contrast: 1.1, shadowColor: "#3a2a6a", shadowAmount: 0.15 },
    Dream: { saturation: 0.85, contrast: 0.92, exposure: 0.15, hue: 10, highlightColor: "#ffd6f4", highlightAmount: 0.2, shadowColor: "#6a5aa8", shadowAmount: 0.2 },
    Dark: { exposure: -0.15, saturation: 0.7, contrast: 1.15 },
    Sepia: { saturation: 0.25, temperature: 0.2, contrast: 1.05, highlightColor: "#ffe0b0", highlightAmount: 0.15, shadowColor: "#4a3020", shadowAmount: 0.2 },
    Vivid: { saturation: 1.25, contrast: 1.1 }
};

// Quality levels. Every expensive feature is scaled here.
const QUALITY = {
    low: {
        name: "Low", objScale: 0.5, lightScale: 0.25, shadowScale: 0.25, dofScale: 0.25, dofTaps: 12,
        bokehScatter: 0, bloomLevels: 2, bloomScale: 0.25, shadowMode: 1, occlusionSteps: 0, maxLights: 8,
        particleMult: 0.4, fogLayers: 1, noiseOctaves: 1, normalMaps: false
    },
    medium: {
        name: "Medium", objScale: 1, lightScale: 0.5, shadowScale: 0.5, dofScale: 0.5, dofTaps: 20,
        bokehScatter: 0.5, bloomLevels: 3, bloomScale: 0.5, shadowMode: 2, occlusionSteps: 0, maxLights: 16,
        particleMult: 0.7, fogLayers: 2, noiseOctaves: 2, normalMaps: false
    },
    high: {
        name: "High", objScale: 1, lightScale: 0.5, shadowScale: 0.5, dofScale: 0.5, dofTaps: 32,
        bokehScatter: 1, bloomLevels: 4, bloomScale: 0.5, shadowMode: 3, occlusionSteps: 14, maxLights: 24,
        particleMult: 1, fogLayers: 3, noiseOctaves: 2, normalMaps: true
    },
    ultra: {
        name: "Ultra", objScale: 1, lightScale: 1, shadowScale: 0.5, dofScale: 0.5, dofTaps: 48,
        bokehScatter: 1.5, bloomLevels: 5, bloomScale: 0.5, shadowMode: 4, occlusionSteps: 28, maxLights: 32,
        particleMult: 1.5, fogLayers: 3, noiseOctaves: 3, normalMaps: true
    }
};
const QUALITY_ORDER = ["low", "medium", "high", "ultra"];
HD2D.QUALITY = QUALITY;

// Bokeh quality presets (used when bokeh.quality is not "auto").
const BOKEH_QUALITY = {
    low: { taps: 12, scatter: 0 },
    medium: { taps: 24, scatter: 0.5 },
    high: { taps: 40, scatter: 1 }
};

// Time-of-day phases. They are *modifiers* applied over the map's preset:
// tints multiply colors (white = unchanged), multipliers scale values.
const BUILTIN_TIME_PHASES = [
    {
        name: "Dawn", hour: 5.5, ambientTint: "#c8bcf0", ambientMult: 0.75, sunTint: "#ffbca4", sunMult: 0.8,
        sunAngle: 330, sunElevation: 12, exposure: -0.03, temperature: -0.02, saturation: 0.95, contrast: 1,
        fogTint: "#eed8f0", fogMult: 1.5, bloomMult: 1.15, lightMult: 0.9, lightTint: "#ffd8b8", dofMult: 1,
        vignetteMult: 1.05, particles: "motes", particleAmount: 10
    },
    {
        name: "Morning", hour: 8, ambientTint: "#f8f8ff", ambientMult: 0.95, sunTint: "#fff2dc", sunMult: 1,
        sunAngle: 300, sunElevation: 35, exposure: 0, temperature: 0.01, saturation: 1, contrast: 1,
        fogTint: "#ffffff", fogMult: 1.15, bloomMult: 1, lightMult: 0.55, lightTint: "#ffffff", dofMult: 1,
        vignetteMult: 1, particles: "", particleAmount: 0
    },
    {
        name: "Day", hour: 12, ambientTint: "#ffffff", ambientMult: 1, sunTint: "#ffffff", sunMult: 1,
        sunAngle: 260, sunElevation: 62, exposure: 0, temperature: 0, saturation: 1, contrast: 1,
        fogTint: "#ffffff", fogMult: 1, bloomMult: 1, lightMult: 0.35, lightTint: "#ffffff", dofMult: 1,
        vignetteMult: 1, particles: "", particleAmount: 0
    },
    {
        name: "Afternoon", hour: 15.5, ambientTint: "#fff6ea", ambientMult: 1, sunTint: "#fff0d8", sunMult: 1,
        sunAngle: 225, sunElevation: 45, exposure: 0, temperature: 0.03, saturation: 1, contrast: 1,
        fogTint: "#ffffff", fogMult: 1, bloomMult: 1, lightMult: 0.45, lightTint: "#ffffff", dofMult: 1,
        vignetteMult: 1, particles: "", particleAmount: 0
    },
    {
        name: "Sunset", hour: 18, ambientTint: "#ffd2ac", ambientMult: 0.85, sunTint: "#ffae6a", sunMult: 1.2,
        sunAngle: 195, sunElevation: 14, exposure: 0.02, temperature: 0.09, saturation: 1.03, contrast: 1.02,
        fogTint: "#ffc0a0", fogMult: 1.3, bloomMult: 1.35, lightMult: 0.85, lightTint: "#ffc898", dofMult: 1,
        vignetteMult: 1.1, particles: "motes", particleAmount: 12
    },
    {
        name: "Evening", hour: 19.5, ambientTint: "#9a8ad0", ambientMult: 0.62, sunTint: "#c8a8ff", sunMult: 0.45,
        sunAngle: 180, sunElevation: 8, exposure: -0.02, temperature: -0.04, saturation: 0.9, contrast: 1.02,
        fogTint: "#9080b8", fogMult: 1.25, bloomMult: 1.3, lightMult: 1.05, lightTint: "#ffd8a8", dofMult: 1.05,
        vignetteMult: 1.15, particles: "", particleAmount: 0
    },
    {
        name: "Night", hour: 22.5, ambientTint: "#6078c8", ambientMult: 0.45, sunTint: "#a8bcff", sunMult: 0.45,
        sunAngle: 250, sunElevation: 58, exposure: 0, temperature: -0.1, saturation: 0.82, contrast: 1.04,
        fogTint: "#4a5a8a", fogMult: 1.2, bloomMult: 1.45, lightMult: 1.25, lightTint: "#ffe0b0", dofMult: 1.1,
        vignetteMult: 1.25, particles: "fireflies", particleAmount: 14
    }
];

//-----------------------------------------------------------------------------
// Value conversion helpers driven by DEFAULT_STATE types.
//-----------------------------------------------------------------------------

/** Converts a raw (string) value to the type of DEFAULT_STATE at path. */
HD2D.convertValue = (path, raw) => {
    const ref = U.getPath(DEFAULT_STATE, path);
    if (path.endsWith(".weight")) return U.num(raw, null);
    if (ref === undefined) return null;
    if (U.isColor(ref)) return U.color(raw, null);
    if (typeof ref === "boolean") return U.bool(raw, null);
    if (typeof ref === "number") return U.num(raw, null);
    if (typeof ref === "string") return raw === undefined || raw === null ? null : String(raw).trim();
    return null;
};

/** Normalizes a partial preset written by hand (colors as strings etc.). */
const normalizePartial = (partial, prefix = "") => {
    const out = Array.isArray(partial) ? [] : {};
    for (const key of Object.keys(partial || {})) {
        const v = partial[key];
        const path = prefix ? prefix + "." + key : key;
        if (key === "particles") {
            out[key] = Array.isArray(v) ? v.map(e => Object.assign({}, e)) : [];
        } else if (v && typeof v === "object" && !Array.isArray(v)) {
            out[key] = normalizePartial(v, path);
        } else {
            const conv = HD2D.convertValue(path, v);
            if (conv !== null && conv !== undefined) out[key] = conv;
        }
    }
    return out;
};

/** Parses "a.b=1, c.d = #fff; e.f=true" into a partial state object. */
HD2D.parseSettingsString = text => {
    const out = {};
    if (!text || text === true) return out;
    for (const part of String(text).split(/[,;\n]/)) {
        const m = part.match(/^\s*([A-Za-z][\w.]*)\s*[=:]\s*(.+?)\s*$/);
        if (!m) continue;
        const path = m[1].replace(/^(\w)/, c => c.toLowerCase());
        const value = HD2D.convertValue(path, m[2]);
        if (value === null || value === undefined) {
            U.warnOnce("Unknown setting '" + m[1] + "'");
            continue;
        }
        U.setPath(out, path, value);
    }
    return out;
};

//-----------------------------------------------------------------------------
// Plugin Manager preset structs -> partial states.
// Every struct field left blank inherits from the base preset.
//-----------------------------------------------------------------------------

const PRESET_FIELD_MAP = {
    "Depth": {
        "Enabled": "depth.enabled", "Auto Y Depth": "depth.autoY", "Focal Depth": "depth.focalDepth",
        "Near Depth (Bottom)": "depth.nearDepth", "Far Depth (Top)": "depth.farDepth", "Focal Y": "depth.focalY",
        "Focus Follows Player": "depth.followPlayer", "Depth Curve": "depth.curve", "Depth Strength": "depth.strength",
        "Upper Tile Offset": "depth.upperTileOffset", "Background Depth": "depth.backgroundDepth"
    },
    "Parallax": {
        "Enabled": "parallax.enabled", "Foreground Boost": "parallax.foregroundBoost", "Far Factor": "parallax.farFactor",
        "Curve": "parallax.curve", "Zoom Influence": "parallax.zoomInfluence"
    },
    "Depth Of Field": {
        "Enabled": "dof.enabled", "Focus Depth": "dof.focus", "Focus Range": "dof.focusRange",
        "Near Transition": "dof.nearTransition", "Far Transition": "dof.farTransition", "Near Blur": "dof.nearBlur",
        "Far Blur": "dof.farBlur", "Blur Strength": "dof.strength", "Blur Radius": "dof.radius"
    },
    "Bokeh": {
        "Enabled": "bokeh.enabled", "Intensity": "bokeh.intensity", "Size": "bokeh.size", "Threshold": "bokeh.threshold",
        "Quality": "bokeh.quality", "Max Count": "bokeh.maxCount"
    },
    "Atmosphere": {
        "Enabled": "atmosphere.enabled", "Haze Color": "atmosphere.hazeColor", "Haze Amount": "atmosphere.hazeAmount",
        "Far Desaturate": "atmosphere.farDesaturate", "Far Contrast": "atmosphere.farContrast",
        "Far Brighten": "atmosphere.farBrighten", "Far Temperature": "atmosphere.farTemperature",
        "Near Saturate": "atmosphere.nearSaturate", "Near Contrast": "atmosphere.nearContrast", "Near Darken": "atmosphere.nearDarken"
    },
    "Ambient": {
        "Enabled": "ambient.enabled", "Color": "ambient.color", "Intensity": "ambient.intensity",
        "Temperature": "ambient.temperature", "Shadow Tint": "ambient.shadowTint", "Shadow Tint Amount": "ambient.shadowTintAmount",
        "Highlight Tint": "ambient.highlightTint", "Highlight Tint Amount": "ambient.highlightTintAmount"
    },
    "Sun": {
        "Enabled": "sun.enabled", "Angle": "sun.angle", "Elevation": "sun.elevation", "Intensity": "sun.intensity", "Color": "sun.color"
    },
    "Lights": {
        "Enabled": "lights.enabled", "Intensity": "lights.intensity", "Color": "lights.color",
        "Day Fade": "lights.dayFade", "Glow": "lights.glow"
    },
    "Shadows": {
        "Enabled": "shadows.enabled", "Opacity": "shadows.opacity", "Length": "shadows.length",
        "Softness": "shadows.softness", "Contact Shadow": "shadows.contact", "Light Shadows": "shadows.lightShadows",
        "Tile Occlusion": "shadows.occlusion"
    },
    "Fog": {
        "Enabled": "fog.enabled", "Color": "fog.color", "Lit": "fog.lit", "Softness": "fog.softness", "Noise": "fog.noise",
        "Depth Fog": "fog.depthFog",
        "Near Opacity": "fog.nearOpacity", "Near Depth": "fog.nearDepth", "Near Scale": "fog.nearScale",
        "Near Speed X": "fog.nearSpeedX", "Near Speed Y": "fog.nearSpeedY",
        "Mid Opacity": "fog.midOpacity", "Mid Depth": "fog.midDepth", "Mid Scale": "fog.midScale",
        "Mid Speed X": "fog.midSpeedX", "Mid Speed Y": "fog.midSpeedY",
        "Far Opacity": "fog.farOpacity", "Far Depth": "fog.farDepth", "Far Scale": "fog.farScale",
        "Far Speed X": "fog.farSpeedX", "Far Speed Y": "fog.farSpeedY"
    },
    "Bloom": {
        "Enabled": "bloom.enabled", "Threshold": "bloom.threshold", "Knee": "bloom.knee", "Intensity": "bloom.intensity",
        "Radius": "bloom.radius", "Emissive Boost": "bloom.emissive"
    },
    "Color Grading": {
        "Enabled": "grade.enabled", "Exposure": "grade.exposure", "Contrast": "grade.contrast",
        "Saturation": "grade.saturation", "Brightness": "grade.brightness", "Gamma": "grade.gamma", "Hue": "grade.hue",
        "Temperature": "grade.temperature", "Tint": "grade.tint", "Shadow Color": "grade.shadowColor",
        "Shadow Amount": "grade.shadowAmount", "Highlight Color": "grade.highlightColor",
        "Highlight Amount": "grade.highlightAmount", "LUT": "grade.lut", "LUT Strength": "grade.lutStrength"
    },
    "Vignette": {
        "Enabled": "vignette.enabled", "Intensity": "vignette.intensity", "Radius": "vignette.radius",
        "Softness": "vignette.softness", "Color": "vignette.color", "Pulse": "vignette.pulse", "Pulse Speed": "vignette.pulseSpeed"
    },
    "Rim Light": {
        "Enabled": "rim.enabled", "Color": "rim.color", "Intensity": "rim.intensity", "Width": "rim.width",
        "Angle": "rim.angle", "Follow Sun": "rim.followSun"
    },
    "Perspective": {
        "Enabled": "perspective.enabled", "Near Scale": "perspective.nearScale", "Far Scale": "perspective.farScale"
    }
};

const parseEmitterStruct = s => {
    const e = { type: U.str(s["Type"], "dust").trim().toLowerCase() || "dust" };
    const num = (label, key) => {
        const v = U.num(s[label], null);
        if (v !== null) e[key] = v;
    };
    num("Amount", "amount");
    num("Depth Min", "depthMin");
    num("Depth Max", "depthMax");
    num("Size", "size");
    num("Speed", "speed");
    num("Opacity", "opacity");
    num("Wind", "wind");
    const color = U.color(s["Color"], null);
    if (color) e.color = color;
    const emissive = U.bool(s["Emissive"], null);
    if (emissive !== null) e.emissive = emissive;
    return e;
};

const parsePresetStruct = s => {
    const partial = {};
    for (const group of Object.keys(PRESET_FIELD_MAP)) {
        const sub = U.json(s[group], null);
        if (!sub || typeof sub !== "object") continue;
        for (const label of Object.keys(PRESET_FIELD_MAP[group])) {
            const raw = sub[label];
            if (raw === undefined || raw === null || String(raw).trim() === "" || String(raw).trim().toLowerCase() === "inherit") continue;
            const path = PRESET_FIELD_MAP[group][label];
            const value = HD2D.convertValue(path, raw);
            if (value !== null) U.setPath(partial, path, value);
        }
    }
    const tod = U.bool(s["Uses Time Of Day"], null);
    if (tod !== null) partial.timeOfDay = tod;
    const emitters = U.structList(s["Particles"]).map(parseEmitterStruct);
    // Particle Mode: Inherit (listed emitters replace the base list, an empty
    // list keeps it), Replace, Add (append to the base list) or None.
    const mode = U.str(s["Particle Mode"], "Inherit").trim().toLowerCase();
    if (mode === "none") partial.particles = [];
    else if (mode === "add") {
        if (emitters.length) partial.__addParticles = emitters;
    } else if (mode === "replace" || emitters.length) partial.particles = emitters;
    U.deepMerge(partial, HD2D.parseSettingsString(s["Extra Settings"]));
    return partial;
};

//-----------------------------------------------------------------------------
// Preset registry
//-----------------------------------------------------------------------------

const Presets = (HD2D.Presets = {
    _defs: {}, // name(lowercase) -> { name, base, partial }
    _cache: {},

    register(name, partial, base) {
        const key = String(name).trim().toLowerCase();
        if (!key) return;
        this._defs[key] = { name: String(name).trim(), base: base ? String(base).trim() : "", partial: partial || {} };
        this._cache = {};
    },

    has(name) {
        return !!this._defs[String(name || "").trim().toLowerCase()];
    },

    names() {
        return Object.values(this._defs).map(d => d.name).filter(n => !n.startsWith("__"));
    },

    canonicalName(name) {
        const def = this._defs[String(name || "").trim().toLowerCase()];
        return def ? def.name : null;
    },

    /** Returns a full (deep-cloned, finalized) state for a preset name. */
    get(name) {
        const key = String(name || "").trim().toLowerCase();
        if (!this._cache[key]) {
            this._cache[key] = this._build(key, 0);
        }
        return U.deepClone(this._cache[key]);
    },

    _build(key, depth) {
        const def = this._defs[key] || this._defs[P.defaultPreset.toLowerCase()] || this._defs.hd2d;
        const baseKey = def.base ? def.base.toLowerCase() : "";
        // Start from the base preset (if any), otherwise from the HD2D defaults.
        const state = baseKey && baseKey !== key && this._defs[baseKey] && depth < 8
            ? this._build(baseKey, depth + 1)
            : U.deepClone(this._defs.__default.state);
        const partial = def.partial || {};
        const add = partial.__addParticles;
        const clean = Object.assign({}, partial);
        delete clean.__addParticles;
        U.deepMerge(state, clean);
        if (add) state.particles = (state.particles || []).concat(add.map(e => Object.assign({}, e)));
        return finalizeState(state);
    }
});

/** Ensures every section has a weight and colors are arrays. */
const finalizeState = state => {
    for (const key of Object.keys(DEFAULT_STATE)) {
        const ref = DEFAULT_STATE[key];
        if (ref && typeof ref === "object" && !Array.isArray(ref)) {
            if (!state[key]) state[key] = U.deepClone(ref);
            const sec = state[key];
            if (sec.weight === undefined || sec.weight === null) sec.weight = sec.enabled === false ? 0 : 1;
        }
    }
    if (!Array.isArray(state.particles)) state.particles = [];
    return state;
};

// Register defaults and built-ins. Custom presets from the Plugin Manager are
// registered afterwards and may replace a built-in preset of the same name.
Presets._defs.__default = { name: "__default", state: finalizeState(U.deepClone(DEFAULT_STATE)) };
for (const name of Object.keys(BUILTIN_PRESETS)) {
    Presets.register(name, normalizePartial(BUILTIN_PRESETS[name]), "");
}
for (const s of P.customPresets) {
    const name = U.str(s["Name"], "").trim();
    if (!name) continue;
    let base = U.str(s["Base"], "").trim();
    const replacesExisting = Presets.has(name);
    if (replacesExisting && (!base || base.toLowerCase() === name.toLowerCase())) {
        // A custom preset with the name of an existing preset extends it:
        // keep the old definition under an alias and use that as the base.
        const alias = "__base_" + name;
        Presets._defs[alias.toLowerCase()] = Object.assign({}, Presets._defs[name.toLowerCase()], { name: alias });
        base = alias;
    }
    Presets.register(name, parsePresetStruct(s), base || "HD2D");
}
for (const name of Object.keys(GRADE_PRESETS)) GRADE_PRESETS[name] = normalizePartial(GRADE_PRESETS[name], "grade");

/** Returns the grade section of a grade preset or of any visual preset. */
HD2D.gradePreset = name => {
    const key = Object.keys(GRADE_PRESETS).find(k => k.toLowerCase() === String(name || "").trim().toLowerCase());
    if (key) {
        const g = U.deepClone(DEFAULT_STATE.grade);
        U.deepMerge(g, GRADE_PRESETS[key]);
        return g;
    }
    if (Presets.has(name)) return Presets.get(name).grade;
    return null;
};

//-----------------------------------------------------------------------------
// State interpolation
//-----------------------------------------------------------------------------

/** Interpolates two full states. Sections fade via their weight. */
const lerpState = (a, b, t) => {
    if (t <= 0) return U.deepClone(a);
    if (t >= 1) return U.deepClone(b);
    const out = {};
    for (const key of Object.keys(b)) {
        const va = a[key];
        const vb = b[key];
        if (key === "particles") {
            out[key] = U.deepClone(t < 0.5 && va ? va : vb);
        } else if (vb && typeof vb === "object" && !Array.isArray(vb)) {
            out[key] = lerpState(va && typeof va === "object" ? va : vb, vb, t);
        } else if (U.isColor(vb) && U.isColor(va)) {
            out[key] = [U.lerp(va[0], vb[0], t), U.lerp(va[1], vb[1], t), U.lerp(va[2], vb[2], t)];
        } else if (U.isNum(vb) && U.isNum(va)) {
            out[key] = U.lerp(va, vb, t);
        } else if (key === "enabled") {
            out[key] = !!(va || vb);
        } else {
            out[key] = U.deepClone(t < 0.5 && va !== undefined ? va : vb);
        }
    }
    return out;
};
HD2D.lerpState = lerpState;

//-----------------------------------------------------------------------------
// Time of day
//-----------------------------------------------------------------------------

const TimeOfDay = (HD2D.TimeOfDay = {
    phases: [],

    init() {
        const src = P.timePhases.length ? P.timePhases.map(s => this.parsePhaseStruct(s)) : BUILTIN_TIME_PHASES;
        this.phases = src
            .map(p => this.normalizePhase(p))
            .filter(p => p && U.isNum(p.hour))
            .sort((a, b) => a.hour - b.hour);
    },

    parsePhaseStruct(s) {
        const map = {
            name: "Name", hour: "Hour", ambientTint: "Ambient Tint", ambientMult: "Ambient Multiplier",
            sunTint: "Sun Tint", sunMult: "Sun Multiplier", sunAngle: "Sun Angle", sunElevation: "Sun Elevation",
            exposure: "Exposure Offset", temperature: "Temperature Offset", saturation: "Saturation Multiplier",
            contrast: "Contrast Multiplier", fogTint: "Fog Tint", fogMult: "Fog Multiplier", bloomMult: "Bloom Multiplier",
            lightMult: "Light Multiplier", lightTint: "Light Tint", dofMult: "DOF Multiplier",
            vignetteMult: "Vignette Multiplier", particles: "Particles", particleAmount: "Particle Amount"
        };
        const out = {};
        for (const key of Object.keys(map)) out[key] = s[map[key]];
        return out;
    },

    normalizePhase(p) {
        const tint = v => U.color(v, [1, 1, 1]);
        return {
            name: U.str(p.name, "Phase"),
            hour: U.num(p.hour, null),
            ambientTint: tint(p.ambientTint),
            ambientMult: U.num(p.ambientMult, 1),
            sunTint: tint(p.sunTint),
            sunMult: U.num(p.sunMult, 1),
            sunAngle: U.num(p.sunAngle, null),
            sunElevation: U.num(p.sunElevation, null),
            exposure: U.num(p.exposure, 0),
            temperature: U.num(p.temperature, 0),
            saturation: U.num(p.saturation, 1),
            contrast: U.num(p.contrast, 1),
            fogTint: tint(p.fogTint),
            fogMult: U.num(p.fogMult, 1),
            bloomMult: U.num(p.bloomMult, 1),
            lightMult: U.num(p.lightMult, 1),
            lightTint: tint(p.lightTint),
            dofMult: U.num(p.dofMult, 1),
            vignetteMult: U.num(p.vignetteMult, 1),
            particles: U.str(p.particles, "").trim().toLowerCase(),
            particleAmount: U.num(p.particleAmount, 0)
        };
    },

    /** Current hour (0..24) or null when time of day is not active. */
    hour() {
        const mode = P.timeMode;
        if (!$gameSystem || mode === "off" || mode === "") return null;
        if (mode === "variable") {
            if (!P.hourVariable) return null;
            const h = Number($gameVariables.value(P.hourVariable)) || 0;
            const m = P.minuteVariable ? Number($gameVariables.value(P.minuteVariable)) || 0 : 0;
            return (((h + m / 60) % 24) + 24) % 24;
        }
        const t = HD2D.State.data().time;
        return t && U.isNum(t.hour) ? ((t.hour % 24) + 24) % 24 : null;
    },

    /** Blended phase for an hour (cyclic interpolation between phases). */
    phaseAt(hour) {
        const list = this.phases;
        if (!list.length) return null;
        if (list.length === 1) return list[0];
        let next = list.findIndex(p => p.hour > hour);
        if (next < 0) next = 0;
        const prev = (next - 1 + list.length) % list.length;
        const a = list[prev];
        const b = list[next];
        let span = b.hour - a.hour;
        if (span <= 0) span += 24;
        let pos = hour - a.hour;
        if (pos < 0) pos += 24;
        const t = U.smoothstep(0, 1, U.saturate(pos / span));
        const mix = (x, y) => (U.isColor(x) ? [0, 1, 2].map(i => U.lerp(x[i], y[i], t)) : U.lerp(x, y, t));
        const angle = (x, y) => {
            if (x === null) return y;
            if (y === null) return x;
            let d = ((y - x + 540) % 360) - 180;
            return x + d * t;
        };
        const out = { name: t < 0.5 ? a.name : b.name, blend: t, from: a.name, to: b.name };
        for (const key of Object.keys(a)) {
            if (key === "name" || key === "hour") continue;
            if (key === "sunAngle") out[key] = angle(a[key], b[key]);
            else if (key === "sunElevation") out[key] = a[key] === null ? b[key] : b[key] === null ? a[key] : U.lerp(a[key], b[key], t);
            else if (key === "particles") out[key] = t < 0.5 ? a.particles : b.particles;
            else if (key === "particleAmount") out[key] = a.particles === b.particles ? U.lerp(a[key], b[key], t) : t < 0.5 ? a[key] * (1 - t * 2) : b[key] * (t * 2 - 1);
            else out[key] = mix(a[key], b[key]);
        }
        return out;
    },

    /** Applies the phase for the given hour onto a full state (in place). */
    apply(state, hour) {
        const ph = this.phaseAt(hour);
        if (!ph) return state;
        const mul = (c, t) => [c[0] * t[0], c[1] * t[1], c[2] * t[2]].map(U.saturate);
        state.ambient.color = mul(state.ambient.color, ph.ambientTint);
        state.ambient.intensity *= ph.ambientMult;
        state.sun.color = mul(state.sun.color, ph.sunTint);
        state.sun.intensity *= ph.sunMult;
        if (ph.sunAngle !== null) state.sun.angle = ph.sunAngle;
        if (ph.sunElevation !== null) state.sun.elevation = ph.sunElevation;
        state.grade.exposure += ph.exposure;
        state.grade.temperature += ph.temperature;
        state.grade.saturation *= ph.saturation;
        state.grade.contrast *= ph.contrast;
        state.fog.color = mul(state.fog.color, ph.fogTint);
        for (const layer of ["near", "mid", "far"]) state.fog[layer + "Opacity"] = U.saturate(state.fog[layer + "Opacity"] * ph.fogMult);
        state.atmosphere.hazeColor = mul(state.atmosphere.hazeColor, ph.fogTint);
        state.bloom.intensity *= ph.bloomMult;
        state.lights.intensity *= ph.lightMult;
        state.lights.color = mul(state.lights.color, ph.lightTint);
        state.dof.strength *= ph.dofMult;
        state.vignette.intensity *= ph.vignetteMult;
        if (state.rim.followSun) state.rim.angle = state.sun.angle;
        if (ph.particles && ph.particleAmount > 0.5) {
            state.particles = (state.particles || []).concat([{ type: ph.particles, amount: Math.round(ph.particleAmount), fromTime: true }]);
        }
        state._phase = ph.name;
        return state;
    }
});
TimeOfDay.init();


//=============================================================================
// 4. Runtime state (saved in $gameSystem) and the effective visual state
//-----------------------------------------------------------------------------
// Layers of the effective state, from bottom to top:
//   1. the active preset (map note <HD2DPreset>, command, or default preset)
//   2. map settings (<HD2DSet: ...> and shortcut tags in the map note)
//   3. time of day (if enabled and the preset reacts to it)
//   4. a running preset transition (snapshot -> target)
//   5. per-value overrides from plugin commands (each with its own tween)
// Effect toggles and the quality level are applied at render time.
//=============================================================================

const State = (HD2D.State = {
    _current: null,
    _target: null,
    _targetKey: "",
    _dirty: true,
    _tempData: null,

    fresh() {
        return {
            version: 1,
            preset: P.defaultPreset,
            trans: null,
            overrides: {},
            toggles: {},
            quality: null,
            time: { hour: 12 },
            timeTween: null,
            depth: {},
            pictures: {},
            lights: {},
            layers: {},
            emitters: {},
            mapPresets: {},
            camera: null,
            autoFocus: null,
            lastMapId: 0
        };
    },

    data() {
        if (typeof $gameSystem === "undefined" || !$gameSystem) {
            if (!this._tempData) this._tempData = this.fresh();
            return this._tempData;
        }
        if (!$gameSystem._hd2d) $gameSystem._hd2d = this.fresh();
        const d = $gameSystem._hd2d;
        if (d !== this._checkedData) {
            // Fill fields that older save files may not have (once per object).
            const f = this.fresh();
            for (const k of Object.keys(f)) if (d[k] === undefined) d[k] = f[k];
            this._checkedData = d;
        }
        return d;
    },

    invalidate() {
        this._dirty = true;
        this._targetKey = "";
    },

    /** Effective visual state for this frame. */
    current() {
        if (!this._current || this._dirty) this._current = this.compute();
        return this._current;
    },

    /** Target state: preset + map settings + time of day (cached). */
    target() {
        const d = this.data();
        const hour = TimeOfDay.hour();
        const mapUsesTime = MapTags.timeOfDay !== false;
        const key = [d.preset, MapTags.version, hour === null || !mapUsesTime ? "-" : hour.toFixed(3)].join("|");
        if (key !== this._targetKey || !this._target) {
            const st = Presets.get(d.preset);
            if (MapTags.noPresetParticles) st.particles = [];
            if (MapTags.settings) U.deepMerge(st, MapTags.settings);
            if (hour !== null && mapUsesTime && st.timeOfDay !== false) TimeOfDay.apply(st, hour);
            if (MapTags.emitters.length) st.particles = st.particles.concat(MapTags.emitters.map(e => Object.assign({}, e)));
            for (const key2 of Object.keys(DEFAULT_STATE)) {
                const sec = st[key2];
                if (sec && typeof sec === "object" && !Array.isArray(sec)) sec.weight = sec.enabled === false ? 0 : 1;
            }
            if (st.rim.followSun) st.rim.angle = st.sun.angle;
            this._target = st;
            this._targetKey = key;
        }
        return this._target;
    },

    compute() {
        const d = this.data();
        const target = this.target();
        let state;
        if (d.trans && d.trans.from && d.trans.dur > 0) {
            state = lerpState(d.trans.from, target, U.ease(d.trans.ease, d.trans.t / d.trans.dur));
        } else {
            state = U.deepClone(target);
        }
        for (const path of Object.keys(d.overrides)) {
            const o = d.overrides[path];
            const k = o.dur > 0 ? U.ease(o.ease, o.t / o.dur) : 1;
            let v;
            if (U.isColor(o.to) && U.isColor(o.from)) v = [0, 1, 2].map(i => U.lerp(o.from[i], o.to[i], k));
            else if (U.isNum(o.to) && U.isNum(o.from)) v = U.lerp(o.from, o.to, k);
            else v = k >= 1 ? o.to : o.from;
            U.setPath(state, path, U.deepClone(v));
            if (path.endsWith(".weight")) U.setPath(state, path.slice(0, -7) + ".enabled", v > 0.001);
        }
        state._phase = target._phase || "";
        this._dirty = false;
        return state;
    },

    /** Advances transitions; called once per frame while on the map/battle. */
    update() {
        const d = this.data();
        let changed = false;
        if (d.trans) {
            d.trans.t++;
            if (d.trans.t >= d.trans.dur) d.trans = null;
            changed = true;
        }
        for (const path of Object.keys(d.overrides)) {
            const o = d.overrides[path];
            if (o.t < o.dur) {
                o.t++;
                changed = true;
            } else if (o.release) {
                delete d.overrides[path];
                changed = true;
            }
        }
        if (d.timeTween) {
            const tw = d.timeTween;
            tw.t++;
            const k = U.ease(tw.ease, tw.dur > 0 ? tw.t / tw.dur : 1);
            d.time.hour = tw.from + (tw.to - tw.from) * k;
            if (tw.t >= tw.dur) d.timeTween = null;
            changed = true;
        }
        const tk = [d.preset, MapTags.version, TimeOfDay.hour()].join("|");
        if (tk !== this._lastTargetSig) {
            this._lastTargetSig = tk;
            changed = true;
        }
        if (changed) this._dirty = true;
        Depth.updateAutoFocus();
    },

    //--- presets -------------------------------------------------------------

    setPreset(name, duration = 0, easing = "smooth", keepOverrides = false) {
        const d = this.data();
        const canonical = Presets.canonicalName(name);
        if (!canonical) {
            U.warnOnce("Unknown preset '" + name + "'");
            return;
        }
        if (duration > 0) d.trans = { from: U.deepClone(this.current()), t: 0, dur: duration, ease: easing };
        else d.trans = null;
        d.preset = canonical;
        if (!keepOverrides) d.overrides = {};
        this.invalidate();
    },

    /** Starts a cross-fade from whatever is on screen now to the current target. */
    crossfade(duration, easing = "smooth") {
        const d = this.data();
        if (duration > 0 && this._current) d.trans = { from: U.deepClone(this._current), t: 0, dur: duration, ease: easing };
        else d.trans = null;
        this.invalidate();
    },

    //--- per-value overrides -------------------------------------------------

    _normPath(path) {
        let p = String(path || "").trim();
        if (!p) return null;
        p = p.replace(/^(\w)/, c => c.toLowerCase());
        const section = p.split(".")[0];
        const alias = { colorgrade: "grade", grading: "grade", depthoffield: "dof", ambientlight: "ambient", sunlight: "sun", directional: "sun", rimlight: "rim" };
        const fixed = alias[section.toLowerCase()];
        if (fixed) p = fixed + p.slice(section.length);
        return p;
    },

    setValue(path, value, duration = 0, easing = "smooth") {
        path = this._normPath(path);
        if (!path || value === null || value === undefined) return;
        const d = this.data();
        if (path.endsWith(".enabled")) {
            path = path.slice(0, -8) + ".weight";
            value = value ? 1 : 0;
        }
        let cur = U.getPath(this.current(), path);
        if (cur === undefined || cur === null) cur = value;
        d.overrides[path] = { from: U.deepClone(cur), to: U.deepClone(value), t: 0, dur: Math.max(0, duration | 0), ease: easing };
        this._dirty = true;
    },

    /** Applies a partial state (e.g. a whole section) as overrides. */
    setValues(partial, duration = 0, easing = "smooth", prefix = "") {
        for (const key of Object.keys(partial || {})) {
            const v = partial[key];
            const path = prefix ? prefix + "." + key : key;
            if (key === "particles" || key === "weight") continue;
            if (v && typeof v === "object" && !Array.isArray(v)) this.setValues(v, duration, easing, path);
            else this.setValue(path, v, duration, easing);
        }
    },

    /** Returns a value to its preset value (tweened) and removes the override. */
    resetValue(path, duration = 0, easing = "smooth") {
        path = this._normPath(path);
        if (!path) return;
        if (path.endsWith(".enabled")) path = path.slice(0, -8) + ".weight";
        const d = this.data();
        const keys = Object.keys(d.overrides).filter(k => k === path || k.startsWith(path + ".") || path === "all" || path === "*");
        for (const key of keys) {
            const targetValue = U.getPath(this.target(), key);
            const cur = U.getPath(this.current(), key);
            if (duration > 0 && targetValue !== undefined) {
                d.overrides[key] = { from: U.deepClone(cur), to: U.deepClone(targetValue), t: 0, dur: duration, ease: easing, release: true };
            } else {
                delete d.overrides[key];
            }
        }
        this._dirty = true;
    },

    //--- toggles and quality -------------------------------------------------

    effectOn(key) {
        const d = this.data();
        return d.toggles[key] !== undefined ? !!d.toggles[key] : !!P.toggles[key];
    },

    setEffect(key, on) {
        if (!EFFECT_KEYS.includes(key)) return;
        this.data().toggles[key] = !!on;
        this._dirty = true;
    },

    qualityKey() {
        const d = this.data();
        let key = String(d.quality || P.quality || "medium").toLowerCase();
        if (!QUALITY[key]) key = "medium";
        if (P.adaptiveQuality && Adaptive.level !== null && !d.quality) {
            const idx = Math.min(QUALITY_ORDER.indexOf(key), Adaptive.level);
            key = QUALITY_ORDER[Math.max(0, idx)];
        }
        return key;
    },

    quality() {
        return QUALITY[this.qualityKey()];
    },

    //--- map lifecycle -------------------------------------------------------

    onMapSetup(mapId) {
        const d = this.data();
        MapTags.parse($dataMap, mapId);
        const first = !d.lastMapId;
        const name = d.mapPresets[mapId] || MapTags.preset || P.defaultPreset;
        const canonical = Presets.canonicalName(name) || Presets.canonicalName(P.defaultPreset) || "HD2D";
        const duration = first ? 0 : P.mapTransitionFrames;
        if (!P.keepOverrides) d.overrides = {};
        if (duration > 0 && this._current) d.trans = { from: U.deepClone(this._current), t: 0, dur: duration, ease: "smooth" };
        else d.trans = null;
        d.preset = canonical;
        d.lastMapId = mapId;
        d.autoFocus = null;
        this.invalidate();
    }
});

/** Shortcut: the effective visual state of this frame. */
HD2D.state = () => State.current();

/** Adaptive quality: lowers the level when the frame rate stays low. */
const Adaptive = (HD2D.Adaptive = {
    level: null,
    _slow: 0,
    update() {
        if (!P.adaptiveQuality) return;
        const fps = Graphics._fpsCounter ? Graphics._fpsCounter.fps : 60;
        if (this.level === null) this.level = QUALITY_ORDER.length - 1;
        if (fps < 50) this._slow++;
        else this._slow = Math.max(0, this._slow - 2);
        if (this._slow > 180 && this.level > 0) {
            this.level--;
            this._slow = 0;
            console.info("[HD2D] Adaptive quality lowered to " + QUALITY_ORDER[this.level]);
        }
    }
});

//=============================================================================
// 5. Map note tags
//=============================================================================

const MapTags = (HD2D.MapTags = {
    version: 0,
    mapId: 0,

    reset() {
        this.preset = null;
        this.settings = null;
        this.regionDepth = {};
        this.regionEmissive = {};
        this.blockRegions = [];
        this.blockTerrain = [];
        this.layers = [];
        this.parallaxDepth = null;
        this.emitters = [];
        this.noPresetParticles = false;
        this.lights = [];
        this.lightRegions = [];
        this.timeOfDay = undefined;
        this.zoom = null;
        this.noHD2D = false;
    },

    parse(dataMap, mapId) {
        this.reset();
        this.mapId = mapId || 0;
        this.version++;
        const note = dataMap && dataMap.note ? dataMap.note : "";
        const preset = U.noteTag(note, "HD2DPreset");
        if (typeof preset === "string" && preset) this.preset = preset;
        const settings = {};
        for (const tag of U.noteTags(note, "HD2DSet")) U.deepMerge(settings, HD2D.parseSettingsString(tag));
        const focus = U.num(U.noteTag(note, "HD2DFocus"), null);
        if (focus !== null) U.setPath(settings, "dof.focus", U.clamp(focus, 0, 100));
        const ambient = U.noteTag(note, "HD2DAmbient");
        if (typeof ambient === "string") {
            const o = U.parseOptions(ambient);
            const color = U.color(o.args[0], null);
            if (color) U.setPath(settings, "ambient.color", color);
            const intensity = U.num(o.args[1], null);
            if (intensity !== null) U.setPath(settings, "ambient.intensity", intensity);
        }
        for (const tag of U.noteTags(note, "HD2DDisable")) {
            for (const name of String(tag).split(",")) {
                const key = HD2D.effectKey(name);
                if (key && DEFAULT_STATE[key] && !Array.isArray(DEFAULT_STATE[key])) U.setPath(settings, key + ".enabled", false);
                if (key === "lighting") U.setPath(settings, "lights.enabled", false);
            }
        }
        for (const tag of U.noteTags(note, "HD2DEnable")) {
            for (const name of String(tag).split(",")) {
                const key = HD2D.effectKey(name);
                if (key && DEFAULT_STATE[key] && !Array.isArray(DEFAULT_STATE[key])) U.setPath(settings, key + ".enabled", true);
                if (key === "lighting") U.setPath(settings, "lights.enabled", true);
            }
        }
        this.settings = Object.keys(settings).length ? settings : null;
        if (U.noteTag(note, "HD2DOff") !== undefined) {
            this.noHD2D = true;
            this.settings = this.settings || {};
            for (const key of Object.keys(DEFAULT_STATE)) {
                if (DEFAULT_STATE[key] && typeof DEFAULT_STATE[key] === "object" && !Array.isArray(DEFAULT_STATE[key])) U.setPath(this.settings, key + ".enabled", false);
            }
            this.noPresetParticles = true;
        }
        const regionPairs = (tag, target, max) => {
            for (const part of String(tag).split(/[,;]/)) {
                const m = part.match(/^\s*(\d+)\s*[=:]\s*(-?[\d.]+)\s*$/);
                if (m) target[Number(m[1])] = U.clamp(Number(m[2]), 0, max);
            }
        };
        for (const tag of U.noteTags(note, "HD2DRegionDepth")) regionPairs(tag, this.regionDepth, 100);
        for (const tag of U.noteTags(note, "HD2DRegionEmissive")) regionPairs(tag, this.regionEmissive, 4);
        for (const tag of U.noteTags(note, "HD2DBlockRegions")) this.blockRegions.push(...U.parseIdList(tag));
        for (const tag of U.noteTags(note, "HD2DBlockTerrain")) this.blockTerrain.push(...U.parseIdList(tag));
        for (const tag of U.noteTags(note, "HD2DLayer")) {
            const layer = Layers.parseTag(tag);
            if (layer) this.layers.push(layer);
        }
        const pd = U.num(U.noteTag(note, "HD2DParallaxDepth"), null);
        if (pd !== null) this.parallaxDepth = U.clamp(pd, 0, 100);
        for (const tag of U.noteTags(note, "HD2DParticles")) {
            const e = Particles.parseTag(tag);
            if (e) this.emitters.push(e);
        }
        if (U.noteTag(note, "HD2DNoPresetParticles") !== undefined) this.noPresetParticles = true;
        for (const tag of U.noteTags(note, "HD2DLight")) {
            const light = Lights.parseMapTag(tag, "point");
            if (light) this.lights.push(light);
        }
        for (const tag of U.noteTags(note, "HD2DSpotLight")) {
            const light = Lights.parseMapTag(tag, "spot");
            if (light) this.lights.push(light);
        }
        for (const tag of U.noteTags(note, "HD2DLightRegion")) {
            const o = U.parseOptions(tag);
            const region = U.num(o.args[0], 0);
            if (region > 0) this.lightRegions.push(Object.assign(Lights.parseOptions(o, 1, "point"), { region }));
        }
        const tod = U.noteTag(note, "HD2DTimeOfDay");
        if (tod !== undefined) this.timeOfDay = tod === true ? true : U.bool(tod, true);
        const zoom = U.num(U.noteTag(note, "HD2DZoom"), null);
        if (zoom !== null) this.zoom = zoom;
    },

    regionDepthOf(regionId) {
        if (this.regionDepth[regionId] !== undefined) return this.regionDepth[regionId];
        if (P.regionDepths[regionId] !== undefined) return P.regionDepths[regionId];
        return null;
    },

    regionEmissiveOf(regionId) {
        if (this.regionEmissive[regionId] !== undefined) return this.regionEmissive[regionId];
        if (P.regionEmissive[regionId] !== undefined) return P.regionEmissive[regionId];
        return 0;
    },

    isBlockingRegion(regionId) {
        return regionId > 0 && (this.blockRegions.includes(regionId) || P.blockRegions.includes(regionId));
    },

    isBlockingTerrain(tag) {
        return tag > 0 && (this.blockTerrain.includes(tag) || P.blockTerrainTags.includes(tag));
    }
});
MapTags.reset();

//=============================================================================
// 6. Event / actor note tags
//=============================================================================

/** Parses every HD2D tag found in a note or comment text. */
const parseObjectTags = text => {
    const tags = {
        depth: null, depthOffset: 0, emissive: 0, foreground: null, parallax: null, scale: null, noScale: false,
        lights: [], shadowCaster: false, shadow: null, rim: null, normalMap: null, particles: [], sortDepth: null
    };
    if (!text) return tags;
    const depth = U.noteTag(text, "HD2DDepth");
    if (depth !== undefined && depth !== true) {
        const v = U.num(depth, null);
        if (v !== null) tags.depth = U.clamp(v, 0, 100);
    }
    tags.depthOffset = U.num(U.noteTag(text, "HD2DDepthOffset"), 0);
    const em = U.noteTag(text, "HD2DEmissive");
    if (em !== undefined) tags.emissive = em === true ? 1 : U.clamp(U.num(em, 1), 0, 4);
    const fg = U.noteTag(text, "HD2DForeground");
    if (fg !== undefined) {
        const o = U.parseOptions(fg === true ? "" : fg);
        tags.foreground = {
            depth: U.clamp(U.num(o.args[0], U.num(o.opts.depth, 15)), 0, 100),
            parallax: U.num(o.opts.parallax, null),
            fade: U.bool(o.opts.fade, true),
            scale: U.num(o.opts.scale, null)
        };
    }
    const par = U.noteTag(text, "HD2DParallax");
    if (par !== undefined && par !== true) tags.parallax = U.num(par, null);
    const sc = U.noteTag(text, "HD2DScale");
    if (sc !== undefined && sc !== true) tags.scale = U.num(sc, null);
    tags.noScale = U.noteTag(text, "HD2DNoScale") !== undefined;
    for (const tag of U.noteTags(text, "HD2DLight")) tags.lights.push(Lights.parseEventTag(tag, "point"));
    for (const tag of U.noteTags(text, "HD2DSpotLight")) tags.lights.push(Lights.parseEventTag(tag, "spot"));
    tags.shadowCaster = U.noteTag(text, "HD2DShadowCaster") !== undefined;
    if (U.noteTag(text, "HD2DNoShadow") !== undefined) tags.shadow = false;
    else if (U.noteTag(text, "HD2DShadow") !== undefined) tags.shadow = true;
    if (U.noteTag(text, "HD2DNoRim") !== undefined) tags.rim = 0;
    else {
        const rim = U.noteTag(text, "HD2DRim");
        if (rim !== undefined) tags.rim = rim === true ? 1 : U.clamp(U.num(rim, 1), 0, 1);
    }
    const nm = U.noteTag(text, "HD2DNormalMap");
    if (typeof nm === "string" && nm) tags.normalMap = nm;
    for (const tag of U.noteTags(text, "HD2DParticles")) {
        const e = Particles.parseTag(tag);
        if (e) tags.particles.push(e);
    }
    if (U.noteTag(text, "HD2DSortByDepth") !== undefined) tags.sortDepth = true;
    return tags;
};
HD2D.parseObjectTags = parseObjectTags;

const EMPTY_TAGS = parseObjectTags("");

/** Text of all comments on an event page (comments can override the note). */
const pageCommentText = page => {
    if (!page || !page.list) return "";
    let text = "";
    for (const cmd of page.list) {
        if (cmd.code === 108 || cmd.code === 408) text += cmd.parameters[0] + "\n";
    }
    return text;
};

Game_CharacterBase.prototype.hd2dTags = function() {
    return EMPTY_TAGS;
};

Game_Event.prototype.hd2dTags = function() {
    if (this._hd2dTagsPage !== this._pageIndex || !this._hd2dTags) {
        const data = this.event();
        const note = data ? data.note || "" : "";
        const page = this._pageIndex >= 0 ? this.page() : null;
        this._hd2dTags = parseObjectTags(note + "\n" + pageCommentText(page));
        this._hd2dTagsPage = this._pageIndex;
        this._hd2dTagsVersion = (this._hd2dTagsVersion || 0) + 1;
    }
    return this._hd2dTags;
};

const actorTags = actor => {
    if (!actor) return EMPTY_TAGS;
    const data = actor.actor();
    if (!data) return EMPTY_TAGS;
    if (!data._hd2dTags) data._hd2dTags = parseObjectTags(data.note || "");
    return data._hd2dTags;
};

Game_Player.prototype.hd2dTags = function() {
    return actorTags($gameParty.leader());
};

Game_Follower.prototype.hd2dTags = function() {
    return actorTags(this.actor());
};

/** Key used to store command depth overrides for a character. */
const characterKey = ch => {
    if (!ch) return "";
    if (ch === $gamePlayer) return "player";
    if (ch instanceof Game_Follower) return "follower:" + ch._memberIndex;
    if (ch instanceof Game_Vehicle) return "vehicle:" + ch._type;
    if (ch instanceof Game_Event) return "event:" + ch._mapId + ":" + ch._eventId;
    return "";
};
HD2D.characterKey = characterKey;

//=============================================================================
// 7. Depth model
//=============================================================================

const Depth = (HD2D.Depth = {
    focalY: 0.56, // runtime focal plane position (smoothed when following the player)
    zoom: 1, // current camera zoom (kept here for depth math)
    viewHeight: 816, // screen height in pixels
    autoFocusDepth: null,

    /** Auto depth for a camera-space vertical position (0 = top, 1 = bottom). */
    auto(camY, cfg) {
        cfg = cfg || HD2D.state().depth;
        const F = cfg.focalDepth;
        if (!cfg.autoY) return F;
        const fy = this.focalY;
        const curve = Math.max(0.2, cfg.curve);
        if (camY >= fy) {
            const u = U.saturate((camY - fy) / Math.max(1 - fy, 0.01));
            return U.clamp(F - (F - cfg.nearDepth) * Math.pow(u, curve) * cfg.strength, 0, 100);
        }
        const u = U.saturate((fy - camY) / Math.max(fy, 0.01));
        return U.clamp(F + (cfg.farDepth - F) * Math.pow(u, curve) * cfg.strength, 0, 100);
    },

    /** Inverse of auto(): camera Y for a depth (used for depth sorting). */
    inverse(depth, cfg) {
        cfg = cfg || HD2D.state().depth;
        const F = cfg.focalDepth;
        const fy = this.focalY;
        const curve = Math.max(0.2, cfg.curve);
        const s = Math.max(cfg.strength, 0.0001);
        if (depth <= F) {
            const span = (F - cfg.nearDepth) * s;
            const u = span > 0 ? Math.pow(U.saturate((F - depth) / span), 1 / curve) : 0;
            return fy + (1 - fy) * u + (depth < F - span ? (F - span - depth) * 0.01 : 0);
        }
        const span = (cfg.farDepth - F) * s;
        const u = span > 0 ? Math.pow(U.saturate((depth - F) / span), 1 / curve) : 0;
        return fy - fy * u - (depth > F + span ? (depth - F - span) * 0.01 : 0);
    },

    /** Region depth at a map tile, or null. */
    regionDepthAt(x, y) {
        if (!$gameMap || !$dataMap) return null;
        const region = $gameMap.regionId(Math.round(x), Math.round(y));
        return region > 0 ? MapTags.regionDepthOf(region) : null;
    },

    /** Scroll factor of something at a given depth (1 = moves with the map). */
    parallaxFactor(depth, cfg) {
        cfg = cfg || HD2D.state().parallax;
        const F = HD2D.state().depth.focalDepth;
        if (depth <= F) return 1 + cfg.foregroundBoost * (F - depth) / Math.max(F, 1);
        const u = U.saturate((depth - F) / Math.max(100 - F, 1));
        return 1 - (1 - cfg.farFactor) * Math.pow(u, Math.max(0.1, cfg.curve));
    },

    /** Perspective scale for a depth (when perspective scaling is enabled). */
    perspectiveScale(depth, cfg) {
        cfg = cfg || HD2D.state().perspective;
        const F = HD2D.state().depth.focalDepth;
        if (depth <= F) return U.lerp(1, cfg.nearScale, U.saturate((F - depth) / Math.max(F, 1)));
        return U.lerp(1, cfg.farScale, U.saturate((depth - F) / Math.max(100 - F, 1)));
    },

    /** Signed circle of confusion for a depth: -1 (near blur) .. +1 (far blur). */
    coc(depth, dof) {
        dof = dof || HD2D.state().dof;
        const dz = depth - dof.focus;
        const far = U.smoothstep(dof.focusRange, dof.focusRange + Math.max(dof.farTransition, 0.01), dz) * dof.farBlur;
        const near = U.smoothstep(dof.focusRange, dof.focusRange + Math.max(dof.nearTransition, 0.01), -dz) * dof.nearBlur;
        return U.clamp(far - near, -1, 1);
    },

    /** Camera-space Y (0..1) of a character's feet. */
    characterCamY(ch) {
        const th = $gameMap.tileHeight();
        const footY = ($gameMap.adjustY(ch._realY) + 1) * th;
        return (footY * this.zoom) / Math.max(this.viewHeight, 1);
    },

    /**
     * Depth of a character. Priority: command override > note/comment tag >
     * region depth under the character > automatic depth from screen position.
     */
    forCharacter(ch) {
        const st = HD2D.state();
        const tags = ch.hd2dTags ? ch.hd2dTags() : EMPTY_TAGS;
        const ov = State.data().depth[characterKey(ch)];
        let depth;
        let explicit = false;
        if (ov && U.isNum(ov.depth)) {
            depth = ov.depth;
            explicit = true;
        } else if (tags.foreground) {
            depth = tags.foreground.depth;
            explicit = true;
        } else if (tags.depth !== null) {
            depth = tags.depth;
            explicit = true;
        } else {
            const region = P.characterRegionDepth ? this.regionDepthAt(ch._realX, ch._realY) : null;
            depth = region !== null ? region : this.auto(this.characterCamY(ch), st.depth);
            explicit = region !== null;
        }
        if (!(ov && U.isNum(ov.depth))) depth += tags.depthOffset || 0;
        return { depth: U.clamp(depth, 0, 100), explicit };
    },

    /** Smoothly follows the focal plane to the player's feet. */
    updateFocal(instant) {
        const st = HD2D.state();
        let target = st.depth.focalY;
        if (st.depth.followPlayer && $gamePlayer && $gameMap && $dataMap) {
            target = U.clamp(this.characterCamY($gamePlayer), 0.2, 0.85);
        }
        this.focalY = instant ? target : U.lerp(this.focalY, target, 0.12);
    },

    /** Auto focus: keeps the DOF focus on a character's depth. */
    updateAutoFocus() {
        const af = State.data().autoFocus;
        if (!af || !$gameMap) {
            this.autoFocusDepth = null;
            return;
        }
        const ch = HD2D.findCharacter(af.target, af.eventId);
        if (!ch) return;
        const d = this.forCharacter(ch).depth;
        this.autoFocusDepth = this.autoFocusDepth === null ? d : U.lerp(this.autoFocusDepth, d, af.speed || 0.1);
    }
});

/** Resolves "player" / "this event" / "event" / "follower N" / "vehicle" to a character. */
HD2D.findCharacter = (target, id, interpreter) => {
    const t = String(target || "player").trim().toLowerCase();
    if (!$gameMap) return null;
    if (t === "player") return $gamePlayer;
    if (t === "this event") return interpreter ? $gameMap.event(interpreter.eventId()) : null;
    if (t === "event") return $gameMap.event(Number(id) || 0) || null;
    if (t === "follower") return $gamePlayer.followers().follower(Math.max(0, (Number(id) || 1) - 1)) || null;
    if (t === "vehicle") return $gameMap.vehicle(["boat", "ship", "airship"][Number(id) || 0] || id) || null;
    return null;
};


//=============================================================================
// 8. Camera
//-----------------------------------------------------------------------------
// Zoom changes the number of visible tiles (Game_Map.screenTileX/Y), so map
// edges, centering and scrolling stay correct at any zoom level. The visual
// transform (zoom, rotation, shake) is applied to the world container only,
// so pictures, the timer and windows are not zoomed.
//=============================================================================

const Camera = (HD2D.Camera = {
    _snap: true,
    _shakeX: 0,
    _shakeY: 0,
    contX: 0, // continuous camera position in pixels (for parallax / particles)
    contY: 0,
    _lastDX: null,
    _lastDY: null,

    fresh() {
        return {
            zoom: 1, zoomTween: null,
            rotation: 0, rotTween: null,
            offsetX: 0, offsetY: 0, offsetTween: null,
            follow: { type: "player" },
            pan: null,
            shake: null,
            letterbox: 0, letterboxTween: null,
            fade: { color: [0, 0, 0], alpha: 0 }, fadeTween: null,
            hold: false,
            smooth: null
        };
    },

    data() {
        const d = State.data();
        if (!d.camera) d.camera = this.fresh();
        return d.camera;
    },

    enabled() {
        return State.effectOn("camera");
    },

    /** Zoom that defines the visible map area (1 when camera effects are off). */
    zoom() {
        if (!this.enabled()) return 1;
        const z = this.data().zoom;
        return U.clamp(U.isNum(z) ? z : 1, P.minZoom, P.maxZoom);
    },

    rotation() {
        return this.enabled() ? this.data().rotation || 0 : 0;
    },

    smoothOn() {
        const s = this.data().smooth;
        return s === null || s === undefined ? P.smoothCamera : !!s;
    },

    /** True while the camera (instead of vanilla scrolling) drives the view. */
    isActive() {
        if (!this.enabled()) return false;
        const c = this.data();
        return this.smoothOn() || Math.abs(this.zoom() - 1) > 0.0001 || !!c.zoomTween ||
            (c.follow && c.follow.type !== "player") || !!c.pan || c.offsetX !== 0 || c.offsetY !== 0;
    },

    snap() {
        this._snap = true;
    },

    _tween(obj, key, tweenKey) {
        const tw = obj[tweenKey];
        if (!tw) return;
        tw.t++;
        const k = U.ease(tw.ease, tw.dur > 0 ? tw.t / tw.dur : 1);
        if (Array.isArray(tw.to)) obj[key] = tw.to.map((v, i) => U.lerp(tw.from[i], v, k));
        else obj[key] = U.lerp(tw.from, tw.to, k);
        if (tw.t >= tw.dur) obj[tweenKey] = null;
    },

    setZoom(zoom, duration = 0, easing = "smooth") {
        const c = this.data();
        zoom = U.clamp(U.num(zoom, 1), P.minZoom, P.maxZoom);
        if (duration > 0) c.zoomTween = { from: c.zoom, to: zoom, t: 0, dur: duration, ease: easing };
        else {
            c.zoom = zoom;
            c.zoomTween = null;
        }
    },

    setRotation(deg, duration = 0, easing = "smooth") {
        const c = this.data();
        if (duration > 0) c.rotTween = { from: c.rotation, to: deg, t: 0, dur: duration, ease: easing };
        else {
            c.rotation = deg;
            c.rotTween = null;
        }
    },

    setOffset(x, y, duration = 0, easing = "smooth") {
        const c = this.data();
        if (duration > 0) c.offsetTween = { from: [c.offsetX, c.offsetY], to: [x, y], t: 0, dur: duration, ease: easing };
        else {
            c.offsetX = x;
            c.offsetY = y;
            c.offsetTween = null;
        }
    },

    /** Pans to (and then follows) a target: {type: player|event|point|none, id, x, y}. */
    focus(target, duration = 0, easing = "smooth") {
        const c = this.data();
        c.follow = target;
        c.hold = false;
        if (duration > 0 && $gameMap) {
            c.pan = { fromX: $gameMap.displayX(), fromY: $gameMap.displayY(), t: 0, dur: duration, ease: easing };
        } else {
            c.pan = null;
            this._snap = duration <= 0 && target.type !== "none" ? true : this._snap;
        }
    },

    shake(power, speed, duration, direction = "both") {
        this.data().shake = { power, speed, dur: Math.max(1, duration), t: 0, dir: String(direction).toLowerCase() };
    },

    setLetterbox(size, duration = 0, easing = "smooth") {
        const c = this.data();
        size = U.clamp(size, 0, 0.45);
        if (duration > 0) c.letterboxTween = { from: c.letterbox, to: size, t: 0, dur: duration, ease: easing };
        else {
            c.letterbox = size;
            c.letterboxTween = null;
        }
    },

    fade(color, alpha, duration = 0, easing = "smooth") {
        const c = this.data();
        const from = [c.fade.color[0], c.fade.color[1], c.fade.color[2], c.fade.alpha];
        const to = [color[0], color[1], color[2], U.saturate(alpha)];
        if (c.fade.alpha <= 0.001) {
            from[0] = to[0];
            from[1] = to[1];
            from[2] = to[2];
        }
        if (duration > 0) c.fadeTween = { from, to, t: 0, dur: duration, ease: easing };
        else {
            c.fade = { color: to.slice(0, 3), alpha: to[3] };
            c.fadeTween = null;
        }
    },

    isBusy() {
        const c = this.data();
        return !!(c.zoomTween || c.rotTween || c.offsetTween || c.pan || c.letterboxTween || c.fadeTween);
    },

    /** Called every frame on the map after the player has moved. */
    update() {
        const c = this.data();
        this._tween(c, "zoom", "zoomTween");
        this._tween(c, "rotation", "rotTween");
        if (c.offsetTween) {
            const tmp = { v: [c.offsetX, c.offsetY], tw: c.offsetTween };
            this._tween(tmp, "v", "tw");
            c.offsetX = tmp.v[0];
            c.offsetY = tmp.v[1];
            c.offsetTween = tmp.tw;
        }
        this._tween(c, "letterbox", "letterboxTween");
        if (c.fadeTween) {
            const tmp = { v: null, tw: c.fadeTween };
            this._tween(tmp, "v", "tw");
            c.fade = { color: tmp.v.slice(0, 3), alpha: tmp.v[3] };
            c.fadeTween = tmp.tw;
        }
        this.updateShake(c);
        if (this.isActive() && $gameMap && $dataMap) this.updateScroll(c);
        this.updateContinuous();
    },

    updateShake(c) {
        const s = c.shake;
        this._shakeX = 0;
        this._shakeY = 0;
        if (!s) return;
        s.t++;
        const decay = 1 - U.smoothstep(0.6, 1, s.t / s.dur);
        const f = s.t * s.speed * 0.06;
        const amp = s.power * decay;
        if (s.dir !== "vertical") this._shakeX = (U.noise1(f) * 2 - 1) * amp;
        if (s.dir !== "horizontal") this._shakeY = (U.noise1(f + 71.3) * 2 - 1) * amp;
        if (s.t >= s.dur) c.shake = null;
    },

    /** Target view center in tiles. */
    targetCenter(c) {
        const f = c.follow || { type: "player" };
        let x;
        let y;
        if (f.type === "event") {
            const ev = $gameMap.event(f.id);
            if (!ev) return null;
            x = ev._realX + 0.5;
            y = ev._realY + 0.5;
        } else if (f.type === "point") {
            x = f.x + 0.5;
            y = f.y + 0.5;
        } else if (f.type === "none") {
            return null;
        } else {
            x = $gamePlayer._realX + 0.5;
            y = $gamePlayer._realY + 0.5;
        }
        return { x: x + c.offsetX / $gameMap.tileWidth(), y: y + c.offsetY / $gameMap.tileHeight() };
    },

    /** Clamps a display position like Game_Map.setDisplayPos does. */
    clampDisplay(x, y) {
        const w = $gameMap.width();
        const h = $gameMap.height();
        const sw = $gameMap.screenTileX();
        const sh = $gameMap.screenTileY();
        if (!$gameMap.isLoopHorizontal()) {
            const endX = w - sw;
            x = endX < 0 ? endX / 2 : U.clamp(x, 0, endX);
        }
        if (!$gameMap.isLoopVertical()) {
            const endY = h - sh;
            y = endY < 0 ? endY / 2 : U.clamp(y, 0, endY);
        }
        return { x, y };
    },

    _delta(from, to, size, loop) {
        let d = to - from;
        if (loop) d = ((((d + size / 2) % size) + size) % size) - size / 2;
        return d;
    },

    updateScroll(c) {
        if ($gameMap.isScrolling()) {
            c.hold = true; // an event is scrolling the map: do not fight it
            return;
        }
        if (c.hold) {
            if ($gamePlayer.isMoving() || c.zoomTween || c.pan || (c.follow && c.follow.type !== "player")) c.hold = false;
            else return;
        }
        const center = this.targetCenter(c);
        if (!center) return;
        let want = this.clampDisplay(center.x - $gameMap.screenTileX() / 2, center.y - $gameMap.screenTileY() / 2);
        const dx0 = $gameMap.displayX();
        const dy0 = $gameMap.displayY();
        if (c.pan) {
            c.pan.t++;
            const k = U.ease(c.pan.ease, c.pan.t / Math.max(1, c.pan.dur));
            const px = c.pan.fromX + this._delta(c.pan.fromX, want.x, $gameMap.width(), $gameMap.isLoopHorizontal()) * k;
            const py = c.pan.fromY + this._delta(c.pan.fromY, want.y, $gameMap.height(), $gameMap.isLoopVertical()) * k;
            want = { x: px, y: py };
            if (c.pan.t >= c.pan.dur) c.pan = null;
        }
        let dx = this._delta(dx0, want.x, $gameMap.width(), $gameMap.isLoopHorizontal());
        let dy = this._delta(dy0, want.y, $gameMap.height(), $gameMap.isLoopVertical());
        if (!this._snap && !c.pan && this.smoothOn() && !c.zoomTween) {
            const k = P.cameraSpeed;
            dx *= k;
            dy *= k;
            // Settle exactly instead of creeping forever.
            if (Math.abs(dx) < 0.0005) dx = this._delta(dx0, want.x, $gameMap.width(), $gameMap.isLoopHorizontal());
            if (Math.abs(dy) < 0.0005) dy = this._delta(dy0, want.y, $gameMap.height(), $gameMap.isLoopVertical());
        }
        this._snap = false;
        this.moveDisplay(dx, dy);
    },

    /** Moves the display using the map's own scroll functions (keeps parallax in sync). */
    moveDisplay(dx, dy) {
        const sw = $gameMap.screenTileX();
        const sh = $gameMap.screenTileY();
        if (!$gameMap.isLoopHorizontal() && $gameMap.width() < sw) {
            $gameMap._displayX = ($gameMap.width() - sw) / 2;
            $gameMap._parallaxX = $gameMap._displayX;
        } else if (dx > 0) $gameMap.scrollRight(dx);
        else if (dx < 0) $gameMap.scrollLeft(-dx);
        if (!$gameMap.isLoopVertical() && $gameMap.height() < sh) {
            $gameMap._displayY = ($gameMap.height() - sh) / 2;
            $gameMap._parallaxY = $gameMap._displayY;
        } else if (dy > 0) $gameMap.scrollDown(dy);
        else if (dy < 0) $gameMap.scrollUp(-dy);
        if (P.pixelPerfect) {
            // Snap the view to whole screen pixels to avoid sub-pixel shimmer.
            const z = this.zoom();
            const qx = 1 / ($gameMap.tileWidth() * z);
            const qy = 1 / ($gameMap.tileHeight() * z);
            $gameMap._displayX = Math.round($gameMap._displayX / qx) * qx;
            $gameMap._displayY = Math.round($gameMap._displayY / qy) * qy;
        }
    },

    /** Tracks an unwrapped camera position in pixels (for parallax and particles). */
    updateContinuous() {
        if (!$gameMap || !$dataMap) return;
        const x = $gameMap.displayX();
        const y = $gameMap.displayY();
        if (this._lastDX === null || this._resetCont) {
            this.contX = x * $gameMap.tileWidth();
            this.contY = y * $gameMap.tileHeight();
            this._resetCont = false;
        } else {
            this.contX += this._delta(this._lastDX, x, $gameMap.width(), $gameMap.isLoopHorizontal()) * $gameMap.tileWidth();
            this.contY += this._delta(this._lastDY, y, $gameMap.height(), $gameMap.isLoopVertical()) * $gameMap.tileHeight();
        }
        this._lastDX = x;
        this._lastDY = y;
    },

    onTransfer() {
        this._snap = true;
        this._resetCont = true;
        const c = this.data();
        c.pan = null;
        c.hold = false;
        if (c.follow && c.follow.type === "event") c.follow = { type: "player" };
        if (MapTags.zoom !== null) {
            c.zoom = U.clamp(MapTags.zoom, P.minZoom, P.maxZoom);
            c.zoomTween = null;
        }
    },

    /** Shake offset in screen pixels for this frame. */
    shakeOffset() {
        return { x: this._shakeX, y: this._shakeY };
    }
});

//=============================================================================
// 9. Lights
//=============================================================================

const Lights = (HD2D.Lights = {
    _frame: 0,
    list: [], // render-ready lights for this frame (local coordinates)

    defaults(type) {
        return {
            id: "", type: type || "point", attach: "map", eventId: 0, mapId: 0, x: 0, y: 0, offsetX: 0, offsetY: 0,
            radius: 144, intensity: 1, color: [1, 0.85, 0.65], falloff: 2, softness: 0.5,
            direction: 90, facing: false, cone: 50, coneSoftness: 0.35,
            flicker: 0, flickerSpeed: 1, shadows: true, depth: null, depthRange: 40, glow: null, height: P.lightHeight,
            enabled: true, scope: "map"
        };
    },

    /** Reads option keys shared by all light tag / command formats. */
    parseOptions(o, startIndex, type) {
        const L = this.defaults(type);
        const a = o.args;
        const i = startIndex;
        L.radius = U.num(a[i], U.num(o.opts.radius, L.radius));
        L.color = U.color(a[i + 1], U.color(o.opts.color, L.color));
        L.intensity = U.num(a[i + 2], U.num(o.opts.intensity, L.intensity));
        if (type === "spot") {
            const dir = a[i + 3] !== undefined ? a[i + 3] : o.opts.direction;
            if (dir !== undefined && String(dir).toLowerCase() === "facing") L.facing = true;
            else L.direction = U.num(dir, L.direction);
            L.cone = U.num(a[i + 4], U.num(o.opts.cone, L.cone));
        }
        const opt = o.opts;
        L.falloff = U.num(opt.falloff, L.falloff);
        L.softness = U.clamp(U.num(opt.softness, L.softness), 0, 1);
        L.flicker = U.clamp(U.num(opt.flicker, L.flicker), 0, 1);
        L.flickerSpeed = U.num(opt.speed, U.num(opt.flickerspeed, L.flickerSpeed));
        L.offsetX = U.num(opt.offsetx, U.num(opt.ox, L.offsetX));
        L.offsetY = U.num(opt.offsety, U.num(opt.oy, L.offsetY));
        L.shadows = U.bool(opt.shadows, L.shadows);
        const depth = U.num(opt.depth, null);
        if (depth !== null) L.depth = U.clamp(depth, 0, 100);
        L.depthRange = U.num(opt.range, U.num(opt.depthrange, L.depthRange));
        const glow = U.num(opt.glow, null);
        if (glow !== null) L.glow = U.clamp(glow, 0, 2);
        L.height = U.num(opt.height, L.height);
        L.coneSoftness = U.clamp(U.num(opt.conesoftness, L.coneSoftness), 0, 1);
        if (opt.facing !== undefined) L.facing = U.bool(opt.facing, L.facing);
        if (opt.direction !== undefined && String(opt.direction).toLowerCase() !== "facing") L.direction = U.num(opt.direction, L.direction);
        if (opt.cone !== undefined) L.cone = U.num(opt.cone, L.cone);
        return L;
    },

    /** <HD2DLight: radius, color, intensity, options> on an event. */
    parseEventTag(tag, type) {
        const o = U.parseOptions(tag === true ? "" : tag);
        const L = this.parseOptions(o, 0, type);
        L.attach = "self";
        return L;
    },

    /** <HD2DLight: x, y, radius, color, intensity, options> in a map note. */
    parseMapTag(tag, type) {
        const o = U.parseOptions(tag === true ? "" : tag);
        const x = U.num(o.args[0], null);
        const y = U.num(o.args[1], null);
        if (x === null || y === null) return null;
        const L = this.parseOptions(o, 2, type);
        L.attach = "map";
        L.x = x;
        L.y = y;
        return L;
    },

    /** Lights created by plugin commands (saved). */
    commandLights() {
        const d = State.data();
        const mapId = $gameMap ? $gameMap.mapId() : 0;
        return Object.values(d.lights).filter(L => L && (L.scope === "global" || L.mapId === mapId));
    },

    create(config) {
        const d = State.data();
        const L = Object.assign(this.defaults(config.type), config);
        L.id = String(config.id || "light" + Object.keys(d.lights).length);
        L.mapId = $gameMap ? $gameMap.mapId() : 0;
        const old = d.lights[L.id];
        L.fade = { from: old ? this.fadeValue(old) : 0, to: 1, t: 0, dur: Math.max(0, config.fadeDuration || 0) };
        d.lights[L.id] = L;
        return L;
    },

    remove(id, duration = 0) {
        const d = State.data();
        const L = d.lights[id];
        if (!L) return;
        if (duration > 0) {
            L.fade = { from: this.fadeValue(L), to: 0, t: 0, dur: duration, remove: true };
        } else {
            delete d.lights[id];
        }
    },

    fadeValue(L) {
        const f = L.fade;
        if (!f) return 1;
        return f.dur > 0 ? U.lerp(f.from, f.to, U.ease("smooth", Math.min(1, f.t / f.dur))) : f.to;
    },

    /** Builds the render-ready light list for this frame (local pixel coordinates). */
    update(viewW, viewH) {
        this._frame++;
        const out = [];
        if (!$gameMap || !$dataMap) {
            this.list = out;
            return;
        }
        const st = HD2D.state();
        const tw = $gameMap.tileWidth();
        const th = $gameMap.tileHeight();
        const ambLuma = U.luma(st.ambient.color) * st.ambient.intensity * st.ambient.weight + (1 - st.ambient.weight);
        const dayFade = 1 - st.lights.dayFade * U.smoothstep(0.35, 0.9, ambLuma);
        const globalMult = st.lights.intensity * dayFade;
        const push = (L, lx, ly, ch) => {
            if (!L.enabled) return;
            let fade = 1;
            if (L.fade) {
                if (L.fade.t < L.fade.dur) L.fade.t++;
                fade = this.fadeValue(L);
                if (L.fade.remove && L.fade.t >= L.fade.dur) {
                    delete State.data().lights[L.id];
                    return;
                }
            }
            const r = Math.max(1, L.radius);
            if (lx + r < -64 || ly + r < -64 || lx - r > viewW + 64 || ly - r > viewH + 64) return;
            let intensity = L.intensity * globalMult * fade;
            if (L.flicker > 0) {
                const t = this._frame * 0.05 * L.flickerSpeed + (L._seed || (L._seed = Math.random() * 1000));
                const n = U.noise1(t) * 0.7 + U.noise1(t * 2.7 + 13.1) * 0.3;
                intensity *= 1 - L.flicker * n;
            }
            if (intensity <= 0.002) return;
            let dir = L.direction;
            if (L.facing && ch) {
                const target = { 2: 90, 4: 180, 6: 0, 8: 270 }[ch.direction()] || 90;
                const cur = L._facingDir === undefined ? target : L._facingDir;
                const delta = ((target - cur + 540) % 360) - 180;
                L._facingDir = cur + delta * 0.25;
                dir = L._facingDir;
            }
            const color = [L.color[0] * st.lights.color[0], L.color[1] * st.lights.color[1], L.color[2] * st.lights.color[2]];
            out.push({
                type: L.type, x: lx, y: ly, radius: r, intensity, color, falloff: L.falloff, softness: L.softness,
                direction: dir, cone: L.cone, coneSoftness: L.coneSoftness, shadows: L.shadows,
                depth: L.depth, depthRange: L.depthRange, glow: L.glow === null ? st.lights.glow : L.glow,
                height: L.height, importance: intensity * r
            });
        };
        const mapPos = (x, y) => [($gameMap.adjustX(x) + 0.5) * tw, ($gameMap.adjustY(y) + 0.5) * th];
        const charPos = (ch, L) => [ch.screenX() + L.offsetX, ch.screenY() - th * 0.45 + L.offsetY];
        // Event lights from tags.
        for (const ev of $gameMap.events()) {
            if (ev._erased || ev._pageIndex < 0) continue;
            const tags = ev.hd2dTags();
            if (!tags.lights.length) continue;
            for (const L of tags.lights) {
                const p = charPos(ev, L);
                push(L, p[0], p[1], ev);
            }
        }
        // Actor lights (lanterns) from actor note tags.
        const playerTags = $gamePlayer.hd2dTags();
        for (const L of playerTags.lights) {
            const p = charPos($gamePlayer, L);
            push(L, p[0], p[1], $gamePlayer);
        }
        // Map note lights.
        for (const L of MapTags.lights) {
            const p = mapPos(L.x, L.y);
            push(L, p[0] + L.offsetX, p[1] + L.offsetY, null);
        }
        // Region lights (cached positions).
        if (MapTags.lightRegions.length) {
            if (this._regionCacheVersion !== MapTags.version) this.buildRegionCache();
            for (const item of this._regionCache) {
                const p = mapPos(item.x, item.y);
                push(item.light, p[0] + item.light.offsetX, p[1] + item.light.offsetY, null);
            }
        }
        // Command lights.
        for (const L of this.commandLights()) {
            let p;
            if (L.attach === "screen") p = [L.x, L.y];
            else if (L.attach === "map") p = mapPos(L.x, L.y);
            else {
                const ch = HD2D.findCharacter(L.attach, L.eventId);
                if (!ch) continue;
                p = charPos(ch, L);
                push(L, p[0], p[1], ch);
                continue;
            }
            push(L, p[0] + L.offsetX, p[1] + L.offsetY, null);
        }
        const max = State.quality().maxLights;
        if (out.length > max) {
            const cx = viewW / 2;
            const cy = viewH / 2;
            for (const l of out) l.importance /= 1 + Math.hypot(l.x - cx, l.y - cy) / (viewW + viewH);
            out.sort((a, b) => b.importance - a.importance);
            out.length = max;
        }
        this.list = out;
    },

    buildRegionCache() {
        this._regionCache = [];
        this._regionCacheVersion = MapTags.version;
        for (const rl of MapTags.lightRegions) {
            for (let y = 0; y < $gameMap.height(); y++) {
                for (let x = 0; x < $gameMap.width(); x++) {
                    if ($gameMap.regionId(x, y) === rl.region && this._regionCache.length < 256) {
                        this._regionCache.push({ x, y, light: rl });
                    }
                }
            }
        }
    }
});

//=============================================================================
// 10. Particles
//-----------------------------------------------------------------------------
// Screen-wide emitters live in a wrapped "layer space" that scrolls with the
// camera according to each particle's depth (parallax). Depth also controls
// size, speed, opacity and softness (a pre-blurred texture variant), so that
// particles reinforce the depth of the scene without per-particle filters.
//=============================================================================

const PARTICLE_TYPES = {
    dust: { tex: "dot", size: [1.5, 3.5], vx: [-0.12, 0.12], vy: [-0.08, 0.1], gravity: 0, wobble: 0.25, life: [300, 600], alpha: 0.45, color: "#fff4e0", blend: 0, emissive: false, twinkle: 0, depth: [12, 88] },
    motes: { tex: "dot", size: [1.5, 4], vx: [-0.1, 0.1], vy: [-0.12, 0.02], gravity: 0, wobble: 0.35, life: [300, 600], alpha: 0.6, color: "#fff4d0", blend: 1, emissive: true, twinkle: 0.45, depth: [10, 90] },
    light: { tex: "glow", size: [4, 9], vx: [-0.08, 0.08], vy: [-0.15, -0.02], gravity: 0, wobble: 0.3, life: [240, 480], alpha: 0.55, color: "#fff2b8", blend: 1, emissive: true, twinkle: 0.4, depth: [15, 85] },
    mist: { tex: "puff", size: [90, 170], vx: [0.08, 0.25], vy: [-0.02, 0.02], gravity: 0, wobble: 0, life: [500, 900], alpha: 0.12, color: "#e8eef8", blend: 0, emissive: false, twinkle: 0, depth: [25, 80] },
    fog: { tex: "puff", size: [150, 280], vx: [0.12, 0.3], vy: [-0.02, 0.02], gravity: 0, wobble: 0, life: [600, 1000], alpha: 0.1, color: "#e0e6ee", blend: 0, emissive: false, twinkle: 0, depth: [30, 85] },
    rain: { tex: "streak", size: [1, 1.4], vx: [-2.2, -1.6], vy: [13, 17], gravity: 0, wobble: 0, life: [999, 999], alpha: 0.5, color: "#dce6f6", blend: 0, emissive: true, twinkle: 0, depth: [5, 95], streak: true, maxBlur: 1 },
    storm: { tex: "streak", size: [1.1, 1.6], vx: [-5, -3.5], vy: [16, 21], gravity: 0, wobble: 0, life: [999, 999], alpha: 0.55, color: "#d4def0", blend: 0, emissive: true, twinkle: 0, depth: [5, 95], streak: true, maxBlur: 1 },
    snow: { tex: "flake", size: [4, 8], vx: [-0.4, 0.1], vy: [0.6, 1.4], gravity: 0, wobble: 1, life: [999, 999], alpha: 0.85, maxBlur: 2, color: "#ffffff", blend: 0, emissive: true, twinkle: 0, depth: [5, 95], falls: true },
    ash: { tex: "dot", size: [1.5, 3.5], vx: [-0.25, 0.1], vy: [0.25, 0.6], gravity: 0, wobble: 0.6, life: [999, 999], alpha: 0.7, color: "#b4aca4", blend: 0, emissive: false, twinkle: 0, depth: [10, 90], falls: true },
    embers: { tex: "spark", size: [1.5, 3.5], vx: [-0.2, 0.25], vy: [-1.1, -0.5], gravity: 0, wobble: 0.6, life: [120, 260], alpha: 0.95, color: "#ffa040", blend: 1, emissive: true, twinkle: 0.5, depth: [15, 85] },
    fireflies: { tex: "glow", size: [3, 6], vx: [-0.25, 0.25], vy: [-0.2, 0.2], gravity: 0, wobble: 1.2, life: [400, 800], alpha: 0.95, color: "#d8ff80", blend: 1, emissive: true, twinkle: 0.95, depth: [20, 80] },
    magic: { tex: "sparkle", size: [3, 7], vx: [-0.15, 0.15], vy: [-0.45, -0.1], gravity: 0, wobble: 0.6, life: [200, 420], alpha: 0.9, color: "#a8c8ff", colors: ["#a8c8ff", "#ffb8f0", "#c8ffe8", "#fff0a8"], blend: 1, emissive: true, twinkle: 0.7, depth: [15, 85] },
    leaves: { tex: "leaf", size: [5, 8], vx: [-0.6, -0.15], vy: [0.4, 0.9], gravity: 0, wobble: 1.4, life: [999, 999], alpha: 0.9, color: "#8ab060", colors: ["#8ab060", "#a8c070", "#c8b058"], blend: 0, emissive: false, twinkle: 0, depth: [10, 80], falls: true, spin: 0.04 },
    petals: { tex: "petal", size: [4, 7], vx: [-0.7, -0.2], vy: [0.35, 0.8], gravity: 0, wobble: 1.4, life: [999, 999], alpha: 0.9, color: "#ffc8dc", colors: ["#ffc8dc", "#ffd8e8", "#ffb0c8"], blend: 0, emissive: false, twinkle: 0, depth: [10, 80], falls: true, spin: 0.05 },
    sunbeams: { tex: "beam", size: [90, 170], vx: [0.02, 0.06], vy: [0, 0], gravity: 0, wobble: 0, life: [500, 900], alpha: 0.16, color: "#fff2c8", blend: 1, emissive: true, twinkle: 0, depth: [35, 65], beam: true }
};
HD2D.PARTICLE_TYPES = PARTICLE_TYPES;
for (const def of Object.values(PARTICLE_TYPES)) {
    def.rgb = U.color(def.color, [1, 1, 1]);
    if (def.colors) def.rgbs = def.colors.map(c => U.color(c, def.rgb));
}

const Particles = (HD2D.Particles = {
    /** <HD2DParticles: type, amount n, depth a-b, color #fff, size s, speed s, ...> */
    parseTag(tag) {
        const o = U.parseOptions(tag === true ? "" : tag);
        const type = String(o.args[0] || o.opts.type || "").trim().toLowerCase();
        if (!PARTICLE_TYPES[type]) {
            U.warnOnce("Unknown particle type '" + type + "'");
            return null;
        }
        const e = { type };
        const amount = U.num(o.args[1], U.num(o.opts.amount, null));
        if (amount !== null) e.amount = amount;
        if (o.opts.depth) {
            const m = String(o.opts.depth).match(/(-?[\d.]+)\s*(?:-|to|\s)\s*(-?[\d.]+)/);
            if (m) {
                e.depthMin = Number(m[1]);
                e.depthMax = Number(m[2]);
            } else {
                e.depthMin = e.depthMax = U.num(o.opts.depth, 50);
            }
        }
        for (const key of ["size", "speed", "opacity", "wind", "radius"]) {
            const v = U.num(o.opts[key], null);
            if (v !== null) e[key] = v;
        }
        const color = U.color(o.opts.color, null);
        if (color) e.color = color;
        if (o.opts.emissive !== undefined) e.emissive = U.bool(o.opts.emissive, null);
        if (o.opts.area) e.area = String(o.opts.area).toLowerCase();
        return e;
    },

    signature(e) {
        return [e.type, e.depthMin, e.depthMax, e.color ? U.colorHex(e.color) : "", e.size, e.speed, e.opacity, e.wind, e.emissive, e.area, e.eventId, e.radius, e.id].join("|");
    }
});

//=============================================================================
// 11. Parallax layers
//=============================================================================

const Layers = (HD2D.Layers = {
    /** <HD2DLayer: image, depth n, loop x|y|xy|none, scroll sx sy, x n, y n, ...> */
    parseTag(tag) {
        const o = U.parseOptions(tag === true ? "" : tag);
        const image = String(o.args[0] || o.opts.image || "").trim();
        if (!image) return null;
        const L = {
            id: o.opts.id || image,
            image,
            folder: String(o.opts.folder || "parallaxes").replace(/^img\//, "").replace(/\/$/, ""),
            depth: U.clamp(U.num(o.opts.depth, U.num(o.args[1], 85)), 0, 100),
            loopX: true,
            loopY: false,
            x: U.num(o.opts.x, 0),
            y: U.num(o.opts.y, 0),
            scrollX: 0,
            scrollY: 0,
            factorX: null,
            factorY: null,
            opacity: U.clamp(U.num(o.opts.opacity, 255), 0, 255),
            blend: Layers.blendMode(o.opts.blend),
            scale: U.num(o.opts.scale, 1),
            zoomInfluence: U.num(o.opts.zoom, null),
            front: o.opts.front !== undefined ? U.bool(o.opts.front, null) : null,
            visible: true
        };
        if (o.opts.loop !== undefined) {
            const v = String(o.opts.loop).toLowerCase();
            L.loopX = v.includes("x") || v === "true" || v === "both";
            L.loopY = v.includes("y") || v === "both";
        }
        if (o.opts.scroll !== undefined) {
            const s = String(o.opts.scroll).split(/\s+/).map(Number);
            L.scrollX = Number.isFinite(s[0]) ? s[0] : 0;
            L.scrollY = Number.isFinite(s[1]) ? s[1] : 0;
        }
        if (o.opts.factor !== undefined) {
            const f = String(o.opts.factor).split(/\s+/).map(Number);
            if (Number.isFinite(f[0])) L.factorX = f[0];
            L.factorY = Number.isFinite(f[1]) ? f[1] : L.factorX;
        }
        return L;
    },

    blendMode(v) {
        const s = String(v === undefined ? "normal" : v).trim().toLowerCase();
        if (s === "1" || s === "add" || s === "additive") return 1;
        if (s === "2" || s === "multiply") return 2;
        if (s === "3" || s === "screen") return 3;
        return 0;
    },

    /** Layers for the current map: map note layers + command layers. */
    current() {
        const d = State.data();
        const mapId = $gameMap ? $gameMap.mapId() : 0;
        const byId = {};
        for (const L of MapTags.layers) byId[L.id] = L;
        for (const L of Object.values(d.layers)) {
            if (!L || (L.scope !== "global" && L.mapId !== mapId)) continue;
            if (L.removed) delete byId[L.id];
            else byId[L.id] = L;
        }
        return Object.values(byId);
    }
});


//=============================================================================
// 12. Shaders (GLSL ES 1.00 - runs on WebGL 1 and 2)
//-----------------------------------------------------------------------------
// Rendering overview (per frame, map scene):
//   world      : the normal RPG Maker scene (tiles, characters, layers, ...)
//   objects    : sprites redrawn as flat "data" (depth / emissive / rim id)
//   depth      : objects + automatic depth field + region depths, per pixel
//   shadows    : character silhouettes + contact shadows, blurred
//   light      : ambient + sun (+ normal maps) + point/spot lights (+ tile occlusion)
//   overlay    : unlit things (emissive particles, glows, animations)
//   dof        : half-res lit/fogged image + circle of confusion -> gather blur
//   bloom      : bright pass + emissive -> dual-filter blur pyramid
//   final      : lighting, atmosphere, fog, DOF mix, rim, bloom, grading, vignette
//=============================================================================

const GLSL = (HD2D.GLSL = {});

GLSL.PRECISION = "precision highp float;\n";

// Vertex shader for internal full-screen passes (drawn with our own quad).
GLSL.QUAD_VERT = `
attribute vec2 aVertexPosition;
uniform mat3 projectionMatrix;
uniform vec4 uFrame;
uniform vec2 uInputScale;
varying vec2 vTextureCoord;
varying vec2 vScreenUV;
varying vec2 vScreenPx;
void main(void) {
    vec2 pos = uFrame.xy + aVertexPosition * uFrame.zw;
    gl_Position = vec4((projectionMatrix * vec3(pos, 1.0)).xy, 0.0, 1.0);
    vTextureCoord = aVertexPosition * uInputScale;
    vScreenUV = aVertexPosition;
    vScreenPx = pos;
}
`;

// Vertex shader for the final pass (run through PIXI's filter system).
GLSL.FILTER_VERT = `
attribute vec2 aVertexPosition;
uniform mat3 projectionMatrix;
uniform vec4 inputSize;
uniform vec4 outputFrame;
varying vec2 vTextureCoord;
varying vec2 vScreenUV;
varying vec2 vScreenPx;
void main(void) {
    vec2 position = aVertexPosition * max(outputFrame.zw, vec2(0.0)) + outputFrame.xy;
    gl_Position = vec4((projectionMatrix * vec3(position, 1.0)).xy, 0.0, 1.0);
    vTextureCoord = aVertexPosition * (outputFrame.zw * inputSize.zw);
    vScreenUV = aVertexPosition;
    vScreenPx = position;
}
`;

// Batch plugin fragments (used with PIXI.BatchPluginFactory).
GLSL.BATCH_OBJECT_FRAG = `
varying vec2 vTextureCoord;
varying vec4 vColor;
varying float vTextureId;
uniform sampler2D uSamplers[%count%];
void main(void) {
    vec4 color;
    %forloop%
    if (color.a < 0.5) discard;
    gl_FragColor = vec4(vColor.rgb, 1.0);
}
`;

GLSL.BATCH_SILHOUETTE_FRAG = `
varying vec2 vTextureCoord;
varying vec4 vColor;
varying float vTextureId;
uniform sampler2D uSamplers[%count%];
void main(void) {
    vec4 color;
    %forloop%
    gl_FragColor = vColor * color.a;
}
`;

GLSL.BATCH_NORMAL_FRAG = `
varying vec2 vTextureCoord;
varying vec4 vColor;
varying float vTextureId;
uniform sampler2D uSamplers[%count%];
void main(void) {
    vec4 color;
    %forloop%
    if (color.a < 0.5) discard;
    gl_FragColor = vec4(color.rgb / color.a, 1.0);
}
`;

// Tile coverage shader: same interface as RPG Maker's tilemap shader, but it
// writes a flat code color wherever a tile pixel is opaque.
GLSL.TILE_VERT = `
attribute float aTextureId;
attribute vec4 aFrame;
attribute vec2 aSource;
attribute vec2 aDest;
uniform mat3 uProjectionMatrix;
varying vec4 vFrame;
varying vec2 vTextureCoord;
varying float vTextureId;
void main(void) {
    vec3 position = uProjectionMatrix * vec3(aDest, 1.0);
    gl_Position = vec4(position, 1.0);
    vFrame = aFrame;
    vTextureCoord = aSource;
    vTextureId = aTextureId;
}
`;

GLSL.TILE_FRAG = GLSL.PRECISION + `
varying vec4 vFrame;
varying vec2 vTextureCoord;
varying float vTextureId;
uniform sampler2D uSampler0;
uniform sampler2D uSampler1;
uniform sampler2D uSampler2;
uniform vec4 uOutColor;
void main(void) {
    vec2 textureCoord = clamp(vTextureCoord, vFrame.xy, vFrame.zw);
    int textureId = int(vTextureId);
    vec4 color = vec4(0.0);
    if (textureId < 0) {
        color = vec4(0.0);
    } else if (textureId == 0) {
        color = texture2D(uSampler0, textureCoord / 2048.0);
    } else if (textureId == 1) {
        color = texture2D(uSampler1, textureCoord / 2048.0);
    } else if (textureId == 2) {
        color = texture2D(uSampler2, textureCoord / 2048.0);
    }
    if (color.a < 0.5) discard;
    gl_FragColor = uOutColor;
}
`;

// Shared helpers: auto depth curve, screen -> map conversion, region lookup.
GLSL.DEPTH_CHUNK = `
uniform vec4 uDepthCurve;    // focalDepth, nearDepth, farDepth, curve
uniform vec4 uDepthCam;      // focalY, strength, autoY, zoom
uniform vec2 uViewSize;      // view size in pixels
uniform mat3 uScreenToLocal; // screen pixel -> world-local pixel (unzoomed)
uniform vec4 uMapInfo;       // tilemap origin x/y (px), tile width/height
uniform vec4 uMapSize;       // map width/height (tiles), loopX, loopY
uniform sampler2D uRegion;   // per tile: r depth*mask, g emissive/4, b light blocker, a mask

float autoDepth(float camY) {
    float F = uDepthCurve.x;
    if (uDepthCam.z < 0.5) return F;
    float fy = uDepthCam.x;
    float c = max(0.2, uDepthCurve.w);
    if (camY >= fy) {
        float u = clamp((camY - fy) / max(1.0 - fy, 0.01), 0.0, 1.0);
        return clamp(F - (F - uDepthCurve.y) * pow(u, c) * uDepthCam.y, 0.0, 100.0);
    }
    float u2 = clamp((fy - camY) / max(fy, 0.01), 0.0, 1.0);
    return clamp(F + (uDepthCurve.z - F) * pow(u2, c) * uDepthCam.y, 0.0, 100.0);
}
vec2 screenToLocal(vec2 px) {
    return (uScreenToLocal * vec3(px, 1.0)).xy;
}
vec2 localToTile(vec2 local) {
    return (local + uMapInfo.xy) / uMapInfo.zw;
}
vec2 wrapTile(vec2 t) {
    if (uMapSize.z > 0.5) t.x = mod(t.x, uMapSize.x);
    if (uMapSize.w > 0.5) t.y = mod(t.y, uMapSize.y);
    return t;
}
vec4 regionAt(vec2 tile) {
    return texture2D(uRegion, wrapTile(tile) / uMapSize.xy);
}
`;

// Stamps the opaque pixels of a (tiling) layer into the object buffer.
GLSL.STAMP_FRAG = GLSL.PRECISION + `
varying vec2 vScreenPx;
uniform sampler2D uLayerTex;
uniform mat3 uScreenToTex;  // screen pixel -> texture uv (unwrapped)
uniform vec4 uStampCfg;     // repeat x, repeat y, fill (skip texture test), unused
uniform vec4 uFrameUV;      // texture frame inside its base texture (uv)
uniform vec4 uOutColor;
void main(void) {
    vec2 uv = (uScreenToTex * vec3(vScreenPx, 1.0)).xy;
    if (uStampCfg.x > 0.5) uv.x = fract(uv.x);
    else if (uv.x < 0.0 || uv.x > 1.0) discard;
    if (uStampCfg.y > 0.5) uv.y = fract(uv.y);
    else if (uv.y < 0.0 || uv.y > 1.0) discard;
    if (uStampCfg.z < 0.5) {
        vec4 c = texture2D(uLayerTex, uFrameUV.xy + uv * uFrameUV.zw);
        if (c.a < 0.5) discard;
    }
    gl_FragColor = uOutColor;
}
`;

// Object buffer + depth field -> resolved depth buffer.
// Output: r = depth/100, g = emissive/4, b = 1 for sprites, a = rim weight.
GLSL.RESOLVE_FRAG = GLSL.PRECISION + `
varying vec2 vTextureCoord;
varying vec2 vScreenUV;
varying vec2 vScreenPx;
uniform sampler2D uObj;
uniform vec4 uResolve; // upperTileOffset, backgroundDepth, emptyIsBackground, unused
` + GLSL.DEPTH_CHUNK + `
void main(void) {
    vec4 o = texture2D(uObj, vScreenUV);
    float code = floor(o.b * 255.0 + 0.5);
    float kind = floor(code / 64.0);
    float low = code - kind * 64.0;
    float depth = 50.0;
    float emissive = 0.0;
    float sprite = 0.0;
    float rim = 0.0;
    if (kind > 1.5 && kind < 2.5) {
        depth = o.r * 100.0;
        emissive = o.g * 4.0;
        sprite = 1.0;
        rim = low / 63.0;
    } else if (kind > 0.5 && kind < 1.5) {
        depth = o.r * 100.0;
        emissive = o.g * 4.0;
    } else if (kind < 0.5 && uResolve.z > 0.5) {
        depth = uResolve.y;
    } else {
        vec2 local = screenToLocal(vScreenPx);
        float camY = local.y * uDepthCam.w / uViewSize.y;
        depth = autoDepth(camY);
        vec4 reg = regionAt(localToTile(local));
        if (reg.a > 0.002) depth = mix(depth, reg.r / reg.a * 100.0, clamp(reg.a, 0.0, 1.0));
        emissive = reg.g * 4.0;
        if (kind > 2.5 && low > 0.5) depth += uResolve.x;
    }
    gl_FragColor = vec4(clamp(depth / 100.0, 0.0, 1.0), clamp(emissive / 4.0, 0.0, 1.0), sprite, rim);
}
`;

// Separable gaussian (9-tap quality with 5 linear-filtered samples).
GLSL.BLUR_FRAG = GLSL.PRECISION + `
varying vec2 vScreenUV;
uniform sampler2D uTex;
uniform vec2 uDir;
void main(void) {
    vec4 c = texture2D(uTex, vScreenUV) * 0.2270270270;
    c += texture2D(uTex, vScreenUV + uDir * 1.3846153846) * 0.3162162162;
    c += texture2D(uTex, vScreenUV - uDir * 1.3846153846) * 0.3162162162;
    c += texture2D(uTex, vScreenUV + uDir * 3.2307692308) * 0.0702702703;
    c += texture2D(uTex, vScreenUV - uDir * 3.2307692308) * 0.0702702703;
    gl_FragColor = c;
}
`;

// Ambient + sun light (with character shadows and optional normal maps).
GLSL.LIGHT_BASE_FRAG = GLSL.PRECISION + `
varying vec2 vScreenUV;
uniform sampler2D uShadow;   // r sun shadows, g light shadows, b contact shadows
uniform sampler2D uNormal;
uniform vec3 uAmbient;
uniform vec3 uSun;
uniform vec3 uSunDir;        // direction to the sun (screen x/y, z towards the camera)
uniform vec4 uShadowCfg;     // sun shadow strength, unused, contact strength, use normals
uniform float uLightScale;   // 1 / storage range
void main(void) {
    vec4 sh = texture2D(uShadow, vScreenUV);
    float ndl = uSunDir.z;
    if (uShadowCfg.w > 0.5) {
        vec4 n = texture2D(uNormal, vScreenUV);
        if (n.a > 0.5) {
            vec3 N = normalize(vec3(n.r * 2.0 - 1.0, 1.0 - n.g * 2.0, n.b * 2.0 - 1.0));
            ndl = max(dot(N, uSunDir), 0.0);
        }
    }
    vec3 sun = uSun * ndl * (1.0 - sh.r * uShadowCfg.x);
    vec3 light = (uAmbient + sun) * (1.0 - sh.b * uShadowCfg.z);
    gl_FragColor = vec4(light * uLightScale, 1.0);
}
`;

// Point / spot lights, drawn as one batch of quads with additive blending.
GLSL.LIGHT_VERT = `
attribute vec2 aPos;
attribute vec2 aCenter;
attribute vec4 aParams;
attribute vec4 aColor;
attribute vec4 aSpot;
attribute vec4 aExtra;
uniform mat3 projectionMatrix;
varying vec2 vPx;
varying vec2 vCenter;
varying vec4 vParams;
varying vec4 vColor;
varying vec4 vSpot;
varying vec4 vExtra;
void main(void) {
    gl_Position = vec4((projectionMatrix * vec3(aPos, 1.0)).xy, 0.0, 1.0);
    vPx = aPos;
    vCenter = aCenter;
    vParams = aParams;
    vColor = aColor;
    vSpot = aSpot;
    vExtra = aExtra;
}
`;

GLSL.LIGHT_FRAG = GLSL.PRECISION + `
#define OCC_STEPS %STEPS%
varying vec2 vPx;
varying vec2 vCenter;
varying vec4 vParams;   // radius px, intensity, falloff, softness
varying vec4 vColor;    // rgb, type (0 point, 1 spot)
varying vec4 vSpot;     // direction x/y, cos outer, cos inner
varying vec4 vExtra;    // depth/100 (<0 = any), depth range/100, casts tile shadows, height px
uniform sampler2D uShadow;
uniform sampler2D uNormal;
uniform sampler2D uDepth;
uniform vec4 uFrameRect;
uniform vec4 uLightCfg; // use normals, use depth, use occlusion, light shadow strength
uniform vec2 uOcc;      // occlusion strength, zoom
uniform float uLightScale;
` + GLSL.DEPTH_CHUNK + `
float occlusion(vec2 px, vec2 lightPx) {
    vec2 a = localToTile(screenToLocal(px));
    vec2 b = localToTile(screenToLocal(lightPx));
    vec2 delta = b - a;
    float len = length(delta);
    if (len < 0.6) return 1.0;
    float vis = 1.0;
    for (int i = 1; i <= OCC_STEPS; i++) {
        float t = float(i) / float(OCC_STEPS + 1);
        float da = t * len;
        float db = (1.0 - t) * len;
        if (da < 0.55 || db < 0.55) continue;
        float o = regionAt(a + delta * t).b;
        vis = min(vis, 1.0 - o);
    }
    return mix(1.0, vis, uOcc.x);
}
void main(void) {
    vec2 d = vPx - vCenter;
    float dist = length(d) / vParams.x;
    if (dist >= 1.0) discard;
    // Smooth falloff that always reaches zero at the radius (no hard circles).
    // Softness shrinks the bright core, falloff shapes the curve.
    float core = (1.0 - vParams.w) * 0.5;
    float att = pow(1.0 - smoothstep(core, 1.0, dist), vParams.z);
    if (vColor.a > 0.5) {
        vec2 dir = d / max(length(d), 0.0001);
        att *= smoothstep(vSpot.z, vSpot.w, dot(dir, vSpot.xy));
    }
    vec2 uv = (vPx - uFrameRect.xy) / uFrameRect.zw;
    float ndl = 1.0;
    if (uLightCfg.x > 0.5) {
        vec4 n = texture2D(uNormal, uv);
        if (n.a > 0.5) {
            vec3 N = normalize(vec3(n.r * 2.0 - 1.0, 1.0 - n.g * 2.0, n.b * 2.0 - 1.0));
            vec3 L = normalize(vec3(-d, vExtra.w * uOcc.y));
            ndl = max(dot(N, L), 0.0) * 1.3;
        }
    }
    if (uLightCfg.y > 0.5 && vExtra.x >= 0.0) {
        float diff = abs(texture2D(uDepth, uv).r - vExtra.x);
        att *= 1.0 - smoothstep(vExtra.y * 0.6, vExtra.y, diff);
    }
    if (uLightCfg.z > 0.5 && vExtra.z > 0.5) att *= occlusion(vPx, vCenter);
    att *= 1.0 - texture2D(uShadow, uv).g * uLightCfg.w;
    gl_FragColor = vec4(vColor.rgb * (vParams.y * att * ndl * uLightScale), 0.0);
}
`;

// Lighting, atmosphere, fog and overlay - shared by the DOF input pass and the final pass.
GLSL.SHADE_CHUNK = `
uniform sampler2D uSampler;   // the rendered world (premultiplied alpha)
uniform sampler2D uDepthTex;  // resolved depth buffer
uniform sampler2D uLightTex;  // light buffer
uniform sampler2D uOverlay;   // unlit overlay (premultiplied)
uniform sampler2D uNoise;     // tileable noise
uniform vec4 uLightOn;        // lighting weight, light storage range, emissive weight, overlay on
uniform vec4 uTintS;          // shadow tint (rgb), amount
uniform vec4 uTintH;          // highlight tint (rgb), amount
uniform vec4 uAtmoA;          // haze color (rgb), haze amount
uniform vec4 uAtmoB;          // far desaturate, far contrast, far brighten, far temperature
uniform vec4 uAtmoC;          // near saturate, near contrast, near darken, weight
uniform vec4 uFocal;          // focal depth, unused...
uniform vec4 uFogColor;       // rgb, lit amount
uniform vec4 uFogCfg;         // softness, noise, depth fog, weight
uniform vec4 uFog0;           // near: opacity, depth, scale, enabled
uniform vec4 uFog1;           // mid
uniform vec4 uFog2;           // far
uniform vec4 uFogOffA;        // near offset xy, mid offset xy (pixels)
uniform vec4 uFogOffB;        // far offset xy, octaves, unused

const vec3 LUMA = vec3(0.299, 0.587, 0.114);

vec3 applyAtmosphere(vec3 c, float depth) {
    if (uAtmoC.w <= 0.0) return c;
    float F = uFocal.x;
    float far = smoothstep(F, 100.0, depth) * uAtmoC.w;
    float near = (1.0 - smoothstep(0.0, F, depth)) * uAtmoC.w;
    float l = dot(c, LUMA);
    c = mix(vec3(l), c, 1.0 - far * uAtmoB.x + near * uAtmoC.x);
    c = (c - 0.5) * (1.0 - far * uAtmoB.y + near * uAtmoC.y) + 0.5;
    c += far * uAtmoB.z;
    c *= 1.0 - near * uAtmoC.z;
    c *= vec3(1.0 + far * uAtmoB.w * 0.35, 1.0, 1.0 - far * uAtmoB.w * 0.35);
    c = mix(c, uAtmoA.rgb, far * uAtmoA.a);
    return max(c, 0.0);
}

float fogNoise(vec2 p) {
    float n = texture2D(uNoise, p).r;
    if (uFogOffB.z > 1.5) n = n * 0.62 + texture2D(uNoise, p * 2.03 + vec2(0.37, 0.11)).g * 0.38;
    if (uFogOffB.z > 2.5) n = n * 0.82 + texture2D(uNoise, p * 4.11 + vec2(0.71, 0.53)).b * 0.18;
    return n;
}

float fogLayer(vec4 L, vec2 off, float depth, vec2 px) {
    if (L.w < 0.5 || L.x <= 0.0) return 0.0;
    float soft = max(uFogCfg.x, 0.5);
    float cover = smoothstep(L.y - soft, L.y + soft, depth);
    if (cover <= 0.0) return 0.0;
    float n = fogNoise((px + off) / (256.0 * max(L.z, 0.05)));
    float patch = mix(1.0, smoothstep(0.2, 0.8, n) * 1.5, uFogCfg.y);
    return clamp(L.x * cover * patch, 0.0, 1.0);
}

vec3 applyFog(vec3 c, float depth, vec2 px, vec3 light) {
    if (uFogCfg.w <= 0.0) return c;
    vec3 fogC = uFogColor.rgb * mix(vec3(1.0), clamp(light, 0.0, 1.5), uFogColor.a);
    c = mix(c, fogC, fogLayer(uFog2, uFogOffB.xy, depth, px) * uFogCfg.w);
    c = mix(c, fogC, fogLayer(uFog1, uFogOffA.zw, depth, px) * uFogCfg.w);
    c = mix(c, fogC, fogLayer(uFog0, uFogOffA.xy, depth, px) * uFogCfg.w);
    if (uFogCfg.z > 0.0) {
        float df = 1.0 - exp(-max(depth - uFocal.x, 0.0) * uFogCfg.z * 0.05);
        c = mix(c, fogC, df * uFogCfg.w);
    }
    return c;
}

// src: premultiplied world color; returns the lit color (straight alpha).
vec3 shadeColor(vec4 src, vec2 uvScr, vec2 px, out vec4 dd) {
    vec3 albedo = src.a > 0.0001 ? src.rgb / src.a : vec3(0.0);
    dd = texture2D(uDepthTex, uvScr);
    float depth = dd.r * 100.0;
    vec3 light = vec3(1.0);
    if (uLightOn.x > 0.0) {
        light = texture2D(uLightTex, uvScr).rgb * uLightOn.y;
        // Soft knee: overlapping lights brighten smoothly instead of clipping to white.
        vec3 over = max(light - 0.8, 0.0);
        light = min(light, vec3(0.8)) + over / (1.0 + over * 1.6);
        float L = dot(light, LUMA);
        light *= mix(vec3(1.0), uTintS.rgb, uTintS.a * (1.0 - smoothstep(0.2, 0.85, L)));
        light *= mix(vec3(1.0), uTintH.rgb, uTintH.a * smoothstep(0.85, 1.35, L));
        light = mix(vec3(1.0), light, uLightOn.x);
    }
    vec3 c = albedo * light;
    float em = dd.g * 4.0 * uLightOn.z;
    if (em > 0.0) c = mix(c, albedo * max(em, 1.0), clamp(em, 0.0, 1.0));
    c = applyAtmosphere(c, depth);
    c = applyFog(c, depth, px, light);
    if (uLightOn.w > 0.5) {
        vec4 ov = texture2D(uOverlay, uvScr);
        c = ov.rgb + c * (1.0 - clamp(ov.a, 0.0, 1.0));
    }
    return c;
}
`;

// Half-resolution DOF input: lit color + signed circle of confusion.
GLSL.DOF_PREP_FRAG = GLSL.PRECISION + `
varying vec2 vTextureCoord;
varying vec2 vScreenUV;
varying vec2 vScreenPx;
uniform vec2 uInTexel;  // input texel size (in input uv)
uniform vec4 uDof;      // focus, focus range, near transition, far transition
uniform vec4 uDof2;     // near blur, far blur, weight, storage scale (1/range)
` + GLSL.SHADE_CHUNK + `
void main(void) {
    vec2 o = uInTexel * 0.5;
    vec4 src = texture2D(uSampler, vTextureCoord + vec2(-o.x, -o.y));
    src += texture2D(uSampler, vTextureCoord + vec2(o.x, -o.y));
    src += texture2D(uSampler, vTextureCoord + vec2(-o.x, o.y));
    src += texture2D(uSampler, vTextureCoord + vec2(o.x, o.y));
    src *= 0.25;
    vec4 dd;
    vec3 c = shadeColor(src, vScreenUV, vScreenPx, dd);
    float dz = dd.r * 100.0 - uDof.x;
    float far = smoothstep(uDof.y, uDof.y + max(uDof.w, 0.01), dz) * uDof2.y;
    float near = smoothstep(uDof.y, uDof.y + max(uDof.z, 0.01), -dz) * uDof2.x;
    float coc = clamp((far - near) * uDof2.z, -1.0, 1.0);
    gl_FragColor = vec4(c * uDof2.w, coc * 0.5 + 0.5);
}
`;

// Depth-aware gather blur (scatter-as-gather). Samples only contribute if
// their own blur disc reaches this pixel, and background samples cannot
// spill over sharper foreground pixels - this avoids halos.
GLSL.DOF_GATHER_FRAG = GLSL.PRECISION + `
#define TAPS %TAPS%
varying vec2 vScreenUV;
uniform sampler2D uPrep;
uniform vec2 uTexel;     // prep texel size (uv)
uniform float uMaxR;     // max blur radius in prep pixels
uniform vec4 uBokeh;     // highlight weight, threshold, unused, storage range
void main(void) {
    vec4 c0 = texture2D(uPrep, vScreenUV);
    float coc0 = c0.a * 2.0 - 1.0;
    float size0 = abs(coc0) * uMaxR;
    vec3 acc = c0.rgb;
    float wsum = 1.0;
    float nearSpill = 0.0;
    for (int i = 0; i < TAPS; i++) {
        float fi = float(i);
        float r = sqrt((fi + 0.5) / float(TAPS)) * uMaxR;
        float th = fi * 2.39996323;
        vec2 off = vec2(cos(th), sin(th)) * r;
        vec4 s = texture2D(uPrep, vScreenUV + off * uTexel);
        float coc = s.a * 2.0 - 1.0;
        float size = abs(coc) * uMaxR;
        if (coc > coc0) size = min(size, size0 * 2.0 + 0.5);
        float m = smoothstep(r - 0.5, r + 0.5, size);
        float lum = dot(s.rgb * uBokeh.w, vec3(0.299, 0.587, 0.114));
        float bw = 1.0 + uBokeh.x * smoothstep(uBokeh.y, uBokeh.y + 0.3, lum) * smoothstep(1.0, 3.0, size);
        acc += mix(acc / wsum, s.rgb, m) * bw;
        wsum += bw;
        if (coc < coc0 - 0.05) nearSpill += m;
    }
    float blend = max(smoothstep(0.3, 1.2, size0), clamp(nearSpill * 3.0 / float(TAPS), 0.0, 1.0));
    gl_FragColor = vec4(acc / wsum, blend);
}
`;

// Bokeh highlight detection: brightest blurred highlight per grid cell.
// MODE 0 writes color + coc, MODE 1 writes the highlight position in the cell.
GLSL.BOKEH_POOL_FRAG = GLSL.PRECISION + `
#define MODE %MODE%
varying vec2 vScreenUV;
uniform sampler2D uPrep;
uniform vec2 uGrid;
uniform vec4 uBokeh;  // threshold, min coc, storage range, unused
void main(void) {
    vec2 cell = floor(vScreenUV * uGrid);
    vec4 best = vec4(0.0);
    vec2 bestPos = vec2(0.5);
    float bestScore = 0.0;
    for (int y = 0; y < 4; y++) {
        for (int x = 0; x < 4; x++) {
            vec2 local = (vec2(float(x), float(y)) + 0.5) / 4.0;
            vec4 s = texture2D(uPrep, (cell + local) / uGrid);
            float coc = abs(s.a * 2.0 - 1.0);
            float lum = dot(s.rgb * uBokeh.z, vec3(0.299, 0.587, 0.114));
            float score = smoothstep(uBokeh.x, uBokeh.x + 0.25, lum) * smoothstep(uBokeh.y, uBokeh.y + 0.2, coc);
            if (score > bestScore) {
                bestScore = score;
                best = s;
                bestPos = local;
            }
        }
    }
    if (MODE == 0) gl_FragColor = best;
    else gl_FragColor = vec4(bestPos, bestScore, bestScore > 0.01 ? 1.0 : 0.0);
}
`;

GLSL.BOKEH_VERT = `
attribute vec2 aCell;
attribute vec2 aCorner;
uniform mat3 projectionMatrix;
uniform vec4 uFrame;
uniform vec2 uGrid;
uniform float uMaxR;
varying vec2 vCellUV;
varying vec2 vPx;
void main(void) {
    vec2 cellSize = uFrame.zw / uGrid;
    vec2 center = uFrame.xy + (aCell + 0.5) * cellSize;
    vec2 pos = center + aCorner * (uMaxR + cellSize * 0.5);
    gl_Position = vec4((projectionMatrix * vec3(pos, 1.0)).xy, 0.0, 1.0);
    vCellUV = (aCell + 0.5) / uGrid;
    vPx = pos;
}
`;

GLSL.BOKEH_FRAG = GLSL.PRECISION + `
varying vec2 vCellUV;
varying vec2 vPx;
uniform sampler2D uGridColor;
uniform sampler2D uGridPos;
uniform vec4 uFrame;
uniform vec2 uGrid;
uniform vec4 uBokeh;  // intensity, size, max radius px, storage range
void main(void) {
    vec4 p = texture2D(uGridPos, vCellUV);
    if (p.a < 0.5) discard;
    vec4 c = texture2D(uGridColor, vCellUV);
    vec2 cellSize = uFrame.zw / uGrid;
    vec2 center = uFrame.xy + (floor(vCellUV * uGrid) + p.xy) * cellSize;
    float coc = abs(c.a * 2.0 - 1.0);
    float r = coc * uBokeh.z * uBokeh.y;
    if (r < 2.0) discard;
    float d = length(vPx - center) / r;
    if (d > 1.0) discard;
    float edge = 1.0 - smoothstep(0.8, 1.0, d);
    float ring = 0.8 + 0.35 * smoothstep(0.5, 0.95, d);
    float energy = clamp(12.0 / (r * r), 0.05, 1.0);
    float k = edge * ring * p.b * uBokeh.x * (0.3 + energy);
    gl_FragColor = vec4(c.rgb * k, k * 0.6);
}
`;

// Bloom: bright pass + dual filter (down / up) blur.
GLSL.BLOOM_BRIGHT_FRAG = GLSL.PRECISION + `
varying vec2 vScreenUV;
uniform sampler2D uSrc;
uniform sampler2D uDepthTex;
uniform vec4 uBloom;   // threshold, knee, emissive boost, source range
uniform float uOutScale;
void main(void) {
    vec3 c = texture2D(uSrc, vScreenUV).rgb * uBloom.w;
    float br = max(c.r, max(c.g, c.b));
    float knee = max(uBloom.y, 0.0001);
    float soft = clamp(br - uBloom.x + knee, 0.0, 2.0 * knee);
    soft = soft * soft / (4.0 * knee);
    float contrib = max(soft, br - uBloom.x) / max(br, 0.0001);
    vec3 b = c * contrib;
    float em = texture2D(uDepthTex, vScreenUV).g * 4.0;
    b += c * min(em, 2.0) * 0.6 * uBloom.z;
    gl_FragColor = vec4(b * uOutScale, 1.0);
}
`;

GLSL.BLOOM_DOWN_FRAG = GLSL.PRECISION + `
varying vec2 vScreenUV;
uniform sampler2D uSrc;
uniform vec2 uTexel;
void main(void) {
    vec4 c = texture2D(uSrc, vScreenUV) * 4.0;
    c += texture2D(uSrc, vScreenUV - uTexel);
    c += texture2D(uSrc, vScreenUV + uTexel);
    c += texture2D(uSrc, vScreenUV + vec2(uTexel.x, -uTexel.y));
    c += texture2D(uSrc, vScreenUV - vec2(uTexel.x, -uTexel.y));
    gl_FragColor = c / 8.0;
}
`;

GLSL.BLOOM_UP_FRAG = GLSL.PRECISION + `
varying vec2 vScreenUV;
uniform sampler2D uSrc;
uniform vec2 uTexel;
uniform float uGain;
void main(void) {
    vec4 c = texture2D(uSrc, vScreenUV + vec2(-uTexel.x * 2.0, 0.0));
    c += texture2D(uSrc, vScreenUV + vec2(-uTexel.x, uTexel.y)) * 2.0;
    c += texture2D(uSrc, vScreenUV + vec2(0.0, uTexel.y * 2.0));
    c += texture2D(uSrc, vScreenUV + vec2(uTexel.x, uTexel.y)) * 2.0;
    c += texture2D(uSrc, vScreenUV + vec2(uTexel.x * 2.0, 0.0));
    c += texture2D(uSrc, vScreenUV + vec2(uTexel.x, -uTexel.y)) * 2.0;
    c += texture2D(uSrc, vScreenUV + vec2(0.0, -uTexel.y * 2.0));
    c += texture2D(uSrc, vScreenUV + vec2(-uTexel.x, -uTexel.y)) * 2.0;
    gl_FragColor = vec4(c.rgb / 12.0 * uGain, 0.0);
}
`;

// Final composite.
GLSL.FINAL_FRAG = GLSL.PRECISION + `
varying vec2 vTextureCoord;
varying vec2 vScreenUV;
varying vec2 vScreenPx;
uniform sampler2D uDofTex;
uniform sampler2D uBloomTex;
uniform sampler2D uLut;
uniform vec4 uFinalCfg;   // dof on, bloom intensity, storage range, debug mode
uniform vec4 uRim;        // rgb, intensity
uniform vec4 uRim2;       // offset (depth uv), unused
uniform vec4 uGradeA;     // exposure multiplier, contrast, saturation, brightness
uniform vec4 uGradeB;     // gamma, hue (radians), temperature, tint
uniform vec4 uGradeS;     // shadow color, amount
uniform vec4 uGradeH;     // highlight color, amount
uniform vec4 uGradeC;     // weight, lut size, lut strength, lut on
uniform vec4 uVig;        // intensity, radius, softness, aspect
uniform vec4 uVigColor;   // rgb, weight
uniform vec4 uDebug;      // focus depth, focal depth, unused
` + GLSL.SHADE_CHUNK + `
vec3 hueRotate(vec3 c, float a) {
    const vec3 k = vec3(0.57735);
    float ca = cos(a);
    return c * ca + cross(k, c) * sin(a) + k * dot(k, c) * (1.0 - ca);
}

vec3 shoulder(vec3 c) {
    vec3 x = max(c - 0.8, 0.0);
    return min(c, vec3(0.8)) + 0.2 * (1.0 - exp(-x * 5.0));
}

vec3 lutLookup(vec3 c) {
    float n = uGradeC.y;
    float b = c.b * (n - 1.0);
    float b0 = floor(b);
    float b1 = min(b0 + 1.0, n - 1.0);
    float f = b - b0;
    float x = (c.r * (n - 1.0) + 0.5) / (n * n);
    float y = (c.g * (n - 1.0) + 0.5) / n;
    vec3 c0 = texture2D(uLut, vec2(x + b0 / n, y)).rgb;
    vec3 c1 = texture2D(uLut, vec2(x + b1 / n, y)).rgb;
    return mix(c0, c1, f);
}

vec3 grade(vec3 c) {
    float w = uGradeC.x;
    vec3 g = c * uGradeA.x;
    g *= vec3(1.0 + uGradeB.z * 0.35 + uGradeB.w * 0.1, 1.0 + uGradeB.z * 0.05 - uGradeB.w * 0.2, 1.0 - uGradeB.z * 0.35 + uGradeB.w * 0.1);
    g = shoulder(g);
    g = (g - 0.5) * uGradeA.y + 0.5;
    float l = dot(g, LUMA);
    g = mix(vec3(l), g, uGradeA.z);
    if (abs(uGradeB.y) > 0.0001) g = hueRotate(g, uGradeB.y);
    l = clamp(dot(g, LUMA), 0.0, 1.0);
    g += (uGradeS.rgb - dot(uGradeS.rgb, LUMA)) * uGradeS.a * (1.0 - smoothstep(0.0, 0.55, l));
    g += (uGradeH.rgb - dot(uGradeH.rgb, LUMA)) * uGradeH.a * smoothstep(0.45, 1.0, l);
    g += uGradeA.w;
    g = pow(max(g, 0.0), vec3(1.0 / max(uGradeB.x, 0.01)));
    if (uGradeC.w > 0.5) g = mix(g, lutLookup(clamp(g, 0.0, 1.0)), uGradeC.z);
    return mix(shoulder(c), g, w);
}

vec3 vignette(vec3 c, vec2 uv) {
    if (uVigColor.a <= 0.0 || uVig.x <= 0.0) return c;
    vec2 p = (uv - 0.5) * vec2(uVig.w, 1.0);
    float d = length(p) / length(vec2(uVig.w, 1.0) * 0.5);
    float v = smoothstep(uVig.y - uVig.z, uVig.y + uVig.z * 0.5, d);
    return mix(c, uVigColor.rgb, clamp(v * uVig.x * uVigColor.a, 0.0, 1.0));
}

vec3 depthColor(float d) {
    float F = uDebug.y;
    if (d < F) return mix(vec3(0.15, 0.95, 0.2), vec3(1.0, 0.15, 0.1), clamp((F - d) / max(F, 1.0), 0.0, 1.0));
    return mix(vec3(0.15, 0.95, 0.2), vec3(0.15, 0.3, 1.0), clamp((d - F) / max(100.0 - F, 1.0), 0.0, 1.0));
}

void main(void) {
    vec4 src = texture2D(uSampler, vTextureCoord);
    float alpha = src.a;
    vec4 dd;
    vec3 c = shadeColor(src, vScreenUV, vScreenPx, dd);
    float dofBlend = 0.0;
    if (uFinalCfg.x > 0.5) {
        vec4 dof = texture2D(uDofTex, vScreenUV);
        dofBlend = clamp(dof.a, 0.0, 1.0);
        c = mix(c, dof.rgb * uFinalCfg.z, dofBlend);
    }
    if (uRim.a > 0.0 && dd.b > 0.5 && dd.a > 0.0) {
        vec4 nb = texture2D(uDepthTex, vScreenUV + uRim2.xy);
        float edge = (nb.b < 0.5 || nb.r > dd.r + 0.03) ? 1.0 : 0.0;
        c += uRim.rgb * (uRim.a * dd.a * edge * (1.0 - dofBlend));
    }
    vec3 bloom = vec3(0.0);
    if (uFinalCfg.y > 0.0) {
        bloom = texture2D(uBloomTex, vScreenUV).rgb * uFinalCfg.z * uFinalCfg.y;
        c += bloom;
    }
    c = grade(c);
    c = vignette(c, vScreenUV);
    float mode = uFinalCfg.w;
    if (mode > 0.5) {
        float gray = dot(c, LUMA);
        float depth = dd.r * 100.0;
        if (mode < 1.5) {
            c = mix(vec3(gray), depthColor(depth), 0.65);
        } else if (mode < 2.5) {
            float dz = depth - uDebug.x;
            c = mix(vec3(gray * 0.35), dz < 0.0 ? vec3(1.0, 0.25, 0.2) : vec3(0.25, 0.45, 1.0), dofBlend);
        } else if (mode < 3.5) {
            c = uLightOn.x > 0.0 ? texture2D(uLightTex, vScreenUV).rgb * uLightOn.y * 0.6 : vec3(0.6);
        } else if (mode < 4.5) {
            c = vec3(gray * 0.3) + vec3(dd.b * 0.5, dd.g * 2.0, dd.a * 0.8);
        } else {
            c = bloom;
        }
    }
    gl_FragColor = vec4(c * alpha, alpha);
}
`;


//=============================================================================
// 13. GPU resources
//-----------------------------------------------------------------------------
// Render textures are cached globally (by name) and reused across scenes so
// opening the menu or changing maps does not reallocate GPU memory.
//=============================================================================

const GPU = (HD2D.GPU = {
    initialized: false,
    failed: false,
    hdr: false,
    maxTextureUnits: 8,
    rts: {},
    shaders: {},
    textures: {},

    init(renderer) {
        if (this.initialized || !renderer) return !this.failed;
        this.initialized = true;
        try {
            const gl = renderer.gl;
            this.maxTextureUnits = gl.getParameter(gl.MAX_TEXTURE_IMAGE_UNITS) || 8;
            this.quad = new PIXI.Geometry().addAttribute("aVertexPosition", [0, 0, 1, 0, 0, 1, 1, 1], 2);
            this.stateNone = new PIXI.State();
            this.stateNone.blend = false;
            this.stateNormal = new PIXI.State();
            this.stateNormal.blendMode = PIXI.BLEND_MODES.NORMAL;
            this.stateAdd = new PIXI.State();
            this.stateAdd.blendMode = PIXI.BLEND_MODES.ADD;
            this.hdr = this.probeHalfFloat(renderer);
            this.dest = new PIXI.Rectangle();
            this.buildTextures();
        } catch (e) {
            this.failed = true;
            console.error("[HD2D] GPU init failed, effects disabled.", e);
        }
        return !this.failed;
    },

    /** Checks whether half-float render targets work (HDR light / bloom). */
    probeHalfFloat(renderer) {
        try {
            const gl = renderer.gl;
            if (renderer.context.webGLVersion === 1) {
                if (!gl.getExtension("OES_texture_half_float") || !gl.getExtension("EXT_color_buffer_half_float")) return false;
                gl.getExtension("OES_texture_half_float_linear");
            } else if (!renderer.context.extensions.colorBufferFloat) {
                return false;
            }
            const rt = PIXI.RenderTexture.create({ width: 4, height: 4, type: PIXI.TYPES.HALF_FLOAT });
            renderer.renderTexture.bind(rt);
            const ok = gl.checkFramebufferStatus(gl.FRAMEBUFFER) === gl.FRAMEBUFFER_COMPLETE && gl.getError() === gl.NO_ERROR;
            renderer.renderTexture.bind(null);
            rt.destroy(true);
            return ok;
        } catch (e) {
            return false;
        }
    },

    /**
     * Returns a render texture covering the screen at a resolution scale.
     * hdr: use a half-float texture when available.
     */
    rt(name, width, height, scale, options = {}) {
        const hdr = !!options.hdr && this.hdr;
        const nearest = !!options.nearest;
        const key = name;
        let rt = this.rts[key];
        if (rt && (rt._hd2dW !== width || rt._hd2dH !== height || rt._hd2dS !== scale || rt._hd2dHdr !== hdr || rt._hd2dNearest !== nearest || !rt.baseTexture)) {
            rt.destroy(true);
            rt = null;
        }
        if (!rt) {
            const opts = {
                width, height, resolution: scale,
                scaleMode: nearest ? PIXI.SCALE_MODES.NEAREST : PIXI.SCALE_MODES.LINEAR
            };
            if (hdr) opts.type = PIXI.TYPES.HALF_FLOAT;
            rt = PIXI.RenderTexture.create(opts);
            rt.baseTexture.mipmap = PIXI.MIPMAP_MODES ? PIXI.MIPMAP_MODES.OFF : false;
            rt._hd2dW = width;
            rt._hd2dH = height;
            rt._hd2dS = scale;
            rt._hd2dHdr = hdr;
            rt._hd2dNearest = nearest;
            this.rts[key] = rt;
        }
        return rt;
    },

    /** Small render texture with an explicit pixel size (bokeh grid). */
    rtPixels(name, pw, ph, nearest) {
        let rt = this.rts[name];
        if (rt && (rt._hd2dPW !== pw || rt._hd2dPH !== ph)) {
            rt.destroy(true);
            rt = null;
        }
        if (!rt) {
            rt = PIXI.RenderTexture.create({ width: pw, height: ph, resolution: 1, scaleMode: nearest ? PIXI.SCALE_MODES.NEAREST : PIXI.SCALE_MODES.LINEAR });
            rt._hd2dPW = pw;
            rt._hd2dPH = ph;
            this.rts[name] = rt;
        }
        return rt;
    },

    releaseAll() {
        for (const key of Object.keys(this.rts)) {
            try {
                this.rts[key].destroy(true);
            } catch (e) {
                // ignore
            }
        }
        this.rts = {};
    },

    stats() {
        let count = 0;
        let bytes = 0;
        for (const rt of Object.values(this.rts)) {
            if (!rt || !rt.baseTexture) continue;
            count++;
            bytes += rt.baseTexture.realWidth * rt.baseTexture.realHeight * (rt._hd2dHdr ? 8 : 4);
        }
        return { count, mb: bytes / (1024 * 1024) };
    },

    /** Cached shader program for internal passes. */
    shader(key, vert, frag, uniforms) {
        if (!this.shaders[key]) {
            this.shaders[key] = PIXI.Shader.from(vert, frag, Object.assign({ uFrame: new Float32Array(4), uInputScale: new Float32Array([1, 1]) }, uniforms || {}));
        }
        return this.shaders[key];
    },

    /** Draws a full-frame quad with a shader into a render texture. */
    drawQuad(renderer, shader, target, frame, options = {}) {
        renderer.batch.flush();
        this.dest.x = 0;
        this.dest.y = 0;
        this.dest.width = frame.width;
        this.dest.height = frame.height;
        renderer.renderTexture.bind(target, frame, this.dest);
        if (options.clear) renderer.renderTexture.clear(options.clearColor || [0, 0, 0, 0]);
        const u = shader.uniforms;
        u.uFrame[0] = frame.x;
        u.uFrame[1] = frame.y;
        u.uFrame[2] = frame.width;
        u.uFrame[3] = frame.height;
        if (options.inputScale) {
            u.uInputScale[0] = options.inputScale[0];
            u.uInputScale[1] = options.inputScale[1];
        }
        renderer.state.set(options.blend === "add" ? this.stateAdd : options.blend === "normal" ? this.stateNormal : this.stateNone);
        renderer.shader.bind(shader);
        renderer.geometry.bind(this.quad, shader);
        renderer.geometry.draw(PIXI.DRAW_MODES.TRIANGLE_STRIP, 4, 0);
    },

    /** Binds a render texture for drawing sprites/geometry in screen coordinates. */
    bindTarget(renderer, target, frame, clearColor) {
        renderer.batch.flush();
        this.dest.x = 0;
        this.dest.y = 0;
        this.dest.width = frame.width;
        this.dest.height = frame.height;
        renderer.renderTexture.bind(target, frame, this.dest);
        if (clearColor) renderer.renderTexture.clear(clearColor);
    },

    dataTexture(data, w, h, options = {}) {
        const base = PIXI.BaseTexture.fromBuffer(data, w, h, {
            scaleMode: options.nearest ? PIXI.SCALE_MODES.NEAREST : PIXI.SCALE_MODES.LINEAR,
            wrapMode: options.repeat ? PIXI.WRAP_MODES.REPEAT : PIXI.WRAP_MODES.CLAMP,
            alphaMode: PIXI.ALPHA_MODES.NPM,
            mipmap: PIXI.MIPMAP_MODES.OFF
        });
        return new PIXI.Texture(base);
    },

    buildTextures() {
        const one = rgba => this.dataTexture(new Uint8Array(rgba), 1, 1, { nearest: true });
        this.textures.neutralDepth = one([128, 0, 0, 0]);
        this.textures.black = one([0, 0, 0, 0]);
        this.textures.white = one([255, 255, 255, 255]);
        this.textures.lightNeutral = one([255, 255, 255, 255]);
        this.textures.noise = this.buildNoise(128);
        this.buildAtlas();
    },

    /** Tileable value-noise texture: r = large blobs, g = medium, b = fine, a = random. */
    buildNoise(size) {
        const data = new Uint8Array(size * size * 4);
        let seed = 12345;
        const rnd = () => {
            seed = (seed * 1664525 + 1013904223) >>> 0;
            return seed / 4294967296;
        };
        const lattice = p => {
            const l = new Float32Array(p * p);
            for (let i = 0; i < l.length; i++) l[i] = rnd();
            return l;
        };
        const sample = (l, p, x, y) => {
            const fx = (x / size) * p;
            const fy = (y / size) * p;
            const x0 = Math.floor(fx);
            const y0 = Math.floor(fy);
            const tx = fx - x0;
            const ty = fy - y0;
            const sx = tx * tx * (3 - 2 * tx);
            const sy = ty * ty * (3 - 2 * ty);
            const g = (i, j) => l[(((j % p) + p) % p) * p + (((i % p) + p) % p)];
            const a = U.lerp(g(x0, y0), g(x0 + 1, y0), sx);
            const b = U.lerp(g(x0, y0 + 1), g(x0 + 1, y0 + 1), sx);
            return U.lerp(a, b, sy);
        };
        const L = [4, 8, 16, 32].map(p => ({ p, l: lattice(p) }));
        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const i = (y * size + x) * 4;
                const n4 = sample(L[0].l, 4, x, y);
                const n8 = sample(L[1].l, 8, x, y);
                const n16 = sample(L[2].l, 16, x, y);
                const n32 = sample(L[3].l, 32, x, y);
                data[i] = Math.round(U.saturate(n4 * 0.6 + n8 * 0.3 + n16 * 0.1) * 255);
                data[i + 1] = Math.round(U.saturate(n8 * 0.6 + n16 * 0.3 + n32 * 0.1) * 255);
                data[i + 2] = Math.round(U.saturate(n16 * 0.6 + n32 * 0.4) * 255);
                data[i + 3] = Math.round(rnd() * 255);
            }
        }
        return this.dataTexture(data, size, size, { repeat: true });
    },

    /**
     * Procedural particle / glow atlas. Small sprites are drawn in four blur
     * levels (rows) so particles can look out of focus without filters.
     */
    buildAtlas() {
        const canvas = document.createElement("canvas");
        canvas.width = 512;
        canvas.height = 448;
        const ctx = canvas.getContext("2d");
        const frames = {};
        const canBlur = typeof ctx.filter === "string";
        const radial = (cx, cy, r, stops) => {
            const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
            for (const [o, a] of stops) g.addColorStop(o, "rgba(255,255,255," + a + ")");
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(cx, cy, r, 0, Math.PI * 2);
            ctx.fill();
        };
        const small = {
            dot: { x: 0, w: 18, h: 18, draw: (cx, cy) => radial(cx, cy, 7, [[0, 1], [0.45, 0.9], [1, 0]]) },
            spark: { x: 22, w: 14, h: 14, draw: (cx, cy) => radial(cx, cy, 5, [[0, 1], [0.3, 1], [1, 0]]) },
            flake: {
                x: 40, w: 18, h: 18, draw: (cx, cy) => {
                    radial(cx, cy, 6, [[0, 1], [0.5, 0.85], [1, 0]]);
                }
            },
            sparkle: {
                x: 62, w: 22, h: 22, draw: (cx, cy) => {
                    ctx.fillStyle = "rgba(255,255,255,1)";
                    ctx.beginPath();
                    ctx.moveTo(cx, cy - 9);
                    ctx.quadraticCurveTo(cx + 1.2, cy - 1.2, cx + 9, cy);
                    ctx.quadraticCurveTo(cx + 1.2, cy + 1.2, cx, cy + 9);
                    ctx.quadraticCurveTo(cx - 1.2, cy + 1.2, cx - 9, cy);
                    ctx.quadraticCurveTo(cx - 1.2, cy - 1.2, cx, cy - 9);
                    ctx.fill();
                    radial(cx, cy, 4, [[0, 1], [1, 0]]);
                }
            },
            leaf: {
                x: 88, w: 18, h: 12, draw: (cx, cy) => {
                    ctx.fillStyle = "rgba(255,255,255,1)";
                    ctx.beginPath();
                    ctx.ellipse(cx, cy, 7, 3.5, 0.3, 0, Math.PI * 2);
                    ctx.fill();
                }
            },
            petal: {
                x: 110, w: 16, h: 12, draw: (cx, cy) => {
                    ctx.fillStyle = "rgba(255,255,255,1)";
                    ctx.beginPath();
                    ctx.ellipse(cx, cy, 5.5, 3.5, 0, 0, Math.PI * 2);
                    ctx.fill();
                }
            },
            streak: {
                x: 130, w: 8, h: 40, draw: (cx, cy) => {
                    const g = ctx.createLinearGradient(cx, cy - 18, cx, cy + 18);
                    g.addColorStop(0, "rgba(255,255,255,0)");
                    g.addColorStop(0.7, "rgba(255,255,255,0.8)");
                    g.addColorStop(1, "rgba(255,255,255,0.2)");
                    ctx.fillStyle = g;
                    ctx.fillRect(cx - 1.5, cy - 18, 3, 36);
                }
            }
        };
        const blurs = [0, 1, 2, 3.5];
        for (let level = 0; level < 4; level++) {
            const top = level * 44;
            for (const name of Object.keys(small)) {
                const s = small[name];
                const cx = s.x + s.w / 2 + 2;
                const cy = top + 22;
                ctx.save();
                if (canBlur && blurs[level] > 0) ctx.filter = "blur(" + blurs[level] + "px)";
                s.draw(cx, cy);
                ctx.restore();
                const pad = level === 0 ? 0 : Math.ceil(blurs[level] * 2);
                frames[name + level] = new PIXI.Rectangle(s.x + 2 - pad / 2, top + 22 - s.h / 2 - pad / 2, s.w + pad, s.h + pad);
            }
        }
        // Large soft sprites (no blur levels).
        radial(32, 208, 32, [[0, 1], [0.15, 0.75], [0.45, 0.25], [1, 0]]);
        frames.glow = new PIXI.Rectangle(0, 176, 64, 64);
        ctx.save();
        ctx.translate(100, 192);
        ctx.scale(1, 0.5);
        radial(0, 0, 30, [[0, 1], [0.55, 0.65], [1, 0]]);
        ctx.restore();
        frames.blob = new PIXI.Rectangle(70, 176, 60, 32);
        for (let i = 0; i < 9; i++) {
            const a = (i / 9) * Math.PI * 2;
            const r = i === 0 ? 0 : 24;
            radial(200 + Math.cos(a) * r * 0.9, 240 + Math.sin(a) * r * 0.6, i === 0 ? 46 : 30, [[0, 0.35], [0.6, 0.15], [1, 0]]);
        }
        frames.puff = new PIXI.Rectangle(136, 176, 128, 128);
        // The light-shaft texture is masked on its own canvas: "destination-in"
        // would otherwise erase everything else already drawn into the atlas.
        const beamCanvas = document.createElement("canvas");
        beamCanvas.width = 64;
        beamCanvas.height = 256;
        const bctx = beamCanvas.getContext("2d");
        const beam = bctx.createLinearGradient(0, 0, 64, 0);
        beam.addColorStop(0, "rgba(255,255,255,0)");
        beam.addColorStop(0.5, "rgba(255,255,255,1)");
        beam.addColorStop(1, "rgba(255,255,255,0)");
        bctx.fillStyle = beam;
        bctx.fillRect(0, 0, 64, 256);
        bctx.globalCompositeOperation = "destination-in";
        const fade = bctx.createLinearGradient(0, 0, 0, 256);
        fade.addColorStop(0, "rgba(255,255,255,0)");
        fade.addColorStop(0.25, "rgba(255,255,255,1)");
        fade.addColorStop(0.7, "rgba(255,255,255,0.6)");
        fade.addColorStop(1, "rgba(255,255,255,0)");
        bctx.fillStyle = fade;
        bctx.fillRect(0, 0, 64, 256);
        ctx.drawImage(beamCanvas, 280, 176);
        frames.beam = new PIXI.Rectangle(280, 176, 64, 256);
        const base = new PIXI.BaseTexture(canvas, { scaleMode: PIXI.SCALE_MODES.LINEAR });
        this.atlas = { base, textures: {} };
        for (const name of Object.keys(frames)) this.atlas.textures[name] = new PIXI.Texture(base, frames[name]);
    },

    atlasTexture(name, blurLevel) {
        const t = this.atlas.textures;
        return t[name + (blurLevel | 0)] || t[name] || t.dot0;
    }
});

//=============================================================================
// 14. Batch renderer plugins (registered before the renderer is created)
//=============================================================================

const BATCH_OBJECT = "hd2dObject";
const BATCH_SILHOUETTE = "hd2dSilhouette";
const BATCH_NORMAL = "hd2dNormal";
try {
    PIXI.Renderer.registerPlugin(BATCH_OBJECT, PIXI.BatchPluginFactory.create({ fragment: GLSL.BATCH_OBJECT_FRAG }));
    PIXI.Renderer.registerPlugin(BATCH_SILHOUETTE, PIXI.BatchPluginFactory.create({ fragment: GLSL.BATCH_SILHOUETTE_FRAG }));
    PIXI.Renderer.registerPlugin(BATCH_NORMAL, PIXI.BatchPluginFactory.create({ fragment: GLSL.BATCH_NORMAL_FRAG }));
} catch (e) {
    GPU.failed = true;
    console.error("[HD2D] Could not register batch plugins.", e);
}

/**
 * Lightweight stand-in for a sprite that the batch renderer can draw. It
 * reuses a sprite's geometry/texture but carries its own color and alpha,
 * so the real sprites are never modified.
 */
class BatchProxy {
    constructor() {
        this._texture = null;
        this._own = new Float32Array(8); // used when the proxy has its own geometry
        this.vertexData = this._own;
        this.uvs = null;
        this.indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
        this._tintRGB = 0xffffff;
        this.worldAlpha = 1;
        this.blendMode = PIXI.BLEND_MODES.NORMAL;
    }
}

const ProxyPool = {
    list: [],
    used: 0,
    reset() {
        this.used = 0;
    },
    get() {
        if (this.used >= this.list.length) this.list.push(new BatchProxy());
        return this.list[this.used++];
    }
};

/** Packs depth/emissive/kind/rim into a tint value for the object batch. */
const objectTint = (depth, emissive, kind, low) => {
    const r = Math.round(U.saturate(depth / 100) * 255);
    const g = Math.round(U.saturate(emissive / 4) * 255);
    const b = ((kind & 3) << 6) | (low & 63);
    return r | (g << 8) | (b << 16);
};

//=============================================================================
// 15. Per-map data texture (region depth, emissive regions, light blockers)
//=============================================================================

const RegionMap = (HD2D.RegionMap = {
    texture: null,
    data: null,
    width: 0,
    height: 0,
    key: "",
    casterKey: "",

    ensure() {
        if (!$gameMap || !$dataMap) return null;
        const w = $gameMap.width();
        const h = $gameMap.height();
        const key = $gameMap.mapId() + "|" + w + "x" + h + "|" + MapTags.version + "|" + $gameMap.tilesetId();
        if (key !== this.key) {
            this.key = key;
            this.build(w, h);
        }
        this.updateCasters();
        return this.texture;
    },

    build(w, h) {
        this.width = w;
        this.height = h;
        this.data = new Uint8Array(w * h * 4);
        this.base = new Uint8Array(w * h * 4);
        for (let y = 0; y < h; y++) {
            for (let x = 0; x < w; x++) {
                const i = (y * w + x) * 4;
                const region = $gameMap.regionId(x, y);
                const depth = region > 0 ? MapTags.regionDepthOf(region) : null;
                if (depth !== null) {
                    this.base[i] = Math.round((depth / 100) * 255);
                    this.base[i + 3] = 255;
                }
                const em = region > 0 ? MapTags.regionEmissiveOf(region) : 0;
                if (em > 0) this.base[i + 1] = Math.round(U.saturate(em / 4) * 255);
                let block = MapTags.isBlockingRegion(region) || MapTags.isBlockingTerrain($gameMap.terrainTag(x, y));
                if (!block && P.wallsBlockLight) {
                    // A3/A4 wall and roof autotiles on the bottom layer block light.
                    const id = $gameMap.tileId(x, y, 0);
                    block = Tilemap.isWallTile(id) || Tilemap.isRoofTile(id);
                }
                if (block) this.base[i + 2] = 255;
            }
        }
        this.data.set(this.base);
        if (this.texture) this.texture.destroy(true);
        this.texture = GPU.dataTexture(this.data, w, h);
        this.casterKey = "";
    },

    /** Events tagged <HD2DShadowCaster> block light on their current tile. */
    updateCasters() {
        if (!this.data) return;
        let key = "";
        const casters = [];
        for (const ev of $gameMap.events()) {
            if (ev._erased || ev._pageIndex < 0) continue;
            if (!ev.hd2dTags().shadowCaster) continue;
            const x = Math.round(ev._realX);
            const y = Math.round(ev._realY);
            casters.push([x, y]);
            key += x + "," + y + ";";
        }
        if (key === this.casterKey) return;
        this.casterKey = key;
        this.data.set(this.base);
        for (const [x, y] of casters) {
            if (x < 0 || y < 0 || x >= this.width || y >= this.height) continue;
            this.data[(y * this.width + x) * 4 + 2] = 255;
        }
        this.texture.baseTexture.resource.data = this.data;
        this.texture.baseTexture.update();
    }
});

//=============================================================================
// 16. Normal maps (optional)
//-----------------------------------------------------------------------------
// Loaded with Bitmap.load (not ImageManager) so that a missing file never
// stops the game; encrypted deployments are still supported.
//=============================================================================

const NormalMaps = (HD2D.NormalMaps = {
    cache: {},

    /**
     * Returns a loaded BaseTexture for a character sheet's normal map, or null.
     * explicit: file name from <HD2DNormalMap: file>; otherwise "<name><suffix>"
     * is tried when Auto-Detect Normal Maps is enabled.
     */
    get(name, explicit) {
        if (!name && !explicit) return null;
        if (!explicit && !P.autoNormalMaps) return null;
        const file = explicit || name + P.normalSuffix;
        let entry = this.cache[file];
        if (!entry) {
            const url = "img/characters/" + Utils.encodeURI(file) + ".png";
            const bitmap = Bitmap.load(url);
            entry = this.cache[file] = { bitmap, state: "loading" };
            bitmap.addLoadListener(() => {
                entry.state = "ok";
            });
        }
        if (entry.state === "loading" && entry.bitmap.isError()) entry.state = "missing";
        return entry.state === "ok" ? entry.bitmap.baseTexture : null;
    }
});


//=============================================================================
// 17. Render pipeline
//-----------------------------------------------------------------------------
// The whole world (map) container gets ONE filter. Inside its apply() all
// passes run in order using our own render textures; the result is written
// to the filter output. PIXI's filter system takes care of render target
// nesting, so the pipeline also works inside Bitmap.snap() (menu background,
// battle transition) and together with other filters.
//=============================================================================

const F32 = n => new Float32Array(n);

class PostFilter extends PIXI.Filter {
    constructor(pipeline, fragment) {
        super(GLSL.FILTER_VERT, fragment, PostFilter.makeUniforms());
        this.pipeline = pipeline;
        this.autoFit = true;
        this.padding = 0;
        this.resolution = 1;
    }

    static makeUniforms() {
        return {
            uDepthTex: PIXI.Texture.WHITE, uLightTex: PIXI.Texture.WHITE, uOverlay: PIXI.Texture.WHITE,
            uNoise: PIXI.Texture.WHITE, uDofTex: PIXI.Texture.WHITE, uBloomTex: PIXI.Texture.WHITE, uLut: PIXI.Texture.WHITE,
            uLightOn: F32(4), uTintS: F32(4), uTintH: F32(4), uAtmoA: F32(4), uAtmoB: F32(4), uAtmoC: F32(4),
            uFocal: F32(4), uFogColor: F32(4), uFogCfg: F32(4), uFog0: F32(4), uFog1: F32(4), uFog2: F32(4),
            uFogOffA: F32(4), uFogOffB: F32(4), uFinalCfg: F32(4), uRim: F32(4), uRim2: F32(4),
            uGradeA: F32(4), uGradeB: F32(4), uGradeS: F32(4), uGradeH: F32(4), uGradeC: F32(4),
            uVig: F32(4), uVigColor: F32(4), uDebug: F32(4)
        };
    }

    apply(filterManager, input, output, clearMode, currentState) {
        const pipe = this.pipeline;
        if (pipe && !pipe.failed) {
            try {
                pipe.render(filterManager, input, output, clearMode, currentState || filterManager.activeState, this);
                return;
            } catch (e) {
                pipe.fail(e);
            }
        }
        filterManager.applyFilter(Pipeline.passThrough(), input, output, clearMode);
    }
}

class Pipeline {
    constructor(spriteset, kind) {
        this.spriteset = spriteset;
        this.kind = kind; // "map" | "battle"
        this.failed = false;
        this.filter = new PostFilter(this, GPU.maxTextureUnits < 8 ? "#define NO_LUT\n" + GLSL.FINAL_FRAG : GLSL.FINAL_FRAG);
        this.flags = {};
        this.passes = 0;
        this.lightCap = 0;
        this.bokehGridKey = "";
        this.time = 0;
        this.depthU = {
            uDepthCurve: F32(4), uDepthCam: F32(4), uViewSize: F32(2), uScreenToLocal: F32(9),
            uMapInfo: F32(4), uMapSize: F32(4), uRegion: GPU.textures.black
        };
        this.tmpMatrix = new PIXI.Matrix();
        this.frameRect = new PIXI.Rectangle();
        this.rtDepth = null;
        this.rtLight = null;
        this.rtShadow = null;
        this.rtNormal = null;
        this.rtOverlay = null;
        this.rtPrep = null;
        this.rtDof = null;
        this.rtBloom = null;
    }

    static passThrough() {
        if (!Pipeline._pass) Pipeline._pass = new PIXI.Filter();
        return Pipeline._pass;
    }

    fail(e) {
        this.failed = true;
        console.error("[HD2D] Rendering error - HD2D post-processing disabled for this scene.", e);
        HD2D.lastError = e;
    }

    //-------------------------------------------------------------------------
    // Flags: which passes run this frame
    //-------------------------------------------------------------------------

    computeFlags() {
        const st = HD2D.state();
        const q = State.quality();
        const T = k => State.effectOn(k);
        const w = k => (st[k] ? st[k].weight : 0);
        const f = this.flags;
        const map = this.kind === "map";
        const tausi = map && Pipeline.tausiOwnsLighting();
        f.depth = map && T("depth") && w("depth") > 0;
        f.obj = f.depth;
        f.dof = f.depth && T("dof") && w("dof") > 0.001 && st.dof.strength * st.dof.radius > 0.05;
        f.bokeh = f.dof && T("bokeh") && w("bokeh") > 0.001 && st.bokeh.intensity > 0;
        f.ambient = map && T("ambient") && w("ambient") > 0 && !tausi;
        f.sun = map && T("lighting") && w("sun") > 0 && st.sun.intensity > 0 && !tausi;
        f.lights = map && T("lighting") && w("lights") > 0 && Lights.list.length > 0 && !tausi;
        f.shadows = map && T("shadows") && w("shadows") > 0 && q.shadowMode > 0;
        f.normals = map && T("normalMaps") && q.normalMaps && (f.sun || f.lights) && !!this.spriteset._hd2dHasNormals;
        f.light = f.ambient || f.sun || f.lights || f.shadows;
        f.fog = map && T("fog") && w("fog") > 0;
        f.atmo = f.depth && T("atmosphere") && w("atmosphere") > 0;
        f.rim = f.depth && T("rim") && w("rim") > 0 && st.rim.intensity > 0;
        f.emissive = T("emissive");
        f.overlay = map && this.spriteset._hd2dUnlit && this.spriteset._hd2dUnlit.children.some(c => c.visible);
        f.bloom = T("bloom") && w("bloom") > 0 && st.bloom.intensity > 0;
        f.prep = f.dof || f.bloom;
        f.grade = T("grade") && w("grade") > 0;
        f.vignette = T("vignette") && w("vignette") > 0 && st.vignette.intensity > 0;
        f.debug = Debug.view;
        f.any = f.obj || f.light || f.fog || f.prep || f.grade || f.vignette || f.overlay || f.debug > 0;
        return f;
    }

    /** TausiLighting compatibility: let Tausi own the lighting on its maps. */
    static tausiOwnsLighting() {
        if (P.tausiMode === "both" || typeof window.LightingUtils === "undefined" || typeof $dataLighting === "undefined" || !$dataLighting) return false;
        if (P.tausiMode === "hd2d off") return true;
        try {
            const map = $dataLighting.getCurrentMap();
            return !!map && map.getMapObjectsOfType(window.Data_Lighting_Light).some(o => o.enabled !== false);
        } catch (e) {
            return false;
        }
    }

    //-------------------------------------------------------------------------
    // Main entry (called from PostFilter.apply)
    //-------------------------------------------------------------------------

    render(fm, input, output, clearMode, state, filter) {
        const renderer = fm.renderer;
        if (!GPU.init(renderer)) throw new Error("GPU init failed");
        const frame = this.frameRect.copyFrom(state.sourceFrame);
        const W = frame.width;
        const H = frame.height;
        const st = HD2D.state();
        const q = State.quality();
        const f = this.computeFlags();
        this.passes = 0;
        this.time++;
        renderer.batch.flush();
        if (this.kind === "map") this.updateDepthUniforms(frame, st);

        if (f.obj) this.renderObjects(renderer, frame, q);
        if (f.depth) this.renderResolve(renderer, frame, q, st);
        if (f.normals) this.renderNormals(renderer, frame, q);
        if (f.shadows) this.renderShadows(renderer, frame, q, st);
        if (f.light) this.renderLight(renderer, frame, q, st, f);
        if (f.overlay) this.renderOverlay(renderer, frame);
        this.setShadeUniforms(st, q, f, W, H);
        if (f.prep) this.renderPrep(renderer, frame, input, q, st, f);
        if (f.dof) this.renderDof(renderer, frame, q, st, f);
        if (f.bloom) this.renderBloom(renderer, frame, q, st, f);
        this.setFinalUniforms(filter, st, f, W, H);
        renderer.batch.flush();
        fm.applyFilter(filter, input, output, clearMode);
        this.passes++;
    }

    //-------------------------------------------------------------------------
    // Camera / depth uniforms
    //-------------------------------------------------------------------------

    updateDepthUniforms(frame, st) {
        const u = this.depthU;
        const tilemap = this.spriteset._tilemap;
        const d = st.depth;
        u.uDepthCurve[0] = d.focalDepth;
        u.uDepthCurve[1] = d.nearDepth;
        u.uDepthCurve[2] = d.farDepth;
        u.uDepthCurve[3] = d.curve;
        u.uDepthCam[0] = Depth.focalY;
        u.uDepthCam[1] = d.strength;
        u.uDepthCam[2] = d.autoY ? 1 : 0;
        u.uDepthCam[3] = Camera.zoom();
        u.uViewSize[0] = Graphics.width;
        u.uViewSize[1] = Graphics.height;
        if (tilemap && tilemap.worldTransform) {
            const inv = this.tmpMatrix.copyFrom(tilemap.worldTransform).invert();
            U.mat3FromPixi(u.uScreenToLocal, inv);
            u.uMapInfo[0] = Math.ceil(tilemap.origin.x);
            u.uMapInfo[1] = Math.ceil(tilemap.origin.y);
            u.uMapInfo[2] = tilemap.tileWidth;
            u.uMapInfo[3] = tilemap.tileHeight;
        }
        if ($gameMap && $dataMap) {
            u.uMapSize[0] = $gameMap.width();
            u.uMapSize[1] = $gameMap.height();
            u.uMapSize[2] = $gameMap.isLoopHorizontal() ? 1 : 0;
            u.uMapSize[3] = $gameMap.isLoopVertical() ? 1 : 0;
            u.uRegion = RegionMap.ensure() || GPU.textures.black;
        }
    }

    applyDepthUniforms(shader) {
        Object.assign(shader.uniforms, this.depthU);
    }

    //-------------------------------------------------------------------------
    // 1. Object buffer
    //-------------------------------------------------------------------------

    renderObjects(renderer, frame, q) {
        const ss = this.spriteset;
        const rt = (this.rtObj = GPU.rt("obj", frame.width, frame.height, q.objScale, { nearest: true }));
        GPU.bindTarget(renderer, rt, frame, [0, 0, 0, 0]);
        ProxyPool.reset();
        const plugin = renderer.plugins[BATCH_OBJECT];
        const tilemap = ss._tilemap;
        const background = !!ss._hd2dBackgroundMode;
        // Background layers (behind the map): farthest first.
        if (background) {
            if (ss._parallax && ss._hd2dParallaxDepth !== null && ss._parallax.visible) {
                this.stampSprite(renderer, ss._parallax, frame, ss._hd2dParallaxDepth, true, true);
            }
            for (const child of ss._hd2dBack.children) this.drawWorldObject(renderer, plugin, child, frame);
        }
        if (tilemap && tilemap.children) {
            for (const child of tilemap.children) {
                if (!child.visible) continue;
                if (child === tilemap._lowerLayer) {
                    if (background) this.drawTileCoverage(renderer, child, 0);
                } else if (child === tilemap._upperLayer) {
                    this.drawTileCoverage(renderer, child, 1);
                } else if (child._hd2d) {
                    this.drawCharacter(renderer, plugin, child);
                } else if (child._hd2dDepth !== undefined) {
                    this.drawWorldObject(renderer, plugin, child, frame);
                }
            }
        }
        for (const child of ss._hd2dFront.children) {
            if (child._hd2d) this.drawCharacter(renderer, plugin, child);
            else this.drawWorldObject(renderer, plugin, child, frame);
        }
        renderer.batch.flush();
        this.passes++;
    }

    pushProxy(renderer, plugin, sprite, tint, blendMode) {
        const tex = sprite._texture;
        if (!tex || !tex.valid || !tex.baseTexture) return null;
        sprite.calculateVertices();
        const v = sprite.vertexData;
        if (Math.abs((v[2] - v[0]) * (v[7] - v[1]) - (v[3] - v[1]) * (v[6] - v[0])) < 0.5) return null;
        const p = ProxyPool.get();
        p._texture = tex;
        p.vertexData = v;
        p.uvs = sprite.uvs || tex._uvs.uvsFloat32;
        p.indices = sprite.indices || p.indices;
        p._tintRGB = tint;
        p.worldAlpha = 1;
        p.blendMode = blendMode || PIXI.BLEND_MODES.NORMAL;
        renderer.batch.setObjectRenderer(plugin);
        plugin.render(p);
        return p;
    }

    drawCharacter(renderer, plugin, sprite) {
        // Mostly transparent sprites (ghosts, fading events) do not own their pixels.
        if (!sprite.visible || sprite.worldAlpha < 0.25) return;
        const h = sprite._hd2d;
        const tint = objectTint(h.depth, h.emissive, 2, Math.round(U.saturate(h.rim) * 63));
        this.pushProxy(renderer, plugin, sprite, tint);
        if (sprite._upperBody && sprite._upperBody.visible) this.pushProxy(renderer, plugin, sprite._upperBody, tint);
        if (sprite._lowerBody && sprite._lowerBody.visible) this.pushProxy(renderer, plugin, sprite._lowerBody, tint);
    }

    /** Pictures / layer sprites / plugin sprites with an explicit depth. */
    drawWorldObject(renderer, plugin, obj, frame) {
        // Translucent layers / pictures (mist, light overlays) keep the depth of
        // what is behind them, otherwise they would blur the whole scene.
        if (!obj || !obj.visible || obj.worldAlpha < 0.4) return;
        const depth = obj._hd2dDepth;
        if (depth === undefined || depth === null) {
            if (obj.children && obj.children.length && !obj._hd2dLayer) {
                for (const c of obj.children) this.drawWorldObject(renderer, plugin, c, frame);
            }
            return;
        }
        const emissive = obj._hd2dEmissive || 0;
        if (obj instanceof PIXI.TilingSprite) {
            this.stampSprite(renderer, obj, frame, depth, true, false, emissive);
        } else if (obj instanceof PIXI.Sprite) {
            this.pushProxy(renderer, plugin, obj, objectTint(depth, emissive, 1, 0));
        }
    }

    /** Writes the coverage of a tilemap layer (kind 3) into the object buffer. */
    drawTileCoverage(renderer, layer, upper) {
        const tr = renderer.plugins.rpgtilemap;
        if (!tr || !tr._shader) return;
        if (!this._tileShader) {
            this._tileShader = PIXI.Shader.from(GLSL.TILE_VERT, GLSL.TILE_FRAG, {
                uSampler0: 0, uSampler1: 0, uSampler2: 0, uProjectionMatrix: new PIXI.Matrix(), uOutColor: F32(4)
            });
        }
        const sh = this._tileShader;
        sh.uniforms.uOutColor[0] = 0;
        sh.uniforms.uOutColor[1] = 0;
        sh.uniforms.uOutColor[2] = ((3 << 6) | (upper ? 1 : 0)) / 255;
        sh.uniforms.uOutColor[3] = 1;
        const original = tr._shader;
        tr._shader = sh;
        try {
            layer.render(renderer);
            renderer.batch.flush();
        } finally {
            tr._shader = original;
        }
    }

    /** Stamps a (tiling) sprite's opaque pixels into the object buffer with a fixed depth. */
    stampSprite(renderer, sprite, frame, depth, isTiling, fillAll, emissive = 0) {
        const tex = sprite._texture || sprite.texture;
        if (!tex || !tex.valid || !tex.baseTexture) return;
        if (!this._stampShader) {
            this._stampShader = GPU.shader("stamp", GLSL.QUAD_VERT, GLSL.STAMP_FRAG, {
                uLayerTex: PIXI.Texture.WHITE, uScreenToTex: F32(9), uStampCfg: F32(4), uFrameUV: F32(4), uOutColor: F32(4)
            });
        }
        const sh = this._stampShader;
        const u = sh.uniforms;
        const inv = this.tmpMatrix.copyFrom(sprite.worldTransform).invert();
        const fw = tex.frame.width || 1;
        const fh = tex.frame.height || 1;
        let ox = 0;
        let oy = 0;
        if (isTiling && sprite.tilePosition) {
            const sx = sprite.tileScale ? sprite.tileScale.x : 1;
            const sy = sprite.tileScale ? sprite.tileScale.y : 1;
            ox = -sprite.tilePosition.x;
            oy = -sprite.tilePosition.y;
            inv.translate(ox, oy);
            inv.scale(1 / (fw * sx), 1 / (fh * sy));
        } else {
            const ax = sprite.anchor ? sprite.anchor.x * fw : 0;
            const ay = sprite.anchor ? sprite.anchor.y * fh : 0;
            inv.translate(ax, ay);
            inv.scale(1 / fw, 1 / fh);
        }
        U.mat3FromPixi(u.uScreenToTex, inv);
        u.uStampCfg[0] = isTiling ? 1 : 0;
        u.uStampCfg[1] = isTiling ? 1 : 0;
        u.uStampCfg[2] = fillAll ? 1 : 0;
        const bt = tex.baseTexture;
        u.uFrameUV[0] = tex.frame.x / bt.width;
        u.uFrameUV[1] = tex.frame.y / bt.height;
        u.uFrameUV[2] = fw / bt.width;
        u.uFrameUV[3] = fh / bt.height;
        u.uLayerTex = tex;
        const r = Math.round(U.saturate(depth / 100) * 255);
        const g = Math.round(U.saturate(emissive / 4) * 255);
        u.uOutColor[0] = r / 255;
        u.uOutColor[1] = g / 255;
        u.uOutColor[2] = (1 << 6) / 255;
        u.uOutColor[3] = 1;
        GPU.drawQuad(renderer, sh, this.rtObj, frame, { blend: "normal" });
    }

    //-------------------------------------------------------------------------
    // 2. Depth resolve
    //-------------------------------------------------------------------------

    renderResolve(renderer, frame, q, st) {
        const rt = (this.rtDepth = GPU.rt("depth", frame.width, frame.height, q.objScale));
        if (!this._resolveShader) {
            this._resolveShader = GPU.shader("resolve", GLSL.QUAD_VERT, GLSL.RESOLVE_FRAG, Object.assign({ uObj: PIXI.Texture.WHITE, uResolve: F32(4) }, this.depthU));
        }
        const sh = this._resolveShader;
        this.applyDepthUniforms(sh);
        sh.uniforms.uObj = this.rtObj;
        sh.uniforms.uResolve[0] = st.depth.upperTileOffset;
        sh.uniforms.uResolve[1] = st.depth.backgroundDepth;
        sh.uniforms.uResolve[2] = this.spriteset._hd2dBackgroundMode ? 1 : 0;
        GPU.drawQuad(renderer, sh, rt, frame);
        this.passes++;
    }

    //-------------------------------------------------------------------------
    // 3. Normal maps (optional)
    //-------------------------------------------------------------------------

    renderNormals(renderer, frame, q) {
        const rt = (this.rtNormal = GPU.rt("normal", frame.width, frame.height, q.objScale, { nearest: true }));
        GPU.bindTarget(renderer, rt, frame, [0, 0, 0, 0]);
        const plugin = renderer.plugins[BATCH_NORMAL];
        for (const sprite of this.spriteset._characterSprites || []) {
            const h = sprite._hd2d;
            if (!h || !h.normalTexture || !sprite.visible || sprite.worldAlpha <= 0) continue;
            const ntex = h.normalTexture;
            const tex = sprite._texture;
            if (!tex || !tex.valid) continue;
            sprite.calculateVertices();
            const p = ProxyPool.get();
            p._texture = ntex;
            p.vertexData = sprite.vertexData;
            p.uvs = ntex._uvs.uvsFloat32;
            p.indices = sprite.indices || p.indices;
            p._tintRGB = 0xffffff;
            p.worldAlpha = 1;
            p.blendMode = PIXI.BLEND_MODES.NORMAL;
            renderer.batch.setObjectRenderer(plugin);
            plugin.render(p);
        }
        renderer.batch.flush();
        this.passes++;
    }

    //-------------------------------------------------------------------------
    // 4. Character shadows (sun + light silhouettes, contact blobs)
    //-------------------------------------------------------------------------

    renderShadows(renderer, frame, q, st) {
        const rt = (this.rtShadow = GPU.rt("shadow", frame.width, frame.height, q.shadowScale));
        GPU.bindTarget(renderer, rt, frame, [0, 0, 0, 0]);
        const plugin = renderer.plugins[BATCH_SILHOUETTE];
        const cam = this.spriteset._hd2dCamera;
        const wt = cam ? cam.worldTransform : PIXI.Matrix.IDENTITY;
        const rot = Math.atan2(wt.b, wt.a);
        const camScale = Math.hypot(wt.a, wt.b) || 1;
        const sh = st.shadows;
        const sunOn = this.flags.sun && q.shadowMode >= 2;
        const sunStrength = U.saturate((st.sun.intensity * st.sun.weight) / 0.25);
        const sunA = ((st.sun.angle * Math.PI) / 180) + rot;
        const elev = (U.clamp(st.sun.elevation, 5, 89) * Math.PI) / 180;
        const sunLen = U.clamp((1 / Math.tan(elev)) * sh.length, 0.12, 1.8);
        const sunVec = [-Math.cos(sunA) * sunLen, -Math.sin(sunA) * sunLen];
        const maxLightShadows = q.shadowMode >= 4 ? 2 : q.shadowMode >= 2 ? 1 : 0;
        const useLights = this.flags.lights && sh.lightShadows && maxLightShadows > 0;
        const lightsScreen = useLights ? this.screenLights(wt, camScale) : [];
        const blob = GPU.atlasTexture("blob");
        for (const sprite of this.spriteset._characterSprites || []) {
            const h = sprite._hd2d;
            if (!h || !h.shadow || !sprite.visible || sprite.worldAlpha <= 0.05) continue;
            sprite.calculateVertices();
            const v = sprite.vertexData;
            // Foot line = bottom edge (anchor y = 1). Width in screen pixels:
            const footX = (v[4] + v[6]) / 2;
            const footY = (v[5] + v[7]) / 2;
            const width = Math.hypot(v[4] - v[6], v[5] - v[7]);
            const height = Math.hypot(v[0] - v[6], v[1] - v[7]);
            if (width < 1 || height < 1) continue;
            // Contact shadow blob (channel B).
            if (sh.contact > 0) {
                const p = ProxyPool.get();
                const bw = Math.min(width, 48 * camScale) * 0.42;
                const bh = bw * 0.36;
                const out = p._own;
                out[0] = footX - bw; out[1] = footY - bh - camScale;
                out[2] = footX + bw; out[3] = footY - bh - camScale;
                out[4] = footX + bw; out[5] = footY + bh - camScale;
                out[6] = footX - bw; out[7] = footY + bh - camScale;
                p.vertexData = out;
                p._texture = blob;
                p.uvs = blob._uvs.uvsFloat32;
                p._tintRGB = 0xff0000;
                p.worldAlpha = U.saturate(h.alpha);
                p.blendMode = PIXI.BLEND_MODES.ADD;
                renderer.batch.setObjectRenderer(plugin);
                plugin.render(p);
            }
            if (q.shadowMode < 2 || sprite._bushDepth > 0) continue;
            const tex = sprite._texture;
            if (!tex || !tex.valid) continue;
            if (sunOn && sunStrength > 0.01) {
                this.pushSilhouette(renderer, plugin, sprite, sunVec, 0x0000ff, sh.opacity * sunStrength * h.alpha);
            }
            if (useLights && lightsScreen.length) {
                const found = [];
                for (const L of lightsScreen) {
                    const dx = footX - L.x;
                    const dy = footY - (L.y + L.r * 0.0);
                    const d = Math.hypot(dx, dy);
                    if (d >= L.r * 0.95 || d < 1) continue;
                    const t = d / L.r;
                    const att = L.intensity * Math.pow(1 - t, 1.6);
                    if (att > 0.06) found.push({ dx: dx / d, dy: dy / d, t, att });
                }
                found.sort((a, b) => b.att - a.att);
                for (let i = 0; i < Math.min(found.length, maxLightShadows); i++) {
                    const s = found[i];
                    const len = U.clamp(0.35 + s.t * 1.2, 0.3, 1.5) * sh.length;
                    this.pushSilhouette(renderer, plugin, sprite, [s.dx * len, s.dy * len], 0x00ff00, sh.opacity * U.saturate(s.att * 1.4) * h.alpha);
                }
            }
        }
        renderer.batch.flush();
        this.passes++;
        // Blur the shadow mask.
        const tmp = GPU.rt("shadowTmp", frame.width, frame.height, q.shadowScale);
        const blur = this.blurShader();
        const soft = Math.max(0.25, sh.softness) * (q.shadowScale < 0.5 ? 0.7 : 1);
        blur.uniforms.uTex = rt;
        blur.uniforms.uDir[0] = soft / rt.baseTexture.realWidth;
        blur.uniforms.uDir[1] = 0;
        GPU.drawQuad(renderer, blur, tmp, frame);
        blur.uniforms.uTex = tmp;
        blur.uniforms.uDir[0] = 0;
        blur.uniforms.uDir[1] = soft / rt.baseTexture.realHeight;
        GPU.drawQuad(renderer, blur, rt, frame);
        this.passes += 2;
    }

    /** Projected silhouette: bottom edge stays, the top edge is moved by vec * height. */
    pushSilhouette(renderer, plugin, sprite, vec, tintRGB, alpha) {
        if (alpha <= 0.005) return;
        const v = sprite.vertexData;
        const height = Math.hypot(v[0] - v[6], v[1] - v[7]);
        const p = ProxyPool.get();
        const out = p._own;
        const ox = vec[0] * height;
        const oy = vec[1] * height;
        // TL, TR become the projected head; BR, BL stay at the feet.
        out[0] = v[6] + ox;
        out[1] = v[7] + oy;
        out[2] = v[4] + ox;
        out[3] = v[5] + oy;
        out[4] = v[4];
        out[5] = v[5];
        out[6] = v[6];
        out[7] = v[7];
        p.vertexData = out;
        p._texture = sprite._texture;
        p.uvs = sprite.uvs || sprite._texture._uvs.uvsFloat32;
        p._tintRGB = tintRGB;
        p.worldAlpha = U.saturate(alpha);
        p.blendMode = PIXI.BLEND_MODES.ADD;
        renderer.batch.setObjectRenderer(plugin);
        plugin.render(p);
    }

    blurShader() {
        if (!this._blurShader) this._blurShader = GPU.shader("blur", GLSL.QUAD_VERT, GLSL.BLUR_FRAG, { uTex: PIXI.Texture.WHITE, uDir: F32(2) });
        return this._blurShader;
    }

    /** Lights in screen space for this frame. */
    screenLights(wt, camScale) {
        const out = [];
        for (const L of Lights.list) {
            out.push({
                x: wt.a * L.x + wt.c * L.y + wt.tx,
                y: wt.b * L.x + wt.d * L.y + wt.ty,
                r: L.radius * camScale,
                intensity: L.intensity,
                src: L
            });
        }
        return out;
    }

    //-------------------------------------------------------------------------
    // 5. Light buffer
    //-------------------------------------------------------------------------

    lightRange() {
        return GPU.hdr ? 1 : 2;
    }

    renderLight(renderer, frame, q, st, f) {
        const rt = (this.rtLight = GPU.rt("light", frame.width, frame.height, q.lightScale, { hdr: true }));
        if (!this._lightBaseShader) {
            this._lightBaseShader = GPU.shader("lightBase", GLSL.QUAD_VERT, GLSL.LIGHT_BASE_FRAG, {
                uShadow: PIXI.Texture.WHITE, uNormal: PIXI.Texture.WHITE, uAmbient: F32(3), uSun: F32(3), uSunDir: F32(3),
                uShadowCfg: F32(4), uLightScale: 1
            });
        }
        const sh = this._lightBaseShader;
        const u = sh.uniforms;
        const aw = f.ambient ? st.ambient.weight : 0;
        const ac = U.temperature(st.ambient.color, st.ambient.temperature);
        for (let i = 0; i < 3; i++) u.uAmbient[i] = U.lerp(1, ac[i] * st.ambient.intensity, aw);
        const sw = f.sun ? st.sun.weight * st.sun.intensity : 0;
        for (let i = 0; i < 3; i++) u.uSun[i] = st.sun.color[i] * sw;
        const cam = this.spriteset._hd2dCamera;
        const rot = cam ? Math.atan2(cam.worldTransform.b, cam.worldTransform.a) : 0;
        const a = ((st.sun.angle * Math.PI) / 180) + rot;
        const elev = (U.clamp(st.sun.elevation, 0, 90) * Math.PI) / 180;
        u.uSunDir[0] = Math.cos(a) * Math.cos(elev);
        u.uSunDir[1] = Math.sin(a) * Math.cos(elev);
        u.uSunDir[2] = Math.sin(elev);
        const shadowsOn = f.shadows && this.rtShadow;
        u.uShadow = shadowsOn ? this.rtShadow : GPU.textures.black;
        u.uNormal = f.normals && this.rtNormal ? this.rtNormal : GPU.textures.black;
        u.uShadowCfg[0] = shadowsOn ? st.shadows.weight : 0;
        u.uShadowCfg[2] = shadowsOn ? st.shadows.contact * st.shadows.weight : 0;
        u.uShadowCfg[3] = f.normals ? 1 : 0;
        u.uLightScale = 1 / this.lightRange();
        GPU.drawQuad(renderer, sh, rt, frame);
        this.passes++;
        if (f.lights && Lights.list.length) this.renderLightQuads(renderer, frame, q, st, f);
    }

    ensureLightGeometry(cap) {
        if (this.lightCap >= cap && this.lightGeom) return;
        this.lightCap = Math.max(cap, 8);
        this.lightData = new Float32Array(this.lightCap * 4 * 20);
        const idx = new Uint16Array(this.lightCap * 6);
        for (let i = 0; i < this.lightCap; i++) {
            idx.set([i * 4, i * 4 + 1, i * 4 + 2, i * 4, i * 4 + 2, i * 4 + 3], i * 6);
        }
        this.lightBuffer = new PIXI.Buffer(this.lightData, false, false);
        const stride = 20 * 4;
        this.lightGeom = new PIXI.Geometry()
            .addAttribute("aPos", this.lightBuffer, 2, false, PIXI.TYPES.FLOAT, stride, 0)
            .addAttribute("aCenter", this.lightBuffer, 2, false, PIXI.TYPES.FLOAT, stride, 8)
            .addAttribute("aParams", this.lightBuffer, 4, false, PIXI.TYPES.FLOAT, stride, 16)
            .addAttribute("aColor", this.lightBuffer, 4, false, PIXI.TYPES.FLOAT, stride, 32)
            .addAttribute("aSpot", this.lightBuffer, 4, false, PIXI.TYPES.FLOAT, stride, 48)
            .addAttribute("aExtra", this.lightBuffer, 4, false, PIXI.TYPES.FLOAT, stride, 64)
            .addIndex(new PIXI.Buffer(idx, true, true));
    }

    renderLightQuads(renderer, frame, q, st, f) {
        const list = Lights.list;
        this.ensureLightGeometry(list.length);
        const steps = q.occlusionSteps;
        const key = "light" + steps;
        if (!GPU.shaders[key]) {
            GPU.shaders[key] = PIXI.Shader.from(GLSL.LIGHT_VERT, GLSL.LIGHT_FRAG.replace("%STEPS%", String(Math.max(1, steps))), Object.assign({
                uShadow: PIXI.Texture.WHITE, uNormal: PIXI.Texture.WHITE, uDepth: PIXI.Texture.WHITE, uFrameRect: F32(4),
                uLightCfg: F32(4), uOcc: F32(2), uLightScale: 1
            }, this.depthU));
        }
        const sh = GPU.shaders[key];
        this.applyDepthUniforms(sh);
        const u = sh.uniforms;
        const cam = this.spriteset._hd2dCamera;
        const wt = cam.worldTransform;
        const camScale = Math.hypot(wt.a, wt.b) || 1;
        const rot = Math.atan2(wt.b, wt.a);
        const zoom = Camera.zoom();
        const viewH = Graphics.height;
        const occOn = steps > 0 && f.shadows && st.shadows.occlusion > 0 && !!RegionMap.data;
        const data = this.lightData;
        let n = 0;
        for (const L of list) {
            const cx = wt.a * L.x + wt.c * L.y + wt.tx;
            const cy = wt.b * L.x + wt.d * L.y + wt.ty;
            const r = L.radius * camScale;
            const spot = L.type === "spot";
            const dirA = ((L.direction * Math.PI) / 180) + rot;
            const half = (U.clamp(L.cone, 1, 359) * Math.PI) / 360;
            const cosOuter = Math.cos(half);
            const cosInner = Math.cos(half * (1 - U.clamp(L.coneSoftness, 0, 0.99)));
            let depth = -1;
            if (this.flags.depth) {
                const d = L.depth !== null && L.depth !== undefined ? L.depth : Depth.auto((L.y * zoom) / viewH, st.depth);
                depth = d / 100;
            }
            const corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
            for (let c = 0; c < 4; c++) {
                const o = (n * 4 + c) * 20;
                data[o] = cx + corners[c][0] * r;
                data[o + 1] = cy + corners[c][1] * r;
                data[o + 2] = cx;
                data[o + 3] = cy;
                data[o + 4] = r;
                data[o + 5] = L.intensity;
                data[o + 6] = Math.max(0.2, L.falloff);
                data[o + 7] = U.saturate(L.softness);
                data[o + 8] = L.color[0];
                data[o + 9] = L.color[1];
                data[o + 10] = L.color[2];
                data[o + 11] = spot ? 1 : 0;
                data[o + 12] = Math.cos(dirA);
                data[o + 13] = Math.sin(dirA);
                data[o + 14] = cosOuter;
                data[o + 15] = Math.max(cosInner, cosOuter + 0.0001);
                data[o + 16] = depth;
                data[o + 17] = U.clamp(L.depthRange, 1, 100) / 100;
                data[o + 18] = occOn && L.shadows ? 1 : 0;
                data[o + 19] = L.height;
            }
            n++;
        }
        if (!n) return;
        this.lightBuffer.update(data);
        u.uShadow = f.shadows && this.rtShadow ? this.rtShadow : GPU.textures.black;
        u.uNormal = f.normals && this.rtNormal ? this.rtNormal : GPU.textures.black;
        u.uDepth = this.rtDepth || GPU.textures.neutralDepth;
        u.uFrameRect[0] = frame.x;
        u.uFrameRect[1] = frame.y;
        u.uFrameRect[2] = frame.width;
        u.uFrameRect[3] = frame.height;
        u.uLightCfg[0] = f.normals ? 1 : 0;
        u.uLightCfg[1] = this.flags.depth && this.rtDepth ? 1 : 0;
        u.uLightCfg[2] = occOn ? 1 : 0;
        u.uLightCfg[3] = f.shadows ? st.shadows.weight : 0;
        u.uOcc[0] = U.saturate(st.shadows.occlusion * st.shadows.weight);
        u.uOcc[1] = camScale;
        u.uLightScale = 1 / this.lightRange();
        GPU.bindTarget(renderer, this.rtLight, frame);
        renderer.state.set(GPU.stateAdd);
        renderer.shader.bind(sh);
        renderer.geometry.bind(this.lightGeom, sh);
        renderer.geometry.draw(PIXI.DRAW_MODES.TRIANGLES, n * 6, 0);
        this.passes++;
    }

    //-------------------------------------------------------------------------
    // 6. Unlit overlay (emissive particles, glows, animations)
    //-------------------------------------------------------------------------

    renderOverlay(renderer, frame) {
        const rt = (this.rtOverlay = GPU.rt("overlay", frame.width, frame.height, 1));
        GPU.bindTarget(renderer, rt, frame, [0, 0, 0, 0]);
        const c = this.spriteset._hd2dUnlit;
        c.renderable = true;
        try {
            c.render(renderer);
            renderer.batch.flush();
        } finally {
            c.renderable = false;
        }
        this.passes++;
    }

    //-------------------------------------------------------------------------
    // Shared shading uniforms (DOF input pass + final pass)
    //-------------------------------------------------------------------------

    setShadeUniforms(st, q, f, W, H) {
        const s = this._shade || (this._shade = PostFilter.makeUniforms());
        s.uDepthTex = f.depth && this.rtDepth ? this.rtDepth : GPU.textures.neutralDepth;
        s.uLightTex = f.light && this.rtLight ? this.rtLight : GPU.textures.white;
        s.uOverlay = f.overlay && this.rtOverlay ? this.rtOverlay : GPU.textures.black;
        s.uNoise = GPU.textures.noise;
        s.uLightOn[0] = f.light ? 1 : 0;
        s.uLightOn[1] = this.lightRange();
        s.uLightOn[2] = f.emissive ? 1 : 0;
        s.uLightOn[3] = f.overlay ? 1 : 0;
        const tint = (c, amount, out) => {
            const l = Math.max(U.luma(c), 0.05);
            out[0] = c[0] / l;
            out[1] = c[1] / l;
            out[2] = c[2] / l;
            out[3] = amount;
        };
        const aw = f.ambient ? st.ambient.weight : 0;
        tint(st.ambient.shadowTint, st.ambient.shadowTintAmount * aw, s.uTintS);
        tint(st.ambient.highlightTint, st.ambient.highlightTintAmount * aw, s.uTintH);
        const at = st.atmosphere;
        s.uAtmoA[0] = at.hazeColor[0];
        s.uAtmoA[1] = at.hazeColor[1];
        s.uAtmoA[2] = at.hazeColor[2];
        s.uAtmoA[3] = at.hazeAmount;
        s.uAtmoB[0] = at.farDesaturate;
        s.uAtmoB[1] = at.farContrast;
        s.uAtmoB[2] = at.farBrighten;
        s.uAtmoB[3] = at.farTemperature;
        s.uAtmoC[0] = at.nearSaturate;
        s.uAtmoC[1] = at.nearContrast;
        s.uAtmoC[2] = at.nearDarken;
        s.uAtmoC[3] = f.atmo ? at.weight : 0;
        s.uFocal[0] = st.depth.focalDepth;
        const fog = st.fog;
        s.uFogColor[0] = fog.color[0];
        s.uFogColor[1] = fog.color[1];
        s.uFogColor[2] = fog.color[2];
        s.uFogColor[3] = f.light ? fog.lit : 0;
        s.uFogCfg[0] = fog.softness;
        s.uFogCfg[1] = fog.noise;
        s.uFogCfg[2] = fog.depthFog;
        s.uFogCfg[3] = f.fog ? fog.weight : 0;
        const layers = q.fogLayers;
        const zoom = Camera.zoom();
        const setLayer = (out, name, enabled) => {
            out[0] = U.saturate(fog[name + "Opacity"]);
            out[1] = f.depth ? fog[name + "Depth"] : 0;
            out[2] = fog[name + "Scale"];
            out[3] = enabled ? 1 : 0;
        };
        setLayer(s.uFog0, "near", layers >= 3);
        setLayer(s.uFog1, "mid", layers >= 2);
        setLayer(s.uFog2, "far", layers >= 1);
        const off = (name, i, out) => {
            const depth = fog[name + "Depth"];
            const factor = Depth.parallaxFactor(depth, st.parallax);
            out[i] = Camera.contX * factor * zoom + this.time * fog[name + "SpeedX"] * zoom;
            out[i + 1] = Camera.contY * factor * zoom + this.time * fog[name + "SpeedY"] * zoom;
        };
        off("near", 0, s.uFogOffA);
        off("mid", 2, s.uFogOffA);
        off("far", 0, s.uFogOffB);
        s.uFogOffB[2] = q.noiseOctaves;
    }

    applyShade(uniforms) {
        const s = this._shade;
        for (const key of Object.keys(s)) {
            if (key === "uDofTex" || key === "uBloomTex" || key === "uLut" || key === "uFinalCfg" || key.startsWith("uGrade") ||
                key.startsWith("uVig") || key === "uRim" || key === "uRim2" || key === "uDebug") continue;
            uniforms[key] = s[key];
        }
    }

    //-------------------------------------------------------------------------
    // 7. Depth of field (+ bokeh)
    //-------------------------------------------------------------------------

    storageScale() {
        return GPU.hdr ? 1 : 0.5;
    }

    dofParams(st) {
        const dof = st.dof;
        const focus = Depth.autoFocusDepth !== null ? Depth.autoFocusDepth : dof.focus;
        const zoomFactor = Math.pow(Camera.zoom(), P.zoomDofInfluence);
        const radius = U.clamp(dof.radius * dof.strength * zoomFactor, 0, 40);
        return { focus, radius };
    }

    renderPrep(renderer, frame, input, q, st, f) {
        const scale = q.dofScale;
        const rt = (this.rtPrep = GPU.rt("prep", frame.width, frame.height, scale, { hdr: true }));
        if (!this._prepShader) {
            this._prepShader = GPU.shader("prep", GLSL.QUAD_VERT, GLSL.DOF_PREP_FRAG, Object.assign(PostFilter.makeUniforms(), {
                uSampler: PIXI.Texture.WHITE, uInTexel: F32(2), uDof: F32(4), uDof2: F32(4)
            }));
        }
        const sh = this._prepShader;
        this.applyShade(sh.uniforms);
        const u = sh.uniforms;
        u.uSampler = input;
        u.uInTexel[0] = 1 / Math.max(1, input.baseTexture.realWidth);
        u.uInTexel[1] = 1 / Math.max(1, input.baseTexture.realHeight);
        const dp = this.dofParams(st);
        u.uDof[0] = dp.focus;
        u.uDof[1] = st.dof.focusRange;
        u.uDof[2] = st.dof.nearTransition;
        u.uDof[3] = st.dof.farTransition;
        u.uDof2[0] = st.dof.nearBlur;
        u.uDof2[1] = st.dof.farBlur;
        u.uDof2[2] = f.dof ? st.dof.weight : 0;
        u.uDof2[3] = this.storageScale();
        GPU.drawQuad(renderer, sh, rt, frame, { inputScale: [frame.width / input.width, frame.height / input.height] });
        this.passes++;
    }

    renderDof(renderer, frame, q, st, f) {
        const scale = q.dofScale;
        const rt = (this.rtDof = GPU.rt("dof", frame.width, frame.height, scale, { hdr: true }));
        const bq = BOKEH_QUALITY[String(st.bokeh.quality || "auto").toLowerCase()];
        const taps = Math.max(8, Math.min(64, bq && f.bokeh ? bq.taps : q.dofTaps));
        const key = "gather" + taps;
        if (!GPU.shaders[key]) {
            GPU.shaders[key] = PIXI.Shader.from(GLSL.QUAD_VERT, GLSL.DOF_GATHER_FRAG.replace("%TAPS%", String(taps)), {
                uFrame: F32(4), uInputScale: new Float32Array([1, 1]), uPrep: PIXI.Texture.WHITE, uTexel: F32(2), uMaxR: 1, uBokeh: F32(4)
            });
        }
        const sh = GPU.shaders[key];
        const u = sh.uniforms;
        const dp = this.dofParams(st);
        u.uPrep = this.rtPrep;
        u.uTexel[0] = 1 / this.rtPrep.baseTexture.realWidth;
        u.uTexel[1] = 1 / this.rtPrep.baseTexture.realHeight;
        u.uMaxR = Math.max(0.5, dp.radius * scale * st.dof.weight);
        u.uBokeh[0] = f.bokeh ? st.bokeh.intensity * st.bokeh.weight * 3 : 0;
        u.uBokeh[1] = st.bokeh.threshold;
        u.uBokeh[3] = 1 / this.storageScale();
        GPU.drawQuad(renderer, sh, rt, frame);
        this.passes++;
        const scatter = bq && bq.scatter !== undefined && String(st.bokeh.quality).toLowerCase() !== "auto" ? bq.scatter : q.bokehScatter;
        if (f.bokeh && scatter > 0 && st.bokeh.maxCount > 0) this.renderBokehSprites(renderer, frame, st, scatter, dp);
    }

    renderBokehSprites(renderer, frame, st, scatter, dp) {
        const count = U.clamp(Math.round(st.bokeh.maxCount * scatter), 4, 400);
        const aspect = frame.width / frame.height;
        const gw = Math.max(2, Math.round(Math.sqrt(count * aspect)));
        const gh = Math.max(2, Math.round(count / gw));
        const gridKey = gw + "x" + gh;
        const poolA = GPU.rtPixels("bokehA", gw, gh, true);
        const poolB = GPU.rtPixels("bokehB", gw, gh, true);
        if (!this._poolShaders) {
            const mk = mode => GPU.shader("bokehPool" + mode, GLSL.QUAD_VERT, GLSL.BOKEH_POOL_FRAG.replace("%MODE%", String(mode)), {
                uPrep: PIXI.Texture.WHITE, uGrid: F32(2), uBokeh: F32(4)
            });
            this._poolShaders = [mk(0), mk(1)];
        }
        const dest = new PIXI.Rectangle(0, 0, gw, gh);
        for (let m = 0; m < 2; m++) {
            const sh = this._poolShaders[m];
            sh.uniforms.uPrep = this.rtPrep;
            sh.uniforms.uGrid[0] = gw;
            sh.uniforms.uGrid[1] = gh;
            sh.uniforms.uBokeh[0] = st.bokeh.threshold;
            sh.uniforms.uBokeh[1] = 0.35;
            sh.uniforms.uBokeh[2] = 1 / this.storageScale();
            renderer.batch.flush();
            renderer.renderTexture.bind(m === 0 ? poolA : poolB, frame, dest);
            sh.uniforms.uFrame[0] = frame.x;
            sh.uniforms.uFrame[1] = frame.y;
            sh.uniforms.uFrame[2] = frame.width;
            sh.uniforms.uFrame[3] = frame.height;
            renderer.state.set(GPU.stateNone);
            renderer.shader.bind(sh);
            renderer.geometry.bind(GPU.quad, sh);
            renderer.geometry.draw(PIXI.DRAW_MODES.TRIANGLE_STRIP, 4, 0);
        }
        if (gridKey !== this.bokehGridKey) {
            this.bokehGridKey = gridKey;
            const n = gw * gh;
            const data = new Float32Array(n * 4 * 4);
            const idx = new Uint16Array(n * 6);
            let k = 0;
            for (let y = 0; y < gh; y++) {
                for (let x = 0; x < gw; x++) {
                    const corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
                    for (let c = 0; c < 4; c++) {
                        const o = (k * 4 + c) * 4;
                        data[o] = x;
                        data[o + 1] = y;
                        data[o + 2] = corners[c][0];
                        data[o + 3] = corners[c][1];
                    }
                    idx.set([k * 4, k * 4 + 1, k * 4 + 2, k * 4, k * 4 + 2, k * 4 + 3], k * 6);
                    k++;
                }
            }
            const buf = new PIXI.Buffer(data, true, false);
            this.bokehGeom = new PIXI.Geometry()
                .addAttribute("aCell", buf, 2, false, PIXI.TYPES.FLOAT, 16, 0)
                .addAttribute("aCorner", buf, 2, false, PIXI.TYPES.FLOAT, 16, 8)
                .addIndex(new PIXI.Buffer(idx, true, true));
            this.bokehCount = n;
        }
        if (!this._bokehShader) {
            this._bokehShader = PIXI.Shader.from(GLSL.BOKEH_VERT, GLSL.BOKEH_FRAG, {
                uGridColor: PIXI.Texture.WHITE, uGridPos: PIXI.Texture.WHITE, uFrame: F32(4), uGrid: F32(2), uMaxR: 1, uBokeh: F32(4)
            });
        }
        const sh = this._bokehShader;
        const u = sh.uniforms;
        const maxR = dp.radius * st.bokeh.size * 1.6;
        u.uGridColor = poolA;
        u.uGridPos = poolB;
        u.uFrame[0] = frame.x;
        u.uFrame[1] = frame.y;
        u.uFrame[2] = frame.width;
        u.uFrame[3] = frame.height;
        u.uGrid[0] = gw;
        u.uGrid[1] = gh;
        u.uMaxR = maxR;
        u.uBokeh[0] = st.bokeh.intensity * st.bokeh.weight;
        u.uBokeh[1] = st.bokeh.size;
        u.uBokeh[2] = dp.radius * 1.6;
        u.uBokeh[3] = 1 / this.storageScale();
        GPU.bindTarget(renderer, this.rtDof, frame);
        renderer.state.set(GPU.stateAdd);
        renderer.shader.bind(sh);
        renderer.geometry.bind(this.bokehGeom, sh);
        renderer.geometry.draw(PIXI.DRAW_MODES.TRIANGLES, this.bokehCount * 6, 0);
        this.passes += 3;
    }

    //-------------------------------------------------------------------------
    // 8. Bloom
    //-------------------------------------------------------------------------

    renderBloom(renderer, frame, q, st, f) {
        const levels = Math.max(1, q.bloomLevels);
        const base = q.bloomScale;
        const src = f.dof && this.rtDof ? this.rtDof : this.rtPrep;
        const rts = [];
        for (let i = 0; i < levels; i++) rts.push(GPU.rt("bloom" + i, frame.width, frame.height, base / Math.pow(2, i), { hdr: true }));
        this.rtBloom = rts[0];
        if (!this._bloomShaders) {
            this._bloomShaders = {
                bright: GPU.shader("bloomBright", GLSL.QUAD_VERT, GLSL.BLOOM_BRIGHT_FRAG, { uSrc: PIXI.Texture.WHITE, uDepthTex: PIXI.Texture.WHITE, uBloom: F32(4), uOutScale: 1 }),
                down: GPU.shader("bloomDown", GLSL.QUAD_VERT, GLSL.BLOOM_DOWN_FRAG, { uSrc: PIXI.Texture.WHITE, uTexel: F32(2) }),
                up: GPU.shader("bloomUp", GLSL.QUAD_VERT, GLSL.BLOOM_UP_FRAG, { uSrc: PIXI.Texture.WHITE, uTexel: F32(2), uGain: 1 })
            };
        }
        const S = this._bloomShaders;
        const b = st.bloom;
        S.bright.uniforms.uSrc = src;
        S.bright.uniforms.uDepthTex = f.depth && this.rtDepth ? this.rtDepth : GPU.textures.neutralDepth;
        S.bright.uniforms.uBloom[0] = b.threshold;
        S.bright.uniforms.uBloom[1] = b.knee;
        S.bright.uniforms.uBloom[2] = f.emissive ? b.emissive : 0;
        S.bright.uniforms.uBloom[3] = 1 / this.storageScale();
        S.bright.uniforms.uOutScale = this.storageScale();
        GPU.drawQuad(renderer, S.bright, rts[0], frame);
        const spread = U.clamp(b.radius, 0.1, 4);
        for (let i = 1; i < levels; i++) {
            const s = rts[i - 1];
            S.down.uniforms.uSrc = s;
            S.down.uniforms.uTexel[0] = spread / s.baseTexture.realWidth;
            S.down.uniforms.uTexel[1] = spread / s.baseTexture.realHeight;
            GPU.drawQuad(renderer, S.down, rts[i], frame);
        }
        for (let i = levels - 1; i >= 1; i--) {
            const s = rts[i];
            S.up.uniforms.uSrc = s;
            S.up.uniforms.uTexel[0] = (spread * 0.5) / s.baseTexture.realWidth;
            S.up.uniforms.uTexel[1] = (spread * 0.5) / s.baseTexture.realHeight;
            S.up.uniforms.uGain = 1;
            GPU.drawQuad(renderer, S.up, rts[i - 1], frame, { blend: "add" });
        }
        this.passes += levels * 2;
    }

    //-------------------------------------------------------------------------
    // 9. Final pass uniforms
    //-------------------------------------------------------------------------

    setFinalUniforms(filter, st, f, W, H) {
        const u = filter.uniforms;
        if (this._shade) this.applyShade(u);
        if (this.kind !== "map") {
            u.uDepthTex = GPU.textures.neutralDepth;
            u.uLightTex = GPU.textures.white;
            u.uOverlay = GPU.textures.black;
            u.uNoise = GPU.textures.noise;
        }
        u.uDofTex = f.dof && this.rtDof ? this.rtDof : GPU.textures.black;
        u.uBloomTex = f.bloom && this.rtBloom ? this.rtBloom : GPU.textures.black;
        u.uFinalCfg[0] = f.dof && this.rtDof ? 1 : 0;
        u.uFinalCfg[1] = f.bloom ? st.bloom.intensity * st.bloom.weight : 0;
        u.uFinalCfg[2] = 1 / this.storageScale();
        u.uFinalCfg[3] = this.kind === "map" ? Debug.view : 0;
        // Rim light: screen-space edge facing the light.
        const rim = st.rim;
        if (f.rim) {
            const cam = this.spriteset._hd2dCamera;
            const rot = cam ? Math.atan2(cam.worldTransform.b, cam.worldTransform.a) : 0;
            const angle = ((rim.followSun ? st.sun.angle : rim.angle) * Math.PI) / 180 + rot;
            const px = Math.max(0.5, rim.width) * Math.max(1, Camera.zoom() * 0.75);
            u.uRim[0] = rim.color[0];
            u.uRim[1] = rim.color[1];
            u.uRim[2] = rim.color[2];
            u.uRim[3] = rim.intensity * rim.weight;
            u.uRim2[0] = (Math.cos(angle) * px) / W;
            u.uRim2[1] = (Math.sin(angle) * px) / H;
        } else {
            u.uRim[3] = 0;
        }
        // Color grading.
        const g = st.grade;
        u.uGradeA[0] = Math.pow(2, g.exposure);
        u.uGradeA[1] = g.contrast;
        u.uGradeA[2] = g.saturation;
        u.uGradeA[3] = g.brightness;
        u.uGradeB[0] = g.gamma;
        u.uGradeB[1] = (g.hue * Math.PI) / 180;
        u.uGradeB[2] = g.temperature;
        u.uGradeB[3] = g.tint;
        u.uGradeS.set([g.shadowColor[0], g.shadowColor[1], g.shadowColor[2], g.shadowAmount]);
        u.uGradeH.set([g.highlightColor[0], g.highlightColor[1], g.highlightColor[2], g.highlightAmount]);
        const lut = f.grade && g.lut ? Lut.get(g.lut) : null;
        u.uLut = lut ? lut.texture : GPU.textures.white;
        u.uGradeC[0] = f.grade ? g.weight : 0;
        u.uGradeC[1] = lut ? lut.size : 16;
        u.uGradeC[2] = U.saturate(g.lutStrength);
        u.uGradeC[3] = lut && GPU.maxTextureUnits >= 8 ? 1 : 0;
        // Vignette.
        const v = st.vignette;
        const pulse = v.pulse > 0 ? 1 + v.pulse * Math.sin((this.time / 60) * Math.PI * 2 * v.pulseSpeed) : 1;
        u.uVig[0] = Math.max(0, v.intensity * pulse);
        u.uVig[1] = v.radius;
        u.uVig[2] = Math.max(0.01, v.softness);
        u.uVig[3] = W / H;
        u.uVigColor.set([v.color[0], v.color[1], v.color[2], f.vignette ? v.weight : 0]);
        u.uDebug[0] = this.dofParams(st).focus;
        u.uDebug[1] = st.depth.focalDepth;
    }
}
HD2D.Pipeline = Pipeline;

//=============================================================================
// 18. LUT loader (optional color lookup tables)
//=============================================================================

const Lut = (HD2D.Lut = {
    cache: {},
    get(name) {
        let e = this.cache[name];
        if (!e) {
            const url = "img/pictures/" + Utils.encodeURI(name) + ".png";
            const bitmap = Bitmap.load(url);
            e = this.cache[name] = { bitmap, ready: false, texture: null, size: 16 };
            bitmap.addLoadListener(() => {
                e.ready = true;
                e.size = bitmap.height;
                const base = bitmap.baseTexture;
                base.scaleMode = PIXI.SCALE_MODES.LINEAR;
                e.texture = new PIXI.Texture(base);
                if (bitmap.width !== bitmap.height * bitmap.height) {
                    U.warnOnce("LUT '" + name + "' should be a horizontal strip of size (N*N) x N, e.g. 256x16.");
                }
            });
        }
        if (!e.ready && e.bitmap.isError()) {
            U.warnOnce("LUT image not found: img/pictures/" + name + ".png");
            e.failed = true;
        }
        return e.ready && e.texture ? e : null;
    }
});


//=============================================================================
// 19. Particle runtime
//=============================================================================

class ParticleEmitter {
    constructor(cfg, system) {
        this.cfg = cfg;
        this.sys = system;
        this.def = PARTICLE_TYPES[cfg.type] || PARTICLE_TYPES.dust;
        this.list = [];
        this.fade = 0;
        this.dying = false;
        this.dead = false;
        const emissive = cfg.emissive !== undefined && cfg.emissive !== null ? cfg.emissive : this.def.emissive;
        this.emissive = !!emissive && State.effectOn("emissive");
        this.container = this.emissive ? system.ss._hd2dUnlit : system.ss._hd2dParticles;
        this.color = cfg.color || null;
    }

    depthRange() {
        const d = this.def.depth;
        let a = this.cfg.depthMin !== undefined ? this.cfg.depthMin : d[0];
        let b = this.cfg.depthMax !== undefined ? this.cfg.depthMax : d[1];
        if (a > b) [a, b] = [b, a];
        return [U.clamp(a, 0, 100), U.clamp(b, 0, 100)];
    }

    targetCount() {
        const amount = this.cfg.amount !== undefined ? this.cfg.amount : 20;
        return Math.max(0, Math.round(amount * State.quality().particleMult * P.particleDensity));
    }

    spawn(p, initial) {
        const def = this.def;
        const sys = this.sys;
        const [d0, d1] = this.depthRange();
        p.depth = U.rand(d0, d1);
        p.factor = Depth.parallaxFactor(p.depth);
        const F = HD2D.state().depth.focalDepth;
        p.sizeMul = p.depth < F ? 1 + ((F - p.depth) / Math.max(F, 1)) * 0.8 : 1 - ((p.depth - F) / Math.max(100 - F, 1)) * 0.5;
        p.alphaMul = p.depth < F ? 1 - ((F - p.depth) / Math.max(F, 1)) * 0.25 : 1 - ((p.depth - F) / Math.max(100 - F, 1)) * 0.45;
        p.size = U.rand(def.size[0], def.size[1]) * (this.cfg.size || 1);
        const speed = this.cfg.speed !== undefined ? this.cfg.speed : 1;
        p.vx = U.rand(def.vx[0], def.vx[1]) * speed + (this.cfg.wind || 0);
        p.vy = U.rand(def.vy[0], def.vy[1]) * speed;
        p.life = U.rand(def.life[0], def.life[1]);
        p.age = initial && def.life[0] < 900 ? Math.random() * p.life : 0;
        p.phase = Math.random() * 1000;
        p.rot = Math.random() * Math.PI * 2;
        const span = sys.span;
        if (this.cfg.area === "event" && this.cfg.eventId) {
            const ev = $gameMap.event(this.cfg.eventId);
            const r = this.cfg.radius !== undefined ? this.cfg.radius : 20;
            const tw = $gameMap.tileWidth();
            const th = $gameMap.tileHeight();
            p.mx = ev ? (ev._realX + 0.5) * tw + U.rand(-r, r) : 0;
            p.my = ev ? (ev._realY + 0.5) * th - th * 0.3 + U.rand(-r * 0.5, r * 0.5) : 0;
            p.anchored = true;
        } else {
            p.lx = Math.random() * span.w + Camera.contX * p.factor;
            p.ly = Math.random() * span.h + Camera.contY * p.factor;
            p.anchored = false;
        }
        const colors = this.color ? null : def.rgbs;
        p.rgb = this.color || (colors ? colors[Math.floor(Math.random() * colors.length)] : def.rgb);
        p.sprite.tint = U.colorInt(p.rgb);
        p.sprite.blendMode = def.blend === 1 ? PIXI.BLEND_MODES.ADD : PIXI.BLEND_MODES.NORMAL;
        p.level = -1;
    }

    create() {
        const tex = new PIXI.Texture(GPU.atlas.base, GPU.atlasTexture(this.def.tex, 0).frame.clone());
        const sprite = new PIXI.Sprite(tex);
        sprite.anchor.set(0.5);
        this.container.addChild(sprite);
        const p = { sprite };
        this.spawn(p, true);
        this.list.push(p);
    }

    update() {
        if (this.dying) this.fade = Math.max(0, this.fade - 1 / 60);
        else this.fade = Math.min(1, this.fade + 1 / 45);
        const target = this.dying ? 0 : this.targetCount();
        while (this.list.length < target) this.create();
        if (this.list.length > target && (this.dying ? this.fade <= 0 : true)) {
            while (this.list.length > target) {
                const p = this.list.pop();
                p.sprite.destroy({ texture: true });
            }
        }
        if (this.dying && this.fade <= 0) {
            this.destroy();
            this.dead = true;
            return;
        }
        const def = this.def;
        const sys = this.sys;
        const span = sys.span;
        const st = HD2D.state();
        const dofW = sys.dofBlur ? st.dof.weight : 0;
        const tw = $gameMap.tileWidth();
        const th = $gameMap.tileHeight();
        for (const p of this.list) {
            p.age++;
            const f = p.factor;
            const wob = def.wobble ? Math.sin(p.age * 0.03 + p.phase) * def.wobble * 0.3 : 0;
            let sx;
            let sy;
            if (p.anchored) {
                p.mx += (p.vx + wob) * 0.5;
                p.my += p.vy * 0.5;
                sx = $gameMap.adjustX(p.mx / tw) * tw;
                sy = $gameMap.adjustY(p.my / th) * th;
            } else {
                p.lx += (p.vx + wob) * f;
                p.ly += p.vy * f;
                sx = (((p.lx - Camera.contX * f) % span.w) + span.w) % span.w - span.m;
                sy = def.beam ? span.h * 0.35 - span.m : (((p.ly - Camera.contY * f) % span.h) + span.h) % span.h - span.m;
            }
            if (p.age > p.life) this.spawn(p, false);
            const lifeFade = p.life >= 900 ? 1 : U.smoothstep(0, 40, p.age) * (1 - U.smoothstep(p.life - 40, p.life, p.age));
            let twinkle = 1;
            if (def.twinkle > 0) {
                const n = U.noise1(p.age * 0.03 + p.phase);
                twinkle = 1 - def.twinkle + def.twinkle * U.smoothstep(0.3, 0.75, n);
            }
            const s = p.sprite;
            s.x = sx;
            s.y = sy;
            let alpha = def.alpha * (this.cfg.opacity !== undefined ? this.cfg.opacity : 1) * p.alphaMul * lifeFade * twinkle * this.fade;
            if (def.beam) {
                alpha *= 0.6 + 0.4 * Math.sin(p.age * 0.01 + p.phase);
                s.rotation = 0.38;
                s.scale.set((p.size * p.sizeMul) / 64, (span.h * 1.5) / 256);
            } else if (def.streak) {
                s.rotation = Math.atan2(p.vy, p.vx) - Math.PI / 2;
                s.scale.set(p.size * p.sizeMul, (Math.hypot(p.vx, p.vy) / 12) * p.sizeMul);
            } else {
                if (def.spin) {
                    p.rot += def.spin * f;
                    s.rotation = p.rot;
                }
                const base = GPU.atlasTexture(def.tex, 0).frame;
                const px = (p.size * p.sizeMul) / Math.max(base.width * 0.5, 1);
                s.scale.set(px);
            }
            s.alpha = U.saturate(alpha);
            // Out-of-focus particles use a pre-blurred variant of their texture.
            if (!def.beam && def.tex !== "glow" && def.tex !== "puff") {
                const maxBlur = def.maxBlur !== undefined ? def.maxBlur : 3;
                const level = dofW > 0 ? Math.min(maxBlur, Math.round(Math.abs(Depth.coc(p.depth, st.dof)) * 3 * dofW)) : 0;
                if (level !== p.level) {
                    p.level = level;
                    const fr = GPU.atlasTexture(def.tex, level).frame;
                    s.texture.frame.copyFrom(fr);
                    s.texture.updateUvs();
                }
            }
        }
    }

    count() {
        return this.list.length;
    }

    destroy() {
        for (const p of this.list) p.sprite.destroy({ texture: true });
        this.list = [];
    }
}

class ParticleSystem {
    constructor(spriteset) {
        this.ss = spriteset;
        this.emitters = new Map();
        this.span = { w: 0, h: 0, m: 64 };
        this.dofBlur = false;
    }

    desired() {
        const list = [];
        if (!State.effectOn("particles")) return list;
        const st = HD2D.state();
        for (const e of st.particles || []) list.push(e);
        // Event emitters from note / comment tags.
        for (const ev of $gameMap.events()) {
            if (ev._erased || ev._pageIndex < 0) continue;
            for (const e of ev.hd2dTags().particles) list.push(Object.assign({ area: "event", eventId: ev.eventId() }, e));
        }
        // Emitters created by plugin commands.
        const mapId = $gameMap.mapId();
        for (const e of Object.values(State.data().emitters)) {
            if (e && (e.scope === "global" || e.mapId === mapId)) list.push(e);
        }
        // RPG Maker weather rendered as depth particles.
        const type = $gameScreen.weatherType();
        if (this.depthWeather() && type !== "none") {
            const power = $gameScreen.weatherPower();
            const per = { rain: 14, storm: 20, snow: 10 }[type] || 10;
            if (PARTICLE_TYPES[type]) list.push({ type, amount: Math.round(power * per), weather: true });
        }
        return list;
    }

    depthWeather() {
        return State.effectOn("weather") && State.effectOn("particles");
    }

    update() {
        const zoom = Camera.zoom();
        this.span.w = Graphics.width / zoom + this.span.m * 2;
        this.span.h = Graphics.height / zoom + this.span.m * 2;
        this.dofBlur = State.effectOn("dof") && State.effectOn("depth");
        const wanted = this.desired();
        const seen = new Set();
        for (const cfg of wanted) {
            const emissive = cfg.emissive !== undefined && cfg.emissive !== null ? cfg.emissive : (PARTICLE_TYPES[cfg.type] || {}).emissive;
            const sig = Particles.signature(cfg) + "|" + (emissive && State.effectOn("emissive") ? "u" : "l");
            if (seen.has(sig)) continue;
            seen.add(sig);
            let em = this.emitters.get(sig);
            if (!em || em.dead) {
                em = new ParticleEmitter(cfg, this);
                this.emitters.set(sig, em);
            } else {
                em.cfg = cfg;
                em.dying = false;
            }
        }
        for (const [sig, em] of this.emitters) {
            if (!seen.has(sig)) em.dying = true;
            em.update();
            if (em.dead) this.emitters.delete(sig);
        }
        if (this.ss._weather) this.ss._weather._hd2dHideSprites = this.depthWeather();
    }

    count() {
        let n = 0;
        for (const em of this.emitters.values()) n += em.count();
        return n;
    }

    destroy() {
        for (const em of this.emitters.values()) em.destroy();
        this.emitters.clear();
    }
}
HD2D.ParticleSystem = ParticleSystem;

//=============================================================================
// 20. Parallax layer runtime
//=============================================================================

class LayerSystem {
    constructor(spriteset) {
        this.ss = spriteset;
        this.sprites = new Map();
        this.scroll = new Map();
    }

    update() {
        const ss = this.ss;
        const st = HD2D.state();
        const parallaxOn = State.effectOn("parallax") && st.parallax.weight > 0;
        const list = Layers.current();
        const ids = new Set();
        const zoom = Camera.zoom();
        const W = Graphics.width;
        const H = Graphics.height;
        const viewW = W / zoom;
        const viewH = H / zoom;
        let background = false;
        for (const L of list) {
            if (!L || L.visible === false) continue;
            ids.add(L.id);
            let sprite = this.sprites.get(L.id);
            const key = L.image + "|" + L.folder + "|" + (L.loopX || L.loopY ? "t" : "s");
            if (sprite && sprite._hd2dKey !== key) {
                sprite.parent && sprite.parent.removeChild(sprite);
                sprite.destroy();
                sprite = null;
            }
            if (!sprite) {
                const bitmap = ImageManager.loadBitmap("img/" + L.folder + "/", L.image);
                sprite = L.loopX || L.loopY ? new TilingSprite(bitmap) : new Sprite(bitmap);
                sprite._hd2dKey = key;
                sprite._hd2dLayer = true;
                this.sprites.set(L.id, sprite);
            }
            const front = L.front !== null && L.front !== undefined ? L.front : L.depth < st.depth.focalDepth;
            const container = front ? ss._hd2dFront : ss._hd2dBack;
            if (sprite.parent !== container) {
                if (sprite.parent) sprite.parent.removeChild(sprite);
                container.addChild(sprite);
                this.sortContainer(container);
            }
            sprite._hd2dDepth = L.depth;
            sprite.opacity = L.opacity;
            sprite.blendMode = L.blend;
            if (!front) background = true;
            // Scroll factor from depth (or explicit), camera zoom influence.
            const auto = Depth.parallaxFactor(L.depth, st.parallax);
            const fx = parallaxOn ? (L.factorX !== null && L.factorX !== undefined ? L.factorX : auto) : 1;
            const fy = parallaxOn ? (L.factorY !== null && L.factorY !== undefined ? L.factorY : auto) : 1;
            const infl = L.zoomInfluence !== null && L.zoomInfluence !== undefined ? L.zoomInfluence : st.parallax.zoomInfluence;
            const layerZoom = U.lerp(zoom, 1 + (zoom - 1) * Math.min(1, auto), U.saturate(infl));
            const k = (layerZoom / zoom) * (L.scale || 1);
            const acc = this.scroll.get(L.id) || { x: 0, y: 0 };
            acc.x += L.scrollX || 0;
            acc.y += L.scrollY || 0;
            this.scroll.set(L.id, acc);
            // Placement: (x, y) is where the image sits while the camera is at the
            // map's top-left corner; it then scrolls by camera position * factor
            // (factor 1 = moves with the map, 0 = fixed on screen). Zoom scales
            // the layer around the view center. Positive auto-scroll moves the
            // image right / down.
            const bw = sprite.bitmap ? sprite.bitmap.width : 0;
            const bh = sprite.bitmap ? sprite.bitmap.height : 0;
            sprite.visible = bw > 0 && bh > 0;
            if (!sprite.visible) continue;
            const cx = viewW / 2;
            const cy = viewH / 2;
            const px = L.x + acc.x - Camera.contX * fx; // unscaled left edge
            const py = L.y + acc.y - Camera.contY * fy; // unscaled top edge
            sprite.scale.set(k);
            if (sprite instanceof TilingSprite) {
                // A tiling sprite repeats on both axes, so a non-looping axis is
                // sized to the image and positioned instead.
                const w = L.loopX ? viewW / k : bw;
                const h = L.loopY ? viewH / k : bh;
                sprite.move(0, 0, w, h);
                if (L.loopX) {
                    sprite.x = 0;
                    sprite.origin.x = -px + cx - cx / k;
                } else {
                    sprite.origin.x = 0;
                    sprite.x = cx + (px - cx) * k;
                }
                if (L.loopY) {
                    sprite.y = 0;
                    sprite.origin.y = -py + cy - cy / k;
                } else {
                    sprite.origin.y = 0;
                    sprite.y = cy + (py - cy) * k;
                }
            } else {
                sprite.x = cx + (px - cx) * k;
                sprite.y = cy + (py - cy) * k;
            }
        }
        for (const [id, sprite] of this.sprites) {
            if (ids.has(id)) continue;
            if (sprite.parent) sprite.parent.removeChild(sprite);
            sprite.destroy();
            this.sprites.delete(id);
            this.scroll.delete(id);
        }
        ss._hd2dBackgroundMode = background || ss._hd2dParallaxDepth !== null;
    }

    /** Back container: farthest first. Front container: nearest last. */
    sortContainer(container) {
        container.children.sort((a, b) => {
            const da = a._hd2dDepth === undefined ? 50 : a._hd2dDepth;
            const db = b._hd2dDepth === undefined ? 50 : b._hd2dDepth;
            return db - da;
        });
    }
}

//=============================================================================
// 21. Light glows (soft additive halos, unlit)
//=============================================================================

class GlowSystem {
    constructor(spriteset) {
        this.ss = spriteset;
        this.sprites = [];
    }

    update(active) {
        let n = 0;
        if (active) {
            for (const L of Lights.list) {
                if (L.glow <= 0.001) continue;
                let s = this.sprites[n];
                if (!s) {
                    s = new PIXI.Sprite(new PIXI.Texture(GPU.atlas.base, GPU.atlasTexture("glow").frame.clone()));
                    s.anchor.set(0.5);
                    s.blendMode = PIXI.BLEND_MODES.ADD;
                    this.ss._hd2dUnlit.addChild(s);
                    this.sprites.push(s);
                }
                s.visible = true;
                s.x = L.x;
                s.y = L.y;
                const r = Math.min(L.radius * 0.45, 96);
                s.scale.set(r / 32);
                s.tint = U.colorInt(L.color);
                s.alpha = U.saturate(L.glow * Math.min(L.intensity, 1.5) * 0.55);
                n++;
            }
        }
        for (let i = n; i < this.sprites.length; i++) this.sprites[i].visible = false;
    }
}

//=============================================================================
// 22. Screen effects: letterbox and colored fades (above pictures)
//=============================================================================

class ScreenFx extends PIXI.Container {
    constructor() {
        super();
        this.fadeG = new PIXI.Graphics();
        this.barG = new PIXI.Graphics();
        this.addChild(this.fadeG);
        this.addChild(this.barG);
        this._fadeKey = "";
        this._barKey = "";
    }

    update() {
        const on = Camera.enabled();
        const c = Camera.data();
        const W = Graphics.width;
        const H = Graphics.height;
        const fade = on ? c.fade : { alpha: 0, color: [0, 0, 0] };
        const fk = fade.alpha.toFixed(3) + U.colorHex(fade.color) + W + "x" + H;
        if (fk !== this._fadeKey) {
            this._fadeKey = fk;
            this.fadeG.clear();
            if (fade.alpha > 0.001) {
                this.fadeG.beginFill(U.colorInt(fade.color), U.saturate(fade.alpha));
                this.fadeG.drawRect(0, 0, W, H);
                this.fadeG.endFill();
            }
        }
        const bar = on ? Math.round(c.letterbox * H) : 0;
        const bk = bar + "|" + W + "x" + H;
        if (bk !== this._barKey) {
            this._barKey = bk;
            this.barG.clear();
            if (bar > 0) {
                this.barG.beginFill(0x000000, 1);
                this.barG.drawRect(0, 0, W, bar);
                this.barG.drawRect(0, H - bar, W, bar);
                this.barG.endFill();
            }
        }
    }
}

//=============================================================================
// 23. Spriteset_Map integration
//=============================================================================

/** True while the current scene is a map with an HD2D spriteset. */
HD2D.mapSpriteset = () => {
    const scene = SceneManager._scene;
    return scene && scene instanceof Scene_Map && scene._spriteset && scene._spriteset._hd2dPipeline ? scene._spriteset : null;
};

const _Spriteset_Map_initialize = Spriteset_Map.prototype.initialize;
Spriteset_Map.prototype.initialize = function() {
    _Spriteset_Map_initialize.apply(this, arguments);
    try {
        this.createHD2D();
    } catch (e) {
        console.error("[HD2D] Could not set up the map spriteset; HD2D disabled on this map.", e);
        this._hd2dPipeline = null;
    }
};

Spriteset_Map.prototype.createHD2D = function() {
    this._hd2dPipeline = null;
    this._hd2dParallaxDepth = null;
    this._hd2dBackgroundMode = false;
    if (GPU.failed || !Graphics.app || !this._baseSprite || !this._tilemap) return;
    const renderer = U.renderer();
    if (!renderer || !renderer.gl) return;
    if (!GPU.init(renderer)) return;
    const base = this._baseSprite;
    // World containers inside _baseSprite (so the screen tone still applies).
    this._hd2dBack = new Sprite();
    this._hd2dParticles = new Sprite();
    this._hd2dFront = new Sprite();
    base.addChildAt(this._hd2dBack, Math.max(0, base.children.indexOf(this._tilemap)));
    base.addChildAt(this._hd2dParticles, base.children.indexOf(this._tilemap) + 1);
    base.addChildAt(this._hd2dFront, base.children.indexOf(this._hd2dParticles) + 1);
    // Camera (zoom / rotation / shake) and post-processing wrappers.
    this._hd2dUnlit = new Sprite();
    this._hd2dUnlit.renderable = false;
    this._hd2dCamera = new Sprite();
    this._hd2dPost = new Sprite();
    const index = Math.max(0, this.children.indexOf(base));
    this.removeChild(base);
    this._hd2dCamera.addChild(base);
    if (this._weather && this._weather.parent === this) {
        this.removeChild(this._weather);
        this._hd2dCamera.addChild(this._weather);
    }
    this._hd2dCamera.addChild(this._hd2dUnlit);
    this._hd2dPost.addChild(this._hd2dCamera);
    this.addChildAt(this._hd2dPost, Math.min(index, this.children.length));
    if (P.postOnPictures && this._pictureContainer && this._pictureContainer.parent === this) {
        this.removeChild(this._pictureContainer);
        this._hd2dPost.addChild(this._pictureContainer);
    }
    this._hd2dPost.filterArea = new PIXI.Rectangle(0, 0, Graphics.width, Graphics.height);
    this._hd2dScreenFx = new ScreenFx();
    this.addChild(this._hd2dScreenFx);
    this._hd2dPictureSprites = this._pictureContainer ? this._pictureContainer.children.filter(c => c instanceof Sprite_Picture) : [];
    // Systems.
    this._hd2dPipeline = new Pipeline(this, "map");
    this._hd2dParticleSystem = new ParticleSystem(this);
    this._hd2dLayerSystem = new LayerSystem(this);
    this._hd2dGlows = new GlowSystem(this);
    for (const sprite of this._characterSprites) sprite._hd2dSpriteset = this;
    Debug.attach(this);
    this.preUpdateHD2D(true);
};

const _Spriteset_Map_destroy = Spriteset_Map.prototype.destroy;
Spriteset_Map.prototype.destroy = function(options) {
    if (this._hd2dParticleSystem) this._hd2dParticleSystem.destroy();
    this._hd2dPipeline = null;
    Debug.detach(this);
    _Spriteset_Map_destroy.call(this, options);
};

const _Spriteset_Map_update = Spriteset_Map.prototype.update;
Spriteset_Map.prototype.update = function() {
    if (this._hd2dPipeline) this.preUpdateHD2D(false);
    _Spriteset_Map_update.call(this);
    if (this._hd2dPipeline) {
        try {
            this.postUpdateHD2D();
        } catch (e) {
            console.error("[HD2D] Update error - HD2D disabled on this map.", e);
            this._hd2dPost.filters = null;
            this._hd2dPipeline = null;
        }
    }
};

/** Per-frame values needed before the character sprites update. */
Spriteset_Map.prototype.preUpdateHD2D = function(instant) {
    State.update();
    Adaptive.update();
    Depth.zoom = Camera.zoom();
    Depth.viewHeight = Graphics.height;
    Depth.updateFocal(instant);
    this._hd2dHasNormals = false;
    this.updateHD2DViewSize();
};

/** Keeps the tilemap / MZ parallax large enough when zoomed out. */
Spriteset_Map.prototype.updateHD2DViewSize = function() {
    const zoom = Camera.zoom();
    const vw = Math.ceil(Graphics.width / Math.min(zoom, 1));
    const vh = Math.ceil(Graphics.height / Math.min(zoom, 1));
    const tilemap = this._tilemap;
    if (tilemap.width !== vw || tilemap.height !== vh) {
        tilemap.width = vw;
        tilemap.height = vh;
        tilemap.refresh();
    }
    if (this._parallax && (this._parallax._width !== vw || this._parallax._height !== vh)) {
        this._parallax.move(0, 0, vw, vh);
    }
};

Spriteset_Map.prototype.postUpdateHD2D = function() {
    const W = Graphics.width;
    const H = Graphics.height;
    // Camera transform on the world (pictures / windows are not affected).
    const cam = this._hd2dCamera;
    const zoom = Camera.zoom();
    const rotDeg = Camera.rotation();
    const rot = (rotDeg * Math.PI) / 180;
    let overscan = 1;
    if (P.rotationOverscan && Math.abs(rot) > 0.0001) {
        const ratio = Math.max(W / H, H / W);
        overscan = Math.abs(Math.cos(rot)) + Math.abs(Math.sin(rot)) * ratio;
    }
    const shake = Camera.shakeOffset();
    cam.pivot.set(W / (2 * zoom), H / (2 * zoom));
    cam.position.set(W / 2 + shake.x, H / 2 + shake.y);
    cam.scale.set(zoom * overscan);
    cam.rotation = rot;
    const fa = this._hd2dPost.filterArea;
    if (fa.width !== W || fa.height !== H) {
        fa.width = W;
        fa.height = H;
    }
    // Systems.
    const viewW = W / zoom;
    const viewH = H / zoom;
    Lights.update(viewW, viewH);
    this._hd2dLayerSystem.update();
    this._hd2dParticleSystem.update();
    const flags = this._hd2dPipeline.computeFlags();
    this._hd2dGlows.update(flags.lights);
    this.updateHD2DPictures();
    this._hd2dPost.filters = flags.any && !this._hd2dPipeline.failed ? [this._hd2dPipeline.filter] : null;
    Debug.update(this);
};

/** MZ map parallax: optional virtual depth via <HD2DParallaxDepth: n>. */
const _Spriteset_Map_updateParallax = Spriteset_Map.prototype.updateParallax;
Spriteset_Map.prototype.updateParallax = function() {
    _Spriteset_Map_updateParallax.call(this);
    if (!this._hd2dPipeline) return;
    const depth = MapTags.parallaxDepth;
    this._hd2dParallaxDepth = depth;
    if (depth === null || !this._parallax.bitmap || !this._parallax.bitmap.width) return;
    const st = HD2D.state();
    const f = State.effectOn("parallax") ? Depth.parallaxFactor(depth, st.parallax) : 1;
    const bitmap = this._parallax.bitmap;
    this._hd2dParallaxScroll = this._hd2dParallaxScroll || { x: 0, y: 0 };
    this._hd2dParallaxScroll.x += ($dataMap.parallaxLoopX ? $dataMap.parallaxSx : 0) / 2;
    this._hd2dParallaxScroll.y += ($dataMap.parallaxLoopY ? $dataMap.parallaxSy : 0) / 2;
    this._parallax.origin.x = (Camera.contX * f + this._hd2dParallaxScroll.x) % bitmap.width;
    this._parallax.origin.y = (Camera.contY * f + this._hd2dParallaxScroll.y) % bitmap.height;
    this._parallax._hd2dDepth = depth;
};

/** Pictures given a depth or emissive strength join the world (DOF, lighting, bloom). */
Spriteset_Map.prototype.updateHD2DPictures = function() {
    const data = State.data().pictures;
    const focal = HD2D.state().depth.focalDepth;
    for (const sprite of this._hd2dPictureSprites) {
        const info = data[sprite._pictureId];
        const inWorld = info && (U.isNum(info.depth) || info.emissive > 0);
        let target = this._pictureContainer;
        if (inWorld) {
            const depth = U.isNum(info.depth) ? info.depth : focal;
            sprite._hd2dDepth = depth;
            sprite._hd2dEmissive = info.emissive || 0;
            target = depth > focal ? this._hd2dBack : this._hd2dFront;
        } else {
            sprite._hd2dDepth = undefined;
            sprite._hd2dEmissive = 0;
        }
        if (sprite.parent !== target && target) {
            if (sprite.parent) sprite.parent.removeChild(sprite);
            if (target === this._pictureContainer) {
                const list = target.children;
                let i = 0;
                while (i < list.length && list[i]._pictureId !== undefined && list[i]._pictureId < sprite._pictureId) i++;
                target.addChildAt(sprite, i);
            } else {
                target.addChild(sprite);
                this._hd2dLayerSystem.sortContainer(target);
            }
        }
    }
};

//-----------------------------------------------------------------------------
// Per-character data (depth, emissive, rim, shadow, foreground, scale)
//-----------------------------------------------------------------------------

const _Sprite_Character_update = Sprite_Character.prototype.update;
Sprite_Character.prototype.update = function() {
    _Sprite_Character_update.call(this);
    if (this._hd2dSpriteset && this._hd2dSpriteset._hd2dPipeline && this._character) {
        this.updateHD2D();
    }
};

Sprite_Character.prototype.updateHD2D = function() {
    const ch = this._character;
    const ss = this._hd2dSpriteset;
    const st = HD2D.state();
    const tags = ch.hd2dTags ? ch.hd2dTags() : EMPTY_TAGS;
    const h = this._hd2d || (this._hd2d = {});
    const res = Depth.forCharacter(ch);
    h.depth = res.depth;
    h.explicit = res.explicit;
    const ov = State.data().depth[characterKey(ch)];
    h.emissive = ov && U.isNum(ov.emissive) ? ov.emissive : tags.emissive || 0;
    const isActor = ch === $gamePlayer || ch instanceof Game_Follower;
    if (tags.rim !== null) h.rim = tags.rim;
    else h.rim = isActor ? 1 : this.isEmptyCharacter() ? 0 : ch.isObjectCharacter() || this._tileId > 0 ? 0.35 : 0.8;
    h.alpha = this.alpha;
    // Shadows: characters by default, not tile/object events or airships.
    if (tags.shadow !== null) h.shadow = tags.shadow && !this.isEmptyCharacter();
    else if (this.isEmptyCharacter() || this._tileId > 0) h.shadow = false;
    else if (ch instanceof Game_Vehicle) h.shadow = ch._type !== "airship";
    else if (ch.isObjectCharacter()) h.shadow = P.objectShadows;
    else h.shadow = true;
    if (ch === $gamePlayer && $gamePlayer.isInAirship && $gamePlayer.isInAirship()) h.shadow = false;
    // Normal map.
    h.normalTexture = null;
    if (State.effectOn("normalMaps") && State.quality().normalMaps && this._characterName && this._tileId === 0) {
        const base = NormalMaps.get(this._characterName, tags.normalMap);
        if (base && this._texture && this._texture.valid) {
            const frame = this._texture.frame;
            if (frame.x + frame.width <= base.width && frame.y + frame.height <= base.height) {
                if (!this._hd2dNormalTex || this._hd2dNormalTex.baseTexture !== base) this._hd2dNormalTex = new PIXI.Texture(base, frame.clone());
                const nt = this._hd2dNormalTex;
                if (!nt.frame.equals(frame)) nt.frame = frame.clone();
                h.normalTexture = nt;
                ss._hd2dHasNormals = true;
            }
        }
    }
    this.updateHD2DForeground(tags, st, ss);
    // Depth-based scale (simulated perspective) and manual scale.
    let scale = tags.scale !== null ? tags.scale : 1;
    if (!tags.noScale && st.perspective.enabled && State.effectOn("perspective")) {
        scale *= U.lerp(1, Depth.perspectiveScale(h.depth, st.perspective), st.perspective.weight);
    }
    if (this._hd2dIsForeground && tags.foreground && tags.foreground.scale !== null) scale *= tags.foreground.scale;
    if (scale !== 1 || this._hd2dScaled) {
        this.scale.set(scale);
        this._hd2dScaled = scale !== 1;
    }
    // Optional sorting by depth instead of screen Y.
    if ((P.sortByDepth || tags.sortDepth) && h.explicit) {
        this._hd2dSortY = (Depth.inverse(h.depth, st.depth) * Graphics.height) / Math.max(Camera.zoom(), 0.01);
    } else if (this._hd2dSortY !== undefined) {
        this._hd2dSortY = undefined;
    }
};

/** Foreground framing: moves the sprite above the map, with parallax and fading. */
Sprite_Character.prototype.updateHD2DForeground = function(tags, st, ss) {
    const fg = tags.foreground;
    if (fg && !this._hd2dIsForeground) {
        this._hd2dHomeParent = this.parent;
        if (this.parent) this.parent.removeChild(this);
        ss._hd2dFront.addChild(this);
        this._hd2dIsForeground = true;
        this._hd2dFgAlpha = 1;
    } else if (!fg && this._hd2dIsForeground) {
        if (this.parent) this.parent.removeChild(this);
        (this._hd2dHomeParent || ss._tilemap).addChild(this);
        this._hd2dIsForeground = false;
        return;
    }
    if (!fg) return;
    const zoom = Camera.zoom();
    const cx = Graphics.width / (2 * zoom);
    const cy = Graphics.height / (2 * zoom);
    const f = fg.parallax !== null ? fg.parallax : tags.parallax !== null ? tags.parallax : State.effectOn("parallax") ? Depth.parallaxFactor(this._hd2d.depth, st.parallax) : 1;
    this.x += (this.x - cx) * (f - 1);
    this.y += (this.y - cy) * (f - 1);
    if (fg.fade) {
        // Fade out while it covers the player.
        const player = ss._characterSprites[ss._characterSprites.length - 1];
        let target = 1;
        if (player && player.visible) {
            const a = this.getBounds();
            const b = player.getBounds();
            if (a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y) target = 0.45;
        }
        this._hd2dFgAlpha = U.lerp(this._hd2dFgAlpha === undefined ? 1 : this._hd2dFgAlpha, target, 0.15);
        this.alpha *= this._hd2dFgAlpha;
    }
};

//-----------------------------------------------------------------------------
// Animations are drawn unlit (so darkness does not dim magic) and bloom.
//-----------------------------------------------------------------------------

const _Spriteset_Base_createAnimationSprite = Spriteset_Base.prototype.createAnimationSprite;
Spriteset_Base.prototype.createAnimationSprite = function(targets, animation, mirror, delay) {
    _Spriteset_Base_createAnimationSprite.apply(this, arguments);
    if (!(this instanceof Spriteset_Map) || !this._hd2dPipeline || !this._hd2dUnlit || !P.unlitAnimations) return;
    const sprite = this._animationSprites[this._animationSprites.length - 1];
    if (!sprite || sprite.parent !== this._effectsContainer) return;
    if (sprite instanceof Sprite_AnimationMV && animation.position === 3) return;
    this._effectsContainer.removeChild(sprite);
    this._hd2dUnlit.addChild(sprite);
};

const _Spriteset_Base_removeAnimation = Spriteset_Base.prototype.removeAnimation;
Spriteset_Base.prototype.removeAnimation = function(sprite) {
    if (sprite && sprite.parent && sprite.parent !== this._effectsContainer) sprite.parent.removeChild(sprite);
    _Spriteset_Base_removeAnimation.call(this, sprite);
};

//-----------------------------------------------------------------------------
// Weather: zoom-aware spawning; sprites hidden when drawn as depth particles.
//-----------------------------------------------------------------------------

const _Weather_updateAllSprites = Weather.prototype._updateAllSprites;
Weather.prototype._updateAllSprites = function() {
    if (this._hd2dHideSprites) {
        while (this._sprites.length > 0) this._removeSprite();
        return;
    }
    _Weather_updateAllSprites.call(this);
};

const _Weather_rebornSprite = Weather.prototype._rebornSprite;
Weather.prototype._rebornSprite = function(sprite) {
    _Weather_rebornSprite.call(this, sprite);
    const zoom = HD2D.mapSpriteset() ? Camera.zoom() : 1;
    if (zoom < 1) {
        sprite.ax = Math.randomInt(Math.ceil(Graphics.width / zoom) + 100) - 100 + this.origin.x;
        sprite.ay = Math.randomInt(Math.ceil(Graphics.height / zoom) + 200) - 200 + this.origin.y;
    }
};

//=============================================================================
// 24. Battle integration (grading, bloom, vignette, blurred battlebacks)
//=============================================================================

const _Spriteset_Battle_initialize = Spriteset_Battle.prototype.initialize;
Spriteset_Battle.prototype.initialize = function() {
    _Spriteset_Battle_initialize.apply(this, arguments);
    try {
        this.createHD2D();
    } catch (e) {
        console.error("[HD2D] Battle setup failed; HD2D disabled in battle.", e);
        this._hd2dPipeline = null;
    }
};

Spriteset_Battle.prototype.createHD2D = function() {
    this._hd2dPipeline = null;
    if (!P.battleEffects || GPU.failed || !Graphics.app || !this._baseSprite) return;
    if (!GPU.init(U.renderer())) return;
    const base = this._baseSprite;
    // Battlebacks get a depth-of-field style blur.
    this._hd2dBattleBack = new Sprite();
    const index = base.children.indexOf(this._back1Sprite);
    if (index >= 0) {
        base.addChildAt(this._hd2dBattleBack, index);
        for (const s of [this._back1Sprite, this._back2Sprite]) {
            base.removeChild(s);
            this._hd2dBattleBack.addChild(s);
        }
        this._hd2dBattleBlur = new PIXI.filters.BlurFilter(0, 3);
    }
    this._hd2dPost = new Sprite();
    const i = Math.max(0, this.children.indexOf(base));
    this.removeChild(base);
    this._hd2dPost.addChild(base);
    this.addChildAt(this._hd2dPost, i);
    this._hd2dPost.filterArea = new PIXI.Rectangle(0, 0, Graphics.width, Graphics.height);
    this._hd2dPipeline = new Pipeline(this, "battle");
    if (P.battlePreset && Presets.has(P.battlePreset)) State.battleOverride = Presets.get(P.battlePreset);
};

const _Spriteset_Battle_update = Spriteset_Battle.prototype.update;
Spriteset_Battle.prototype.update = function() {
    if (this._hd2dPipeline) State.update();
    _Spriteset_Battle_update.call(this);
    if (!this._hd2dPipeline) return;
    const st = HD2D.state();
    if (this._hd2dBattleBlur) {
        const on = State.effectOn("dof") && st.dof.weight > 0;
        const px = on ? st.dof.radius * st.dof.farBlur * st.dof.strength * st.dof.weight * P.battleBlur : 0;
        this._hd2dBattleBlur.blur = px;
        this._hd2dBattleBack.filters = px > 0.05 ? [this._hd2dBattleBlur] : null;
    }
    const flags = this._hd2dPipeline.computeFlags();
    this._hd2dPost.filters = flags.any && !this._hd2dPipeline.failed ? [this._hd2dPipeline.filter] : null;
};

const _Spriteset_Battle_destroy = Spriteset_Battle.prototype.destroy;
Spriteset_Battle.prototype.destroy = function(options) {
    State.battleOverride = null;
    _Spriteset_Battle_destroy.call(this, options);
};


//=============================================================================
// 25. Debug overlay and depth views
//=============================================================================

const Debug = (HD2D.Debug = {
    overlay: false,
    view: 0,
    VIEWS: ["Off", "Depth (red near / green focal / blue far)", "Blur amount", "Lighting", "Objects / emissive / rim", "Bloom"],
    el: null,
    spriteset: null,
    gfx: null,
    _tick: 0,

    enabled() {
        const m = P.debugMode;
        if (m === "off") return false;
        if (m === "always") return true;
        return U.isPlaytest();
    },

    keyCode(name) {
        const m = /^F(\d+)$/i.exec(String(name || ""));
        return m ? 111 + Number(m[1]) : -1;
    },

    onKeyDown(event) {
        if (!this.enabled() || event.ctrlKey || event.altKey) return;
        if (event.keyCode === this.keyCode(P.debugOverlayKey)) {
            this.overlay = !this.overlay;
            event.preventDefault();
            if (!this.overlay && this.el) this.el.style.display = "none";
        } else if (event.keyCode === this.keyCode(P.debugViewKey)) {
            this.view = (this.view + 1) % this.VIEWS.length;
            event.preventDefault();
        }
    },

    attach(spriteset) {
        this.spriteset = spriteset;
        this.gfx = new PIXI.Graphics();
        spriteset.addChild(this.gfx);
    },

    detach(spriteset) {
        if (this.spriteset === spriteset) {
            this.spriteset = null;
            this.gfx = null;
        }
        if (this.el) this.el.style.display = "none";
    },

    ensureElement() {
        if (this.el) return this.el;
        const el = document.createElement("div");
        el.id = "hd2dDebug";
        Object.assign(el.style, {
            position: "absolute", left: "4px", top: "4px", zIndex: 20, padding: "6px 8px", whiteSpace: "pre",
            font: "11px/1.35 monospace", color: "#f4f4f4", background: "rgba(10,12,20,0.72)", borderRadius: "4px",
            pointerEvents: "none", display: "none"
        });
        document.body.appendChild(el);
        this.el = el;
        return el;
    },

    update(spriteset) {
        const g = this.gfx;
        if (g) g.clear();
        if (!this.overlay || !this.enabled()) return;
        const el = this.ensureElement();
        el.style.display = "block";
        // Light gizmos.
        if (g && spriteset._hd2dCamera) {
            const wt = spriteset._hd2dCamera.worldTransform;
            const s = Math.hypot(wt.a, wt.b) || 1;
            for (const L of Lights.list) {
                const x = wt.a * L.x + wt.c * L.y + wt.tx;
                const y = wt.b * L.x + wt.d * L.y + wt.ty;
                g.lineStyle(1, U.colorInt(L.color), 0.8);
                g.drawCircle(x, y, L.radius * s);
                g.beginFill(U.colorInt(L.color), 1);
                g.drawCircle(x, y, 3);
                g.endFill();
            }
        }
        if (this._tick++ % 10 !== 0) return;
        el.textContent = this.text(spriteset);
    },

    text(spriteset) {
        const st = HD2D.state();
        const d = State.data();
        const q = State.quality();
        const pipe = spriteset._hd2dPipeline;
        const f = pipe ? pipe.flags : {};
        const fps = Graphics._fpsCounter ? Graphics._fpsCounter.fps : 0;
        const ms = Graphics._fpsCounter ? Graphics._fpsCounter.duration : 0;
        const player = spriteset._characterSprites ? spriteset._characterSprites[spriteset._characterSprites.length - 1] : null;
        const pd = player && player._hd2d ? player._hd2d.depth : 50;
        const focus = pipe ? pipe.dofParams(st).focus : st.dof.focus;
        const coc = Depth.coc(pd, Object.assign({}, st.dof, { focus }));
        const rt = GPU.stats();
        const on = [];
        const off = [];
        const add = (name, v) => (v ? on : off).push(name);
        add("depth", f.depth);
        add("dof", f.dof);
        add("bokeh", f.bokeh);
        add("ambient", f.ambient);
        add("sun", f.sun);
        add("lights", f.lights);
        add("shadows", f.shadows);
        add("normals", f.normals);
        add("fog", f.fog);
        add("atmosphere", f.atmo);
        add("rim", f.rim);
        add("bloom", f.bloom);
        add("grade", f.grade);
        add("vignette", f.vignette);
        add("particles", State.effectOn("particles"));
        add("camera", Camera.enabled());
        const trans = d.trans ? " (transition " + Math.round((d.trans.t / d.trans.dur) * 100) + "%)" : "";
        const hour = TimeOfDay.hour();
        const time = hour === null ? "off" : (st._phase || "") + " " + Math.floor(hour) + ":" + String(Math.floor((hour % 1) * 60)).padStart(2, "0");
        const particles = spriteset._hd2dParticleSystem ? spriteset._hd2dParticleSystem.count() : 0;
        return [
            "HD2D " + HD2D.VERSION + "  quality " + q.name + (GPU.hdr ? " (HDR)" : " (LDR)") + (pipe && pipe.failed ? "  [FAILED]" : ""),
            "FPS " + fps.toFixed(1) + "   frame " + ms.toFixed(1) + " ms   passes " + (pipe ? pipe.passes : 0),
            "preset " + d.preset + trans + "   time " + time,
            "focus " + focus.toFixed(1) + "   focal plane " + st.depth.focalDepth.toFixed(1) + " @ Y " + Depth.focalY.toFixed(2),
            "player depth " + pd.toFixed(1) + "   blur at player " + coc.toFixed(2),
            "camera zoom " + Camera.zoom().toFixed(2) + "   rotation " + Camera.rotation().toFixed(1) + "°",
            "lights " + Lights.list.length + " / " + q.maxLights + "   particles " + particles,
            "on:  " + on.join(" "),
            "off: " + off.join(" "),
            "render textures " + rt.count + " (" + rt.mb.toFixed(1) + " MB)",
            "view: " + this.VIEWS[this.view] + "  [" + P.debugViewKey + "]   overlay [" + P.debugOverlayKey + "]"
        ].join("\n");
    }
});
document.addEventListener("keydown", e => Debug.onKeyDown(e));

//=============================================================================
// 26. Pixel-perfect mode
//=============================================================================

if (P.pixelPerfect) {
    if (P.roundPixels) PIXI.settings.ROUND_PIXELS = true;
    const PIXEL_FOLDERS = [
        "img/characters/", "img/parallaxes/", "img/tilesets/", "img/sv_actors/", "img/sv_enemies/",
        "img/enemies/", "img/battlebacks1/", "img/battlebacks2/", "img/animations/"
    ];
    const _ImageManager_loadBitmap = ImageManager.loadBitmap;
    ImageManager.loadBitmap = function(folder, filename) {
        const bitmap = _ImageManager_loadBitmap.apply(this, arguments);
        if (bitmap && filename && PIXEL_FOLDERS.includes(folder)) bitmap.smooth = false;
        return bitmap;
    };
}

//=============================================================================
// 27. Game object hooks
//=============================================================================

HD2D.state = () => State.battleOverride || State.current();
State.battleOverride = null;

const _Game_Map_setup = Game_Map.prototype.setup;
Game_Map.prototype.setup = function(mapId) {
    _Game_Map_setup.call(this, mapId);
    State.onMapSetup(mapId);
    Camera.onTransfer();
};

const _Game_Map_screenTileX = Game_Map.prototype.screenTileX;
Game_Map.prototype.screenTileX = function() {
    return _Game_Map_screenTileX.call(this) / Camera.zoom();
};

const _Game_Map_screenTileY = Game_Map.prototype.screenTileY;
Game_Map.prototype.screenTileY = function() {
    return _Game_Map_screenTileY.call(this) / Camera.zoom();
};

/** Converts a canvas point to tilemap-local pixels through the camera transform. */
const canvasToLocal = (x, y) => {
    const ss = HD2D.mapSpriteset();
    if (!ss || !ss._tilemap || (Camera.zoom() === 1 && Camera.rotation() === 0)) return null;
    return ss._tilemap.worldTransform.applyInverse(new PIXI.Point(x, y));
};

const _Game_Map_canvasToMapX = Game_Map.prototype.canvasToMapX;
Game_Map.prototype.canvasToMapX = function(x) {
    const local = canvasToLocal(x, x === TouchInput.x ? TouchInput.y : Graphics.height / 2);
    if (!local) return _Game_Map_canvasToMapX.call(this, x);
    const tw = this.tileWidth();
    return this.roundX(Math.floor((this._displayX * tw + local.x) / tw));
};

const _Game_Map_canvasToMapY = Game_Map.prototype.canvasToMapY;
Game_Map.prototype.canvasToMapY = function(y) {
    const local = canvasToLocal(y === TouchInput.y ? TouchInput.x : Graphics.width / 2, y);
    if (!local) return _Game_Map_canvasToMapY.call(this, y);
    const th = this.tileHeight();
    return this.roundY(Math.floor((this._displayY * th + local.y) / th));
};

const _Game_CharacterBase_isNearTheScreen = Game_CharacterBase.prototype.isNearTheScreen;
Game_CharacterBase.prototype.isNearTheScreen = function() {
    const zoom = Camera.zoom();
    if (zoom >= 1) return _Game_CharacterBase_isNearTheScreen.call(this);
    const gw = Graphics.width / zoom;
    const gh = Graphics.height / zoom;
    const tw = $gameMap.tileWidth();
    const th = $gameMap.tileHeight();
    const px = this.scrolledX() * tw + tw / 2 - gw / 2;
    const py = this.scrolledY() * th + th / 2 - gh / 2;
    return px >= -gw && px <= gw && py >= -gh && py <= gh;
};

const _Game_Player_updateScroll = Game_Player.prototype.updateScroll;
Game_Player.prototype.updateScroll = function(lastScrolledX, lastScrolledY) {
    if (Camera.isActive()) return; // the HD2D camera scrolls the map
    _Game_Player_updateScroll.call(this, lastScrolledX, lastScrolledY);
};

const _Game_Player_center = Game_Player.prototype.center;
Game_Player.prototype.center = function(x, y) {
    Camera.snap();
    return _Game_Player_center.call(this, x, y);
};

const _Scene_Map_updateMain = Scene_Map.prototype.updateMain;
Scene_Map.prototype.updateMain = function() {
    _Scene_Map_updateMain.call(this);
    Camera.update();
};

const _Scene_Map_onMapLoaded = Scene_Map.prototype.onMapLoaded;
Scene_Map.prototype.onMapLoaded = function() {
    // Re-read map tags after loading a save or returning from a menu.
    if (!this._transfer && $gameMap && $dataMap) MapTags.parse($dataMap, $gameMap.mapId());
    _Scene_Map_onMapLoaded.call(this);
};

const _Game_Event_setupPage = Game_Event.prototype.setupPage;
Game_Event.prototype.setupPage = function() {
    _Game_Event_setupPage.call(this);
    this._hd2dTags = null; // page changed: re-read comment tags
};

const resetRuntime = () => {
    State._current = null;
    State.invalidate();
    Camera.snap();
    Camera._lastDX = null;
    Camera._resetCont = true;
    Depth.autoFocusDepth = null;
};

const _DataManager_setupNewGame = DataManager.setupNewGame;
DataManager.setupNewGame = function() {
    _DataManager_setupNewGame.call(this);
    resetRuntime();
};

const _DataManager_extractSaveContents = DataManager.extractSaveContents;
DataManager.extractSaveContents = function(contents) {
    _DataManager_extractSaveContents.call(this, contents);
    resetRuntime();
};

//=============================================================================
// 28. Script API (usable from Script event commands)
//=============================================================================

/** HD2D.set("bloom.intensity", 0.6, 60, "smooth") */
HD2D.set = (path, value, duration = 0, easing = "smooth") => {
    const p = State._normPath(path);
    const v = typeof value === "string" ? HD2D.convertValue(p, value) : value;
    State.setValue(p, v === null ? value : v, duration, easing);
};
HD2D.get = path => U.getPath(HD2D.state(), State._normPath(path));
HD2D.reset = (path = "all", duration = 0, easing = "smooth") => State.resetValue(path, duration, easing);
HD2D.setPreset = (name, duration = 0, easing = "smooth") => State.setPreset(name, duration, easing);
HD2D.setEffect = (name, on) => {
    const key = HD2D.effectKey(name) || name;
    if (String(name).toLowerCase() === "all") EFFECT_KEYS.forEach(k => State.setEffect(k, on));
    else State.setEffect(key, on);
};
HD2D.setQuality = level => {
    const key = String(level || "").toLowerCase();
    State.data().quality = QUALITY[key] ? key : null;
};
HD2D.setTime = (hour, duration = 0, easing = "smooth") => {
    const d = State.data();
    const from = U.isNum(d.time.hour) ? d.time.hour : 12;
    let to = hour;
    let delta = to - from;
    if (delta < -12) to += 24;
    if (delta > 12) to -= 24;
    if (duration > 0) d.timeTween = { from, to, t: 0, dur: duration, ease: easing };
    else {
        d.time.hour = ((hour % 24) + 24) % 24;
        d.timeTween = null;
    }
    State.invalidate();
};
HD2D.addLight = config => Lights.create(config);
HD2D.removeLight = (id, duration = 0) => Lights.remove(String(id), duration);
HD2D.registerSprite = (sprite, options = {}) => {
    sprite._hd2dDepth = U.isNum(options.depth) ? options.depth : 50;
    sprite._hd2dEmissive = options.emissive || 0;
    return sprite;
};

//=============================================================================
// 29. Plugin commands
//=============================================================================

const A = {
    num: (v, def) => U.num(v, def),
    opt: v => (v === undefined || v === null || String(v).trim() === "" ? null : U.num(v, null)),
    bool: (v, def) => U.bool(v, def),
    str: (v, def = "") => U.str(v, def).trim(),
    color: (v, def) => U.color(v, def),
    dur: v => Math.max(0, Math.round(U.num(v, 0))),
    ease: v => U.str(v, "Smooth") || "Smooth"
};

/** Applies optional (non-blank) values with a tween. */
const setOptional = (pairs, duration, easing) => {
    for (const [path, raw, kind] of pairs) {
        if (raw === undefined || raw === null || String(raw).trim() === "") continue;
        let v;
        if (kind === "color") v = U.color(raw, null);
        else if (kind === "bool") v = U.bool(raw, null);
        else if (kind === "str") v = String(raw).trim();
        else v = U.num(raw, null);
        if (v === null) continue;
        State.setValue(path, v, duration, easing);
    }
};

const command = (name, fn) => PluginManager.registerCommand(PLUGIN_NAME, name, function(args) {
    try {
        fn.call(this, args || {});
    } catch (e) {
        console.error("[HD2D] Plugin command '" + name + "' failed:", e);
    }
});

/** Resolves a command target to a character (for depth / emissive / camera). */
const commandCharacter = (interp, target, id) => {
    const t = A.str(target, "Player").toLowerCase();
    if (t === "this event") return $gameMap.event(interp.eventId());
    return HD2D.findCharacter(t, A.num(id, 0), interp);
};

command("SetPreset", function(a) {
    const name = A.str(a.preset, P.defaultPreset);
    State.setPreset(name, A.dur(a.duration), A.ease(a.easing), A.bool(a.keepOverrides, false));
    if (A.bool(a.remember, false) && $gameMap) State.data().mapPresets[$gameMap.mapId()] = Presets.canonicalName(name);
});

command("SetTimeOfDay", function(a) {
    const raw = A.str(a.time, "Day");
    let hour = U.num(raw, null);
    if (hour === null) {
        const phase = TimeOfDay.phases.find(p => p.name.toLowerCase() === raw.toLowerCase());
        hour = phase ? phase.hour : 12;
    }
    HD2D.setTime(hour, A.dur(a.duration), A.ease(a.easing));
});

command("SetDepth", function(a) {
    const target = A.str(a.target, "This Event").toLowerCase();
    const depth = U.clamp(A.num(a.depth, 50), 0, 100);
    const d = State.data();
    if (target === "picture") {
        const id = A.num(a.pictureId, 1);
        d.pictures[id] = Object.assign(d.pictures[id] || {}, { depth });
        return;
    }
    const ch = commandCharacter(this, target, a.eventId);
    if (!ch) return;
    const key = characterKey(ch);
    d.depth[key] = Object.assign(d.depth[key] || {}, { depth });
});

command("ResetDepth", function(a) {
    const target = A.str(a.target, "This Event").toLowerCase();
    const d = State.data();
    if (target === "picture") {
        const entry = d.pictures[A.num(a.pictureId, 1)];
        if (entry) delete entry.depth;
        return;
    }
    if (target === "all") {
        d.depth = {};
        d.pictures = {};
        return;
    }
    const ch = commandCharacter(this, target, a.eventId);
    if (ch && d.depth[characterKey(ch)]) delete d.depth[characterKey(ch)].depth;
});

command("SetEmissive", function(a) {
    const target = A.str(a.target, "This Event").toLowerCase();
    const strength = U.clamp(A.num(a.strength, 1), 0, 4);
    const d = State.data();
    if (target === "picture") {
        const id = A.num(a.pictureId, 1);
        d.pictures[id] = Object.assign(d.pictures[id] || {}, { emissive: strength });
        return;
    }
    const ch = commandCharacter(this, target, a.eventId);
    if (!ch) return;
    const key = characterKey(ch);
    d.depth[key] = Object.assign(d.depth[key] || {}, { emissive: strength });
});

command("SetFocusDepth", function(a) {
    State.data().autoFocus = null;
    State.setValue("dof.focus", U.clamp(A.num(a.depth, 50), 0, 100), A.dur(a.duration), A.ease(a.easing));
});

command("FocusOnTarget", function(a) {
    const d = State.data();
    if (!A.bool(a.enabled, true)) {
        d.autoFocus = null;
        return;
    }
    let target = A.str(a.target, "Player").toLowerCase();
    let eventId = A.num(a.eventId, 0);
    if (target === "this event") {
        target = "event";
        eventId = this.eventId();
    }
    d.autoFocus = { target, eventId, speed: U.clamp(A.num(a.speed, 0.1), 0.01, 1) };
});

command("SetDepthOfField", function(a) {
    const dur = A.dur(a.duration);
    const ease = A.ease(a.easing);
    setOptional([
        ["dof.enabled", a.enabled, "bool"], ["dof.focusRange", a.focusRange], ["dof.nearBlur", a.nearBlur],
        ["dof.farBlur", a.farBlur], ["dof.strength", a.strength], ["dof.radius", a.radius],
        ["dof.nearTransition", a.nearTransition], ["dof.farTransition", a.farTransition]
    ], dur, ease);
});

command("SetBokeh", function(a) {
    const dur = A.dur(a.duration);
    setOptional([
        ["bokeh.enabled", a.enabled, "bool"], ["bokeh.intensity", a.intensity], ["bokeh.size", a.size],
        ["bokeh.threshold", a.threshold], ["bokeh.quality", a.quality, "str"], ["bokeh.maxCount", a.maxCount]
    ], dur, A.ease(a.easing));
});

command("SetAmbientLight", function(a) {
    setOptional([
        ["ambient.enabled", a.enabled, "bool"], ["ambient.color", a.color, "color"], ["ambient.intensity", a.intensity],
        ["ambient.temperature", a.temperature], ["ambient.shadowTint", a.shadowTint, "color"],
        ["ambient.highlightTint", a.highlightTint, "color"]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("SetDirectionalLight", function(a) {
    setOptional([
        ["sun.enabled", a.enabled, "bool"], ["sun.angle", a.angle], ["sun.elevation", a.elevation],
        ["sun.intensity", a.intensity], ["sun.color", a.color, "color"]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("CreateLight", function(a) {
    const attachRaw = A.str(a.attach, "This Event").toLowerCase();
    const config = {
        id: A.str(a.id, "light"),
        type: A.str(a.type, "Point").toLowerCase() === "spot" ? "spot" : "point",
        radius: A.num(a.radius, 144),
        color: A.color(a.color, [1, 0.85, 0.65]),
        intensity: A.num(a.intensity, 1),
        falloff: A.num(a.falloff, 2),
        softness: U.clamp(A.num(a.softness, 0.5), 0, 1),
        direction: A.num(a.direction, 90),
        facing: A.bool(a.facing, false),
        cone: A.num(a.cone, 50),
        flicker: U.clamp(A.num(a.flicker, 0), 0, 1),
        shadows: A.bool(a.shadows, true),
        glow: A.opt(a.glow),
        offsetX: A.num(a.offsetX, 0),
        offsetY: A.num(a.offsetY, 0),
        x: A.num(a.x, 0),
        y: A.num(a.y, 0),
        depth: A.opt(a.depth),
        scope: A.str(a.scope, "This Map").toLowerCase() === "all maps" ? "global" : "map",
        fadeDuration: A.dur(a.fadeDuration)
    };
    if (attachRaw === "map position") config.attach = "map";
    else if (attachRaw === "screen position") config.attach = "screen";
    else if (attachRaw === "player") config.attach = "player";
    else if (attachRaw === "follower") {
        config.attach = "follower";
        config.eventId = A.num(a.eventId, 1);
    } else {
        config.attach = "event";
        config.eventId = attachRaw === "this event" ? this.eventId() : A.num(a.eventId, 0);
    }
    Lights.create(config);
});

command("RemoveLight", function(a) {
    const id = A.str(a.id, "");
    if (id.toLowerCase() === "all") {
        for (const key of Object.keys(State.data().lights)) Lights.remove(key, A.dur(a.fadeDuration));
    } else {
        Lights.remove(id, A.dur(a.fadeDuration));
    }
});

command("EnableEffect", function(a) {
    HD2D.setEffect(A.str(a.effect, "all"), true);
});

command("DisableEffect", function(a) {
    HD2D.setEffect(A.str(a.effect, "all"), false);
});

command("SetBloom", function(a) {
    setOptional([
        ["bloom.enabled", a.enabled, "bool"], ["bloom.threshold", a.threshold], ["bloom.intensity", a.intensity],
        ["bloom.radius", a.radius], ["bloom.emissive", a.emissiveBoost]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("SetVignette", function(a) {
    setOptional([
        ["vignette.enabled", a.enabled, "bool"], ["vignette.intensity", a.intensity], ["vignette.radius", a.radius],
        ["vignette.softness", a.softness], ["vignette.color", a.color, "color"], ["vignette.pulse", a.pulse]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("SetFog", function(a) {
    const layer = A.str(a.layer, "Far").toLowerCase();
    const layers = layer === "all" ? ["near", "mid", "far"] : [layer];
    const dur = A.dur(a.duration);
    const ease = A.ease(a.easing);
    setOptional([["fog.enabled", a.enabled, "bool"], ["fog.color", a.color, "color"], ["fog.noise", a.noise]], dur, ease);
    for (const l of layers) {
        if (!["near", "mid", "far"].includes(l)) continue;
        setOptional([
            ["fog." + l + "Opacity", a.opacity], ["fog." + l + "Depth", a.depth], ["fog." + l + "Scale", a.scale],
            ["fog." + l + "SpeedX", a.speedX], ["fog." + l + "SpeedY", a.speedY]
        ], dur, ease);
    }
});

command("SetColorGrade", function(a) {
    const dur = A.dur(a.duration);
    const ease = A.ease(a.easing);
    const preset = A.str(a.preset, "");
    if (preset && preset.toLowerCase() !== "(custom)") {
        const g = HD2D.gradePreset(preset);
        if (g) {
            const values = Object.assign({}, g);
            delete values.weight;
            delete values.enabled;
            State.setValues({ grade: values }, dur, ease);
            State.setValue("grade.enabled", true, dur, ease);
        } else {
            U.warnOnce("Unknown color grade '" + preset + "'");
        }
    }
    setOptional([
        ["grade.exposure", a.exposure], ["grade.contrast", a.contrast], ["grade.saturation", a.saturation],
        ["grade.brightness", a.brightness], ["grade.gamma", a.gamma], ["grade.hue", a.hue],
        ["grade.temperature", a.temperature], ["grade.tint", a.tint], ["grade.lut", a.lut, "str"],
        ["grade.lutStrength", a.lutStrength]
    ], dur, ease);
});

command("SetShadows", function(a) {
    setOptional([
        ["shadows.enabled", a.enabled, "bool"], ["shadows.opacity", a.opacity], ["shadows.length", a.length],
        ["shadows.softness", a.softness], ["shadows.contact", a.contact], ["shadows.occlusion", a.occlusion]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("SetRimLight", function(a) {
    setOptional([
        ["rim.enabled", a.enabled, "bool"], ["rim.color", a.color, "color"], ["rim.intensity", a.intensity],
        ["rim.width", a.width], ["rim.angle", a.angle], ["rim.followSun", a.followSun, "bool"]
    ], A.dur(a.duration), A.ease(a.easing));
});

command("SetVisualValue", function(a) {
    HD2D.set(A.str(a.path, ""), A.str(a.value, ""), A.dur(a.duration), A.ease(a.easing));
});

command("ResetVisualValues", function(a) {
    State.resetValue(A.str(a.path, "") || "all", A.dur(a.duration), A.ease(a.easing));
});

command("SetCameraZoom", function(a) {
    const dur = A.dur(a.duration);
    Camera.setZoom(A.num(a.zoom, 1), dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("SetCameraFocus", function(a) {
    const target = A.str(a.target, "Player").toLowerCase();
    const dur = A.dur(a.duration);
    let follow;
    if (target === "player") follow = { type: "player" };
    else if (target === "this event") follow = { type: "event", id: this.eventId() };
    else if (target === "event") follow = { type: "event", id: A.num(a.eventId, 0) };
    else if (target === "map position") follow = { type: "point", x: A.num(a.x, 0), y: A.num(a.y, 0) };
    else follow = { type: "none" };
    Camera.focus(follow, dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("CameraOffset", function(a) {
    const dur = A.dur(a.duration);
    Camera.setOffset(A.num(a.x, 0), A.num(a.y, 0), dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("CameraShake", function(a) {
    const dur = Math.max(1, A.dur(a.duration));
    Camera.shake(A.num(a.power, 6), A.num(a.speed, 6), dur, A.str(a.direction, "Both"));
    if (A.bool(a.wait, false)) this.wait(dur);
});

command("CameraRotation", function(a) {
    const dur = A.dur(a.duration);
    Camera.setRotation(A.num(a.angle, 0), dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("SmoothCamera", function(a) {
    const v = A.str(a.mode, "Default").toLowerCase();
    Camera.data().smooth = v === "on" ? true : v === "off" ? false : null;
});

command("SetLetterbox", function(a) {
    const dur = A.dur(a.duration);
    Camera.setLetterbox(U.clamp(A.num(a.size, 10), 0, 45) / 100, dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("ScreenFade", function(a) {
    const dur = A.dur(a.duration);
    Camera.fade(A.color(a.color, [0, 0, 0]), U.clamp(A.num(a.opacity, 255), 0, 255) / 255, dur, A.ease(a.easing));
    if (A.bool(a.wait, false) && dur > 0) this.wait(dur);
});

command("SetParallax", function(a) {
    const id = A.str(a.id, "layer");
    const loop = A.str(a.loop, "Horizontal").toLowerCase();
    const layer = {
        id,
        image: A.str(a.image, ""),
        folder: A.str(a.folder, "parallaxes").replace(/^img\//, "").replace(/\/$/, "") || "parallaxes",
        depth: U.clamp(A.num(a.depth, 85), 0, 100),
        loopX: loop === "horizontal" || loop === "both",
        loopY: loop === "vertical" || loop === "both",
        x: A.num(a.x, 0),
        y: A.num(a.y, 0),
        scrollX: A.num(a.scrollX, 0),
        scrollY: A.num(a.scrollY, 0),
        factorX: A.opt(a.factorX),
        factorY: A.opt(a.factorY),
        opacity: U.clamp(A.num(a.opacity, 255), 0, 255),
        blend: Layers.blendMode(a.blend),
        scale: A.num(a.scale, 1),
        zoomInfluence: null,
        front: null,
        visible: true,
        scope: A.str(a.scope, "This Map").toLowerCase() === "all maps" ? "global" : "map",
        mapId: $gameMap ? $gameMap.mapId() : 0
    };
    if (!layer.image) return;
    State.data().layers[id] = layer;
});

command("RemoveParallax", function(a) {
    const id = A.str(a.id, "");
    const d = State.data();
    if (id.toLowerCase() === "all") {
        d.layers = {};
        for (const L of MapTags.layers) d.layers[L.id] = { id: L.id, removed: true, scope: "map", mapId: $gameMap.mapId() };
        return;
    }
    if (MapTags.layers.some(L => L.id === id)) d.layers[id] = { id, removed: true, scope: "map", mapId: $gameMap.mapId() };
    else delete d.layers[id];
});

command("SetParticles", function(a) {
    const id = A.str(a.id, "particles");
    const type = A.str(a.type, "Dust").toLowerCase();
    if (!PARTICLE_TYPES[type]) return;
    const e = { id, type, amount: A.num(a.amount, 30) };
    const dmin = A.opt(a.depthMin);
    const dmax = A.opt(a.depthMax);
    if (dmin !== null) e.depthMin = dmin;
    if (dmax !== null) e.depthMax = dmax;
    const color = A.color(a.color, null);
    if (color) e.color = color;
    const attach = A.str(a.attach, "Screen").toLowerCase();
    if (attach !== "screen") {
        e.area = "event";
        e.eventId = attach === "this event" ? this.eventId() : A.num(a.eventId, 0);
        e.radius = A.num(a.radius, 20);
    }
    e.scope = A.str(a.scope, "This Map").toLowerCase() === "all maps" ? "global" : "map";
    e.mapId = $gameMap ? $gameMap.mapId() : 0;
    State.data().emitters[id] = e;
});

command("RemoveParticles", function(a) {
    const id = A.str(a.id, "");
    if (id.toLowerCase() === "all") State.data().emitters = {};
    else delete State.data().emitters[id];
});

command("SetQuality", function(a) {
    HD2D.setQuality(A.str(a.quality, "Default"));
});

command("DebugView", function(a) {
    Debug.overlay = A.bool(a.overlay, Debug.overlay);
    const view = A.str(a.view, "");
    const index = ["off", "depth", "blur", "lighting", "objects", "bloom"].indexOf(view.toLowerCase());
    if (index >= 0) Debug.view = index;
});

})();
