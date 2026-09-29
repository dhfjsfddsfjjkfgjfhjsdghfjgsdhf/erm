//=============================================================================
// Plugin Name: QuestLog
// Author: Winthorp Darkrites (Winter Dream Games Creator)
// Description: Create a questlog to manage your quests
// Use: Feel free to use for private and commercial projects. Feel free to edit. Please give credits.
//=============================================================================

/*:
 * @target MZ
 * @plugindesc Custom Quest Plugin for RPG Maker MZ
 * @author Winthorp Darkrites
 * @url https://ko-fi.com/winterdream
 *
 * @param linebreak1
 * @text ===Main options===
 * @desc The main window options
 * @default ================
 *
 * @param fontsize
 * @parent linebreak1
 * @text Title Font Size
 * @type number
 * @desc The size of the font for the Scene Title
 * @default 40
 * @min 1
 *
 * @param textManagement
 * @parent linebreak1
 * @text Description text management
 * @type select
 * @desc Choose how to manage text
 * @option Manual Text
 * @value manual
 * @option Auto Sizer (change font size but doesn't break lines)
 * @value size
 * @option Auto Wrap (fit both by breaking lines and resizing font)
 * @value wrap
 * @default wrap
 *
 * @param paddingValue
 * @parent linebreak1
 * @text Auto Text Padding
 * @type number
 * @desc The padding from the left/right border for Auto Size and Auto Wrap
 * @default 50
 *
 * @param descriptionSize
 * @parent linebreak1
 * @text Quest Description Font Size
 * @type number
 * @desc The size of the font for the description of the Quest (If not Dynamic)
 * @default 20
 * @min 1
 *
 * @param infoalign
 * @parent linebreak1
 * @text Quest Info Alignment
 * @desc Select how to align the informations in the quest description
 * @type select
 * @option Left
 * @value left
 * @option Center
 * @value center
 * @option Right
 * @value right
 * @default center
 *
 * @param listSize
 * @parent linebreak1
 * @text Font Size in the list
 * @type number
 * @desc The size of the font of the Quest's name in the quests list
 * @default 20
 * @min 1
 *
 * @param listAlign
 * @parent linebreak1
 * @text Quest List Align
 * @desc Select how to align the quest in the QuestLog list
 * @type select
 * @option Left
 * @value left
 * @option Center
 * @value center
 * @option Right
 * @value right
 * @default center
 * 
 * @param linebreak6
 * @text ===Category Options===
 * @desc Organize your Quests
 * @default ================
 *
 * @param categoryFlag
 * @parent linebreak6
 * @type boolean
 * @text Use Categories?
 * @desc Decide if you want to organize in categories
 * @default false
 * @on Use them
 * @off Don't use them
 * 
 * @param categoryPriority
 * @parent linebreak6
 * @text Categories Priority
 * @desc Select how categories are organized
 * @type select
 * @option Category group all the ongoing-completed-failed quests
 * @value category
 * @option First show the ongoing quests by category, then completed, then failed
 * @value status
 * @default category
 * 
 * @param categoryDatabase
 * @parent linebreak6
 * @text Categories Database
 * @type struct<catData>
 * @desc The settings of the Categories
 * @default {"uncategorizedName":"--No Category--","uncategorizedNameTrans":"[]","uncategoryIndex":"999","categoriesDatabase":"[]"}
 * 
 * @param linebreak2
 * @text ===Text Options===
 * @desc Select your terms
 * @default ================
 *
 * @param Title
 * @parent linebreak2
 * @text Title
 * @desc Set the title of the QuestLog
 * @default QuestLog
 *
 * @param giverprefix
 * @parent linebreak2
 * @text Giver Prefix
 * @desc How the "From:" prefix is shown in the Quest Giver
 * @default From:
 *
 * @param areaprefix
 * @parent linebreak2
 * @text Area Prefix
 * @desc How the "Area:" prefix is shown in the Quest Area
 * @default Area:
 *
 * @param statusname
 * @parent linebreak2
 * @text Status Name
 * @desc How the "Status:" is shown for Quest Completion
 * @default Status:
 *
 * @param questcompleted
 * @parent linebreak2
 * @text Quest Completed
 * @desc Word to show if quest is completed
 * @default Completed
 *
 * @param questongoing
 * @parent linebreak2
 * @text Quest Ongoing
 * @desc Word to show if quest is ongoing
 * @default Ongoing
 *
 * @param questfailed
 * @parent linebreak2
 * @text Quest Failed
 * @desc Word to show if quest is failed
 * @default Failed
 * 
 * @param linebreakExtra
 * @text ===Extra Features===
 * @desc Set the preferences for extra features
 * @default ================
 * 
 * @param logsFlag
 * @parent linebreakExtra
 * @type boolean
 * @text Use Detailed Logs?
 * @desc Decide if you want to show the command to open quest's detailed logs
 * @default false
 * @on Use them
 * @off Don't use them
 * 
 * @param logsDefText
 * @parent logsFlag
 * @text Command Name for Logs
 * @desc The text of the command to open the detailed logs
 * @default Logs
 * 
 * @param trackSetting
 * @parent linebreakExtra
 * @type select
 * @text Use Quest HUD Tracking?
 * @desc Decide if you want to show the command to open quest's detailed logs
 * @default no
 * @option Don't use Tracking
 * @value no
 * @option Allow player to decide the quest to track
 * @value player
 * @option Use tracking set by the developer
 * @value dev
 *
 * @param trackConfiguration
 * @parent trackSetting
 * @text Quest HUD Tracking Options
 * @type struct<trackOpt>
 * @desc The settings of HUD tracking
 * @default {"maxQuest":"3","textColor":"#ffffff","maxFont":"16","hudSize":"{\"width\":\"20\",\"height\":\"20\",\"x\":\"0\",\"y\":\"0\"}"}
 * 
 * @param trackDefText
 * @parent trackSetting
 * @text Command Name for Quest Tracking (Track)
 * @desc The text of the command to start tracking a quest
 * @default Track Quest
 * 
 * @param untrackDefText
 * @parent trackSetting
 * @text Command Name for Quest Tracking (Remove Track)
 * @desc The text of the command to stop tracking a quest
 * @default Don't Track
 * 
 * @param linebreak3
 * @text ===Command Button===
 * @desc Set the preferences for the menu command
 * @default ================
 *
 * @param menucommand
 * @parent linebreak3
 * @type boolean
 * @text Menu Command
 * @desc Add the Quest command to the game menu
 * @default False
 * @on Show
 * @off Hide
 *
 * @param commandname
 * @parent linebreak3
 * @text Command Name
 * @desc Set the name of the command (if activated)
 * @default QuestLog
 * 
 * @param linebreak5
 * @text ===Translation Settings===
 * @desc Set the translation options
 * @default ================
 *
 * @param translationPacks
 * @parent linebreak5
 * @text Translation Packs (for Settings)
 * @type struct<settingsTransPack>[]
 * @desc The translation packs for the plugin settings (not the quests)
 * @default []
 * 
 * @param linebreak4
 * @text ===Graphic Settings===
 * @desc Set the graphic preferences
 * @default ================
 *
 * @param titleFlag
 * @parent linebreak4
 * @text Show QuestLog Title?
 * @type boolean
 * @desc Choose if you want to show the QuestLog title
 * @default true
 * @on Show
 * @off Hide
 *
 * @param layoutAlign
 * @parent linebreak4
 * @text QuestLog Layout
 * @desc Select the QuestLog Layout
 * @type select
 * @option Quest List on left, Info on right
 * @value layout1
 * @option Quest List on right, Info on left
 * @value layout2
 * @default layout1
 *
 * @param layoutSize
 * @parent linebreak4
 * @text Layout Size
 * @desc Select the QuestLog Layout size
 * @type select
 * @option 100% of the Graphic Box (classic)
 * @value size1
 * @option 90% of the Graphic Box (RMMZ style)
 * @value size2
 * @option 100% of the Screen (For projects with different UI and Screen sizes)
 * @value size3
 * @option 90% of the Screen (For projects with different UI and Screen sizes)
 * @value size4
 * @default size1
 *
 * @param touchCancel
 * @parent linebreak4
 * @text Show Touch Cancel Button?
 * @type boolean
 * @desc Choose if you want to show the touch cancel button (make sure the player has non touch commands if you don't)
 * @default true
 * @on Show
 * @off Hide
 *
 * @param skinSettings
 * @parent linebreak4
 * @text Custom Skin
 * @type struct<skinSet>
 * @desc If you want to use a custom skin use this settings
 * @default {"skinFlag":"false","skinName":"","redT":"0","greenT":"0","blueT":"0"}
 *
 * @param linebreak7
 * @text ===Management Settings===
 * @desc How the plugin works
 * @default ================
 * 
 * @param errorManagement
 * @parent linebreak7
 * @text Error Management
 * @desc How the plugin handles the errors
 * @type select
 * @option Throw an Error (will break the game, safer)
 * @value err1
 * @option Show a warning in the console (Must keep an eye at the console)
 * @value err2
 * @option Do nothing (really? why?)
 * @value err3
 * @default err1
 * 
 * @command line1
 * @text --- Quest Management ---
 * @desc Series of commands to manage your quests 
 *
 * @command newCreateQuest
 * @text Create Quest
 * @desc Create a new quest
 * @arg id
 * @type number
 * @text ID
 * @desc The ID of the quest. (Minimum 1)
 * @min 1
 *
 * @arg icon
 * @type icon
 * @text Icon
 * @desc The icon index to display for the quest
 * 
 * @arg cat
 * @type number
 * @text Quest Category ID
 * @desc If in use, select a category (0 for no category)
 * @min 0
 *
 * @arg short
 * @type string
 * @text Name (short)
 * @desc The name of the quest
 *
 * @arg long
 * @type string
 * @text Long Title
 * @desc A longer title for the description page, leave blank to use the Quest Name
 *
 * @arg index
 * @type number
 * @text Index
 * @desc The indexing number for the quest in the list
 *
 * @arg giver
 * @type string
 * @text Giver
 * @desc Information on the quest giver
 *
 * @arg area
 * @type string
 * @text Area
 * @desc Information on the location of the quest
 *
 * @arg desc
 * @type string
 * @text Description
 * @desc Information on the quest
 * 
 * @arg questTrans
 * @text Quest Translations
 * @desc Translations for the Quest
 * @default []
 * @type struct<questTxtTrans>[]
 *
 * @arg status
 * @text Status
 * @type select
 * @option Ongoing
 * @value ongoing
 * @option Completed
 * @value completed
 * @option Failed
 * @value failed
 * @desc Whether the quest is completed, ongoing or failed
 * @default ongoing
 * 
 * @arg logs
 * @text Detailed Logs (if active)
 * @type struct<detLogs>[]
 * @default []
 * @desc The detailed Logs for the quest
 * 
 * @arg track
 * @text Tracking Settings
 * @type struct<detTrack>
 * @default {"isTrackable":"true","text":"","textTrans":"[]"}
 * @desc The setting for tracking
 *
 * @command RemoveQuestNew
 * @text Remove Quest
 * @desc Removes quest searching by ID or Name.
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to remove (leave 0 if using Name).
 *
 * @arg questName
 * @text Quest Name
 * @desc Name of the quest to be removed (leave blank if using ID).
 * @type text
 *
 * @command SetCompletion
 * @text Set Quest Completion Parameter
 * @desc Sets if a quest is completed or not searching by ID or Name.
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to edit. (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to edit. (Must be exact name, leave blank if you use ID)
 * @default
 *
 * @arg status
 * @text Status
 * @type select
 * @option Ongoing
 * @value ongoing
 * @option Completed
 * @value completed
 * @option Failed
 * @value failed
 * @desc Whether the quest is completed, ongoing or failed.
 * @default ongoing
 *
 * @command editQuestDescriptors
 * @text Edit Quest Descriptors (name, description, icon, ...)
 * @desc Edit the Quest descriptors, leave them blank if no changes
 * 
 * @arg questID
 * @text Search by Quest ID
 * @type number
 * @default 0
 * @desc Search Quest by ID, leave 0 if you search by name
 * 
 * @arg questName
 * @text Search by Quest Name (not advised)
 * @default
 * @desc Search Quest by name (short title), it's advised to use Quest ID as it never changes. Leave blank if not used
 * 
 * @arg icon
 * @type icon
 * @text Icon
 * @desc The icon index to display for the quest, leave 0 if no changes
 * @default 0
 * 
 * @arg cat
 * @type number
 * @text Quest Category ID
 * @desc If in use, select a category (0 for no category), -1 for no changes
 * @min -1
 * @default -1
 *
 * @arg short
 * @type string
 * @text Name (short)
 * @desc The name of the quest (Blank for no changes)
 *
 * @arg long
 * @type string
 * @text Long Title
 * @desc A longer title for the description page, leave blank to use the Quest Name (Blank for no changes)
 *
 * @arg giver
 * @type string
 * @text Giver
 * @desc Information on the quest giver (Blank for no changes)
 *
 * @arg area
 * @type string
 * @text Area
 * @desc Information on the location of the quest (Blank for no changes)
 *
 * @arg desc
 * @type string
 * @text Description
 * @desc Information on the quest (Blank for no changes)
 * 
 * @arg questTrans
 * @text Quest Translations
 * @desc Translations for the Quest
 * @default []
 * @type struct<questTxtTrans>[]
 * 
 * @command hideShowQuest
 * @text Hide or Show Quest
 * @desc Hides or Shows a Quest
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to remove (leave 0 if using Name).
 *
 * @arg questName
 * @text Quest Name
 * @desc Name of the quest to be removed (leave blank if using ID).
 * @type text
 * 
 * @arg showFlag
 * @text Hide or Show?
 * @type select
 * @option Show
 * @value show
 * @option Hide
 * @value hide
 * @option Toggle
 * @value toggle
 * @desc Select if you want to hide, show or toggle between the two
 * @default show
 *
 * @command line2
 * @text --- Plugin Functionality ---
 * @desc Series of command to change words and fonts.
 *
 * @command newSetTitle
 * @text Set QuestLog Title
 * @desc Set the title of the QuestLog.
 *
 * @arg title
 * @text New Title (Default Language)
 * @desc The new title of the QuestLog.
 * 
 * @arg transTitle
 * @text New Title (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command SetQuestTitleFontSize
 * @text Set QuestLog Title's Font Size
 * @desc Sets the font size of the quest title
 *
 * @arg fontSize
 * @type number
 * @text Font Size
 * @desc The new font size value for the quest title
 * @min 1
 *
 * @command SetQuestInfoFontSize
 * @text Set Quest Description Font Size
 * @desc Set the Font Size of the Quest Description
 *
 * @arg fontSize
 * @type number
 * @text Font Size
 * @desc The new font size value for the quest title
 * @min 1
 *
 * @command SetQuestListFontSize
 * @text Set Quest List Font Size
 * @desc Set Quests' Name Font Size in the Quest List
 *
 * @arg fontSize
 * @type number
 * @min 1
 * @text Font Size
 * @desc The new font size value for the quest title
 *
 * @command newSetGiverPrefix
 * @text Set Giver Prefix
 * @desc Set the prefix for the quest's "Giver:" descriptor
 *
 * @arg prefix
 * @text New Prefix
 * @desc The new prefix for the quest giver (include ":" if you want them).
 * @type string
 * 
 * @arg transPrefix
 * @text New Prefix (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command newSetAreaPrefix
 * @text Set Area Prefix
 * @desc Set the prefix for the quest's "Area:" descriptor
 *
 * @arg prefix
 * @text New Prefix
 * @desc The new prefix for the quest area (include ":" if you want them).
 * @type string
 * 
 * @arg transPrefix
 * @text New Prefix (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command newSetStatusName
 * @text Set Status Prefix
 * @desc Set the name for the quest "Status:" prefix
 *
 * @arg name
 * @text New Status Name
 * @desc The new name for the quest status (include ":" if you want them).
 * @type string
 * 
 * @arg transName
 * @text New Status Name (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command newSetQuestCompleted
 * @text Set word for "Completed"
 * @desc Set the word for a completed quest
 *
 * @arg completed
 * @text New Completed
 * @desc The word to show for a completed quest
 * @type string
 * 
 * @arg transCompleted
 * @text New Completed (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command newSetQuestOngoing
 * @text Set word for "Ongoing"
 * @desc Set the word for an ongoing quest
 *
 * @arg ongoing
 * @text New Ongoing
 * @desc The word to show for an ongoing quest
 * @type string
 * 
 * @arg transOngoing
 * @text New Ongoing (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 *
 * @command newSetQuestFailed
 * @text Set word for "Failed"
 * @desc Set the word for a failed quest
 *
 * @arg failed
 * @text New Failed
 * @desc The word to show for a failed quest
 * @type string
 * 
 * @arg transFailed
 * @text New Failed (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 * 
 * @command newSetCommandName  
 * @text Set Command Name
 * @desc Sets the name of the quest command in the game menu
 *
 * @arg commandName
 * @type string
 * @text New Command Name
 * @desc The name to set for the quest command in the game menu
 * 
 * @arg transCommandName
 * @text New Command Name (Translations)
 * @default []
 * @type struct<genericSingleTrans>[]
 * 
 * @command line3
 * @text --- Game Editor Functionality ---
 * @desc Series of command to change words and fonts
 *
 * @command OpenQuestScene
 * @text Open Quest Scene
 * @desc Opens the Quest Scene.
 *
 * @command CheckQuestCompletion
 * @text Check if Quest is completed
 * @desc Checks if Quest is completed and stores result in a Switch or Variable
 *
 * @arg selectMode
 * @text Use Switch or Variable
 * @type select
 * @option Switch
 * @option Variable
 * @desc Switch is TRUE if completed, FALSE if not. Variable is 0 (ongoing), 1 (completed) or 2 (failed)
 * @default Switch
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to check. (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to check. (Must be exact name, leave blank if you use ID)
 * @default
 *
 * @arg switchID
 * @type number
 * @text Switch/Variable ID
 * @desc The ID of the switch or variable to set
 * @default 1
 * @min 1
 *
 * @command checkExistingQuest
 * @text Check if a quest exists
 * @desc Check if a quest is already added to the player questlog
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to track
 * @default 1
 * @min 1
 * 
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to track.(Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @arg switchID
 * @type switch
 * @text Result Switch ID
 * @desc The ID of the switch that will carry the result (TRUE if the quest is in the questLog, FALSE if not)
 * @default 1
 * @min 1
 * 
 * @command line4
 * @text --- Graphic Changes ---
 * @desc Plugin command to change the Graphic settings
 *
 * @command changeGraphics
 * @text Change Graphic Settings
 * @desc Change to the desired Graphic Settings
 *
 * @arg titleFlag
 * @text Show QuestLog Title?
 * @type select
 * @option Don't change
 * @value title0
 * @option Show Title Window
 * @value title1
 * @option Hide Title Window
 * @value title2
 * @default title0
 * @desc Choose if you want to show the QuestLog title
 *
 * @arg layoutAlign
 * @text QuestLog Layout
 * @desc Select the QuestLog Layout
 * @type select
 * @option Don't change
 * @value layout0
 * @option Quest List on left, Info on right
 * @value layout1
 * @option Quest List on right, Info on left
 * @value layout2
 * @default layout0
 *
 * @arg layoutSize
 * @text Layout Size
 * @desc Select the QuestLog Layout size
 * @type select
 * @option Don't change
 * @value size0
 * @option 100% of the Graphic Box (classic)
 * @value size1
 * @option 90% of the Graphic Box (RMMZ style)
 * @value size2
 * @option 100% of the Screen (For projects with different UI and Screen sizes)
 * @value size3
 * @option 90% of the Screen (For projects with different UI and Screen sizes)
 * @value size4
 * @default size0
 *
 * @arg touchCancel
 * @text Show Touch Cancel Button?
 * @type select
 * @option Don't change
 * @value cancel0
 * @option Show Touch Cancel
 * @value cancel1
 * @option Hide Touch Cancel
 * @value cancel2
 * @default cancel0
 * @desc Choose if you want to show the touch cancel button (make sure the player has non touch commands if you don't)
 *
 * @arg skinSettings
 * @text Custom Skin
 * @type struct<skinSetArg>
 * @desc If you want to use a custom skin use this settings
 * @default {"skinFlag":"skin0","skinName":"","redT":"0","greenT":"0","blueT":"0"}
 * 
 * @command line5
 * @text --- Quest Extra Features Management ---
 * @desc Plugin command to change the extra features like Logs and Tracking
 * 
 * @command activateLog
 * @text Activate\Deactivate existing Logs
 * @desc Turn visible or invisible a log that is already in the Quest extra Logs
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to check. (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to check. (Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @arg logID
 * @text Log ID
 * @desc The ID of the log
 * @default
 * 
 * @arg visibleFlag
 * @text Turn it Visible?
 * @type boolean
 * @on Visible
 * @off Hidden
 * @desc Make the log visible or invisible
 * @default true
 * 
 * @command addLog
 * @text Add a log to a quest
 * @desc Add a new log to a quest (its better practice to create all together and use visible/hidden flag)
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to check. (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to check. (Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @arg logSettings
 * @text Log properties
 * @type struct<detLogs>
 * @default {"logID":"Log000","logTitle":"Short tile here","logTitleTrans":"[]","isVisible":"true","graphStyle":"no","graphAlign":"center","graphPlacement":"above","iconID":"0","picID":"","picScale":"100","faceID":"","faceIndex":"0","charID":"","charSpecial":"false","charIndex":"0","textStyle":"true","textAlign":"center","textData":"","textDataTrans":"[]"}
 * @desc The detailed Log for the quest
 *
 * @command removeLog
 * @text Remove existing Log
 * @desc REMOVE (doesn't hide, it completely deletes) a log from a quest
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to check. (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to check. (Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @arg logID
 * @text Log ID
 * @desc The ID of the log
 * @default
 * 
 * @command enableTracking
 * @text Enable/Disable Tracking
 * @desc Enable or Disable the Quest HUD Tracking
 *
 * @arg trackingFlag
 * @text Enable Tracking?
 * @on Enable
 * @off Disable
 * @default true
 * @desc Enable or Disable the Quest HUD Tracking
 * 
 * @command enablePlayerTracking
 * @text Enable/Disable Player Tracking
 * @desc Give or remove the authorization to manually track quest to the player
 *
 * @arg trackingFlag
 * @text Enable Player Tracking?
 * @on Enable
 * @off Disable
 * @default true
 * @desc Enable or Disable the Quest HUD Tracking by the player
 * 
 * @arg wipeFlag
 * @text Wipe previous tracking?
 * @on Remove tracking
 * @off Keep tracking
 * @default true
 * @desc Clear all the current tracked quest (Useful if removing player authorization)
 * 
 * @command addRemoveTracking
 * @text Add or Remove Quest Tracking
 * @desc Add / Remove quest HUD Tracking from a Dev side (ignores max quest restriction)
 *
 * @arg addFlag
 * @text Add or Remove?
 * @type boolean
 * @on Add
 * @off Remove
 * @default true
 * @desc Choose if you want to add or remove the tracking
 * 
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to track (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to track.(Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @command changeTrackingText
 * @text Change Tracking Text
 * @desc Change the tracking text for a quest
 *
 * @arg questID
 * @type number
 * @text Quest ID
 * @desc The ID of the quest to track (Leave 0 if you use the name)
 * @default 0
 *
 * @arg questName
 * @text Quest Name
 * @desc The name of the quest to track.(Must be exact name, leave blank if you use ID)
 * @default
 * 
 * @arg text
 * @text New HUD Text
 * @desc The tracking text to show, keep it short (You can use RMMZ text codes)
 * @default
 * 
 * @arg textTrans
 * @parent text
 * @text New HUD Text (Translations)
 * @desc Translations for the HUD Text
 * @default []
 * @type struct<trackTxtTrans>[]
 * 
 * @command line6
 * @text --- Quest Storage ---
 * @desc Commands to store quests
 * 
 * @command storeQuests
 * @text Store Current Quests
 * @desc Store current quests under a Storage ID
 *
 * @arg storeID
 * @text Storage ID
 * @default main
 * @desc Update an existing storage ID or create a new one
 * 
 * @arg wipe
 * @type boolean
 * @text Wipe quests after storing?
 * @on Wipe
 * @off Keep
 * @desc If true it will remove every quest after storing them
 * @default true
 * 
 * @command recoverStore
 * @text Load Storage
 * @desc Search a storage ID and recovers it
 *
 * @arg storeID
 * @text Storage ID
 * @default main
 * @desc The ID of the storage to recover
 * 
 * @arg onError
 * @type boolean
 * @text Throw Error if no storage is detected?
 * @on Throw Error
 * @off Ignore the command
 * @desc Select how the load handles a mssing ID
 * @default true
 * 
 * @help WD_Quest.js
 *
 * The plugin creates a QuestLog that can will store your quests.
 *
 * The QuestLog can be called via script SceneManager.push(SceneManager.Scene_Quest);
 * or via Plugin Command or you can set the Parameter Menu Command true
 * to add a command in the game Menu
 *
 * You can edit both via parameter or plugin command (useful for translations)
 * the QuestLog title, the menu command text, the From: prefix, the Area:
 * prefix, the Status: prefix and the text used for "Completed" or "Ongoing"
 * quests
 *
 * The quest can be added via Plugin Command "Create Quest" and then they
 * will be displayed in the QuestLog ordered by their index.
 * Completed quest will still be visible but grayed out and pushed to the 
 * bottom of the list.
 *
 * Quests completion can be changed via Plugin Command, either by name
 * (must be exact name) or by quest ID
 *
 * Quests can also be completely removed (if you don't want to keep them
 * visible once completed or for whatever reason) via Plugin Command
 * either by name (must be exact name) or by quest ID
 *
 * If your game has a lot of quests I strongly advice to keep track of 
 * quest ID in some kind of note as the plugin doesn't show a full
 * list of the stored quest and their IDs
 *
 * NOTE: The Quest Description text can be split in different lines
 * by adding \n in the string. This works only for that field.
 * 
 * EXTERNAL SCRIPT CALL: You can call for "Check Quest Completion" from
 * any plugin or RPG MAKER MZ's Script Call:
 * - use window.WD_Interplugin_Quest.checkCompletionID(#) to search
 *   quest ID # completion
 * - use window.WD_Interplugin_Quest.checkCompletionName(#) to search
 *   quest name # completion
 * The script call will result true if completed or false if failed or
 * ongoing
 *
 * You can find more scripts and games on my Ko-Fi page:
 * https://ko-fi.com/winterdream
 * and on my Itch.io page:
 * https://winterdreamgamescreator.itch.io/
 * And if you want a direct line with me, you can join my Discord:
 * https://discord.gg/AZR38kGG4F
 *
 * By using this plugin you accept the Terms of Use (https://drive.google.com/file/d/1l_GadoZh3ylSvRm4hAoT2WOUXTpePpHf/view?usp=sharing)
 *
 * //////////////////////////////////////////////////
 * VERSION 2.5 Changelog
 * - Solved a bug that would show the wrong detailed logs list while
 *   changing quests (Thanks to Astral Bureau for the report!)
 * - Fixed the UI layer of HUD Tracking and the visible setting of the
 *   HUD window to avoid clipping with other RMMZ windows (Thanks to 
 *   RamondN for the report!)
 * - Made HUD activation more stable
 * VERSION 2.4.4 Changelog
 * - In the layout setting added the options to select UI Box (standard) or
 *   Screen Size (new) as reference for the QuestLog Window (Suggestion by Tails)
 * - Now the Tracking HUD offset can be set to negative (Suggestion by Tails)
 * - Added a compatibility patch with EliMZ MessageActions
 *   plugin, thanks to Succubus Nirriti for the report!
 * VERSION 2.4.3 Changelog
 * - Fixed some lines of code that didn't allow empty text elements,
 *   now you can remove terms such "Status", "Ongoing" or "Area"
 * - Made the Old Save conversion stronger and more stable
 * - Fixed a couple of alignment bugs in the QuestLog details 
 *   window
 * VERSION 2.4.2 Changelog
 * - Thanks to tinribs26 for those two reports!
 * - Fixed a bug in the new Quest Containers functionality
 *   that would break the savegames load. It's now patched
 *   with retrocompatibility for old broken saves.
 * - Fixed a font reset problem during category and quest
 *   titles display
 * VERSION 2.4.1 Changelog
 * - Now Categories names and Quest Titles accept RMMZ text
 *   commands, especially useful for colours
 * - Thanks to Tails for this two reports
 * - Fixed a bug on the "Add or Remove Quest Tracking"
 *   flag parameter that was a string instead of a boolean
 * - Fixed the "Change tracking text" plugin command that
 *   wouldn't refresh the HUD informations
 * VERSION 2.4 Changelog
 * - Added the option to hide/show a quest
 * - Added the option to show the quest title in the tracking HUD
 * - Now you can mass store quests undere ID driven storages, this will
 *   make it super easy to switch between different characters or parties
 * - Tracked quests will now automatically be removed when they are set to 
 *   Completed or Failed
 * - Fixed a bug in the conversion of old Quests to the new format
 * - Fixed a bug in logs activation / deactivation
 * - Fixed a bug in the Export Quest Completion functionality
 * VERSION 2.3 Changelog
 * - The Language control has been moved to WinterDream Core (you will
 *   need v1.3 or higher). QuestLog loses the parameters "Default Language"
 *   and AutoDetect language, now controller by the central plugin
 * VERSION 2.2 Changelog
 * - Changed the quest window refresh method to adapt it to Android
 *   deployments (Thanks to Stevynn for the report)
 * - Fixed incorrect font variable used in manual text mode
 * - Fixed description text drawing area calculation
 * VERSION 2.1 Changelog
 * - Fixed a nasty memory bug that would "remember" the quests when exiting
 *   an existing game and starting a new one without exiting the executable
 * - Added a command to check if a quest already exist (useful if you want to
 *   add a quest from different sources)
 * VERSION 2.0.2 Changelog
 * - Corrected a typo that would block the "Edit Quest Descriptor" command,
 *   thanks to tinribs26 for the report!
 * - Also correct a misplaced code line that would crash the above command
 *   when launched
 * VERSION 2.0.1 Changelog
 * - The plugin wasn't saving correctly the quests! Thanks to kricu for the
 *   report, now it's all correct. NOTE: Old savefiles won't work, sadly,
 *   only work with new saves.
 * - The tracking system now correctly saves the tracking preference and
 *   loads them when the player loads a savefile!
 * VERSION 2.0.0 Changelog
 * - Code rebuilt and updated but kept compatible with older versions
 * - Updated the Discord invite link in the help file that was invalid,
 *   embarassing!
 * - Added translations managed via WD_Core
 * - Dynamic Resize has been moved to WD_Core, plus a new text management
 *   option has been added: AutoWrap. Just write your sentence (supports RMMZ
 *   text codes) and the code will automatically wrap the text in the 
 *   designed area. No need to manually use the \n code (but you still can
 *   if you want to force a new line). If the text is still too big, the
 *   AutoWrap will try to shrink the font size to the minimum required.
 * - Added the optional rule to display an expanded data log if the player
 *   clicks on the quest
 * - Added the optional rule to activate a small Quest List on the map
 *   scene (either managed by the player or by the dev)
 * - Added Quest Categories to group quests together
 * VERSION 1.6.1 Changelog
 * - Changed the Quest Title from DrawText to DrawTextEx. The text will
 *   still be centered but now you can add the standard RMMZ commands 
 *   such as \I for Icons or \C for colours
 * VERSION 1.6 Changelog
 * - Fixed a bug were the old quest files would be deleted if any quest
 *   action (like accepting a quest) would be done after reloading a 
 *   save and before opening the questlog. (Thanks to TewiInaba for the
 *   report)
 * - Fixed a minor bug in the "Complete Quest" command
 * - Changed the Icon selection parameters from a number to an icon
 *   selector
 * - Added an external script call to check quest completion, see help
 * VERSION 1.5 Changelog
 * - Fixed an unexpected behaviour in the Auto Size description text 
 *   that resets the font size after correctly finding the fitting 
 *   value
 * - Added a padding value to the text to have the desired look to 
 *   the text graphic
 * - Added a full support for RMMZ text codes while keeping the alignment
 *   options
 * - Minor tweaks to the Plugin Parameters
 * - Now the plugin will automatically support compatibility with v1.1
 *   or lower without having to choose different files
 * VERSION 1.4 Changelog
 * - Added the setting to show or hide the title in the QuestLog
 * - Added the possibility to switch the quest list / quest info layout
 * - Added the option to use 100% of the graphic box (standard setting
 *   for this plugin) or 90% (standard RPG Maker MZ scene compatible 
 *   with cancel touch button)
 * - Added the possibility to hide the cancel touch button (useful for 
 *   100% size, but make sure the player has access to non touch controls)
 * - Added the possibility to change the windows skin for the QuestLog only,
 *   also you can change the colors tone (by re-selecting the default skin 
 *   you can apply different color tones to it)
 * - Added a new plugin command to change all the above mid-game
 * VERSION 1.3.2 Changelog
 * - Fixed an old part of the code creating two problems: A black layer under
 *   the scene and no centering if the Game UI was changed from the System 2
 *   tab as reported from ryf and Puppet Knight
 * VERSION 1.3.1 Changelog
 * - Hotfix for a small bug that would turn the menu command name to "true",
 *   thanks to ryf for the report!
 * VERSION 1.3 Changelog
 * - Updated the code to a newer version with, but not limited to, tweaks
 *   to the save and load functionality.
 * - Added the "Failed" status to the Quests with the needed changes to 
 *   "Add Quest", "Set Completion" and "Check Completion". Added bits of
 *   code to allow retrocompatibility with the older versions.
 * - Added the option to Autoset the Description Font Size, the plugin will
 *   range from a font size of 100 to a font size of 10, trying to fit the
 *   text both in width and height. You still need to break the lines with
 *   \n as before. The autosize text is only left aligned due to a limitation
 *   of the DrawTextEx feature used. (On the positive side, it should accept
 *   the usual RMMZ text code like \I for icons, didn't tried it)
 * - Added the possibility to add a longer title that will be displayed in the
 *   Quest Informations window (while the short name will be used for the quest
 *   list on the left). If you don't need it just leave blank the field.
 * - Minor fix on a bug that could cause the menu button to change name due to
 *   a conflict with the Quest List items
 * VERSION 1.2.2 Changelog 
 * - Hotfix for changes made in 1.2.1 as Plugin Parameters from Plugin Manager
 *   where not correctly loaded (Report by Grillmonger)
 * VERSION 1.2.1 Changelog 
 * - Fixed an issue reported by Grillmonger where QuestList would wipe if game 
 *   was closed entrely and then reloaded. Upon further investigation the fix 
 *   was extended to the other Plugin Parameters too (Such as Title Font, etc..)
 *   who would not carry over the changes if done via Plugin Command
 * VERSION 1.2 Changelog
 * - Merged "Set Completion by ID / by Name" and "Remove Quest by ID / by Name"
 * - Changed font size for the Quest List and Quest Description, you can change
 *   them via Plugin Parameters or Plugin Command 
 * - Changed the alignemnt con Quest List from "left" to "Center", can be 
 *   changed via Plugin Parameter
 * - Created a command that checks if a quest is completed and stores the
 *   result in a Switch of your choice (ON for Complete, OFF for Ongoing)
 * - Created a plugin command to change the Quest Icon searching it by ID or 
 *   Name
 * VERSION 1.1 Changelog
 * - Added new plugin command to edit an existing quest 
 *   description by ID or Quest Name
 * - Added new Plugin Command to change FontSize
 * //////////////////////////////////////////////////
 *
 */
 /*~struct~skinSet:
 * @param skinFlag
 * @text Use special Window Skin?
 * @type boolean
 * @desc Choose if you want to use a different skin for the QuestLog
 * @default false
 *
 * @param skinName
 * @text Select the Skin
 * @type file
 * @dir img/system
 * @desc The new skin you want to use
 * @default
 * 
 * @param redT
 * @text Red Tone Regulation
 * @type number
 * @desc (Optional) Choose the red tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 *
 * @param greenT
 * @text Green Tone Regulation
 * @type number
 * @desc (Optional) Choose the green tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 *
 * @param blueT
 * @text Blue Tone Regulation
 * @type number
 * @desc (Optional) Choose the blue tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 */
 /*~struct~skinSetArg:
 * @param skinFlag
 * @text Use special Window Skin?
 * @type select
 * @option Don't change
 * @value skin0
 * @option Use Custom
 * @value skin1
 * @option Use Default
 * @value skin2
 * @default skin0
 * @desc Choose if you want to use a different skin for the QuestLog
 *
 * @param skinName
 * @text Select the Skin
 * @type file
 * @dir img/system
 * @desc The new skin you want to use
 * @default
 * 
 * @param redT
 * @text Red Tone Regulation
 * @type number
 * @desc (Optional) Choose the red tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 *
 * @param greenT
 * @text Green Tone Regulation
 * @type number
 * @desc (Optional) Choose the green tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 *
 * @param blueT
 * @text Blue Tone Regulation
 * @type number
 * @desc (Optional) Choose the blue tone correction (from -255 to 255)
 * @default 0
 * @min -255
 * @max 255
 */
 /*~struct~settingsTransPack:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param questTitle
 * @text Title
 * @desc Set the title of the QuestLog
 * @default QuestLog
 *
 * @param giverPrefix
 * @text Giver Prefix
 * @desc How the "From:" prefix is shown in the Quest Giver
 * @default From:
 *
 * @param areaPrefix
 * @text Area Prefix
 * @desc How the "Area:" prefix is shown in the Quest Area
 * @default Area:
 *
 * @param statusName
 * @text Status Name
 * @desc How the "Status:" is shown for Quest Completion
 * @default Status:
 *
 * @param questCompleted
 * @text Quest Completed
 * @desc Word to show if quest is completed
 * @default Completed
 *
 * @param questOngoing
 * @text Quest Ongoing
 * @desc Word to show if quest is ongoing
 * @default Ongoing
 *
 * @param questFailed
 * @text Quest Failed
 * @desc Word to show if quest is failed
 * @default Failed
 * 
 * @param questMenuCommandName
 * @text Command Name
 * @desc Set the name of the command (if activated)
 * @default QuestLog
 * 
 * @param logText
 * @text Command Name for Logs
 * @desc The text of the command to open the detailed logs
 * @default Logs
 * 
 * @param trackText
 * @text Command Name for Quest Tracking (Track)
 * @desc The text of the command to start tracking a quest
 * @default Track Quest
 * 
 * @param untrackText
 * @text Command Name for Quest Tracking (Remove Track)
 * @desc The text of the command to stop tracking a quest
 * @default Don't Track
 */ 
 /*~struct~catData:
 * @param uncategorizedName
 * @text No Category Name
 * @desc The "category" where the quest with no category are grouped
 * @default --No Category--
 * 
 * @param uncategorizedNameTrans
 * @parent uncategorizedName
 * @text No Category Name (Translations)
 * @type struct<uncatTrans>[]
 * @desc The translations for No Categories
 * @default []
 * 
 * @param uncategoryIndex
 * @text No Category Index
 * @desc The Indexing order of no category group
 * @default 999
 * @type number
 * @min 1
 * 
 * @param categoriesDatabase
 * @text Categories Database
 * @type struct<catList>[]
 * @desc The various Categories
 * @default []
 */
 /*~struct~uncatTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param uncategorizedName
 * @text No Category Name (Translation)
 * @desc The "category" where the quest with no category are grouped (Translation)
 * @default --No Category--
 */
 /*~struct~catList:
 * @param categoryID
 * @text Category ID (Unique)
 * @desc The Category ID, must be unique
 * @default 1
 * @type number
 * @min 1
 * 
 * @param categoryIndex
 * @text Category Index
 * @desc The Indexing order of this category
 * @default 1
 * @type number
 * @min 1
 * 
 * @param categoryName
 * @text Category Name
 * @desc The name of the category
 * @default Important
 * 
 * @param categoryNameTrans
 * @parent categoryName
 * @text Category Name (Translations)
 * @type struct<catTrans>[]
 * @desc The translations for this category
 * @default []
 */ 
 /*~struct~catTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param categoryName
 * @text Category Name (Translation)
 * @desc The name of the category (Translation)
 * @default Important
 */
 /*~struct~detLogs:
 * @param logID
 * @text Log ID (Unique for the quest)
 * @desc The ID of the Log (must be unique for the quest)
 * @default Log000
 * 
 * @param logTitle
 * @text Log Small Title
 * @desc The small title in the log list (accept RMMZ code)
 * @default Short tile here
 * 
 * @param logTitleTrans
 * @parent logTitle
 * @text Log Small Title (Translations)
 * @desc The small title in the log list (translatations)
 * @default []
 * @type struct<logTitleTrans>[]
 * 
 * @param isVisible
 * @text Is Visible?
 * @desc Is the log visible?
 * @default true
 * @type boolean
 * @on Visible
 * @off Hidden
 * 
 * @param graphStyle
 * @text Graphic Image
 * @type select
 * @option No Image
 * @value no
 * @option Icon
 * @value icon
 * @option Face Image
 * @value face
 * @option Character Image
 * @value char
 * @option Picture
 * @value pic
 * @default no
 * @desc Choose the Graphic Element (if any)
 * 
 * @param graphAlign
 * @parent graphStyle
 * @text Graphic Alignment
 * @type select
 * @option Center
 * @value center
 * @option Left
 * @value left
 * @option Right
 * @value right
 * @default center
 * @desc Choose the Graphic Element alignment
 * 
 * @param graphPlacement
 * @parent graphStyle
 * @text Graphic Placement
 * @type select
 * @option Above Text
 * @value above
 * @option Below Text
 * @value below
 * @default above
 * @desc Choose the Graphic Element placement
 * 
 * @param iconID
 * @parent graphStyle
 * @text Icon Selection (if icon)
 * @type icon
 * @default 0
 * @desc Choose the icon
 * 
 * @param picID
 * @parent graphStyle
 * @text Picture Selection (if picture)
 * @type file
 * @dir img/pictures
 * @default
 * @desc Choose the picture file
 * 
 * @param picScale
 * @parent graphStyle
 * @text Picture Size (Percentage)
 * @type number
 * @default 100
 * @min 1
 * @max 9999
 * @desc The resize percentage of the Picture in percentage (by default 100%)
 * 
 * @param faceID
 * @parent graphStyle
 * @text Face Selection (if face)
 * @type file
 * @dir img/faces
 * @default
 * @desc Choose the face file
 * 
 * @param faceIndex
 * @parent graphStyle
 * @text Face Index (if face)
 * @type number
 * @default 0
 * @min 0
 * @max 7
 * @desc Choose the face index for the file (0 top-left .. 7 bottom-right)
 * 
 * @param charID
 * @parent graphStyle
 * @text Character Selection (if character)
 * @type file
 * @dir img/characters
 * @default
 * @desc Choose the character file
 * 
 * @param charIndex
 * @parent graphStyle
 * @text Character Index (if character)
 * @type number
 * @default 0
 * @min 0
 * @max 7
 * @desc Choose the character index for the file (0 top-left .. 7 bottom-right)
 * 
 * @param charSpecial
 * @parent charID
 * @text Is Character Sheet Special?
 * @desc Does the character sheet have the $ symbol? Meaning only 1 set insted of 8?
 * @default false
 * @type boolean
 * @on Special ($ symbol)
 * @off Normal
 * 
 * @param textStyle
 * @text Show Text Description
 * @type select
 * @default true
 * @type boolean
 * @on show Text
 * @off No Text
 * @desc Show text?
 * 
 * @param textAlign
 * @parent textStyle
 * @text Text Alignment
 * @type select
 * @option Center
 * @value center
 * @option Left
 * @value left
 * @option Right
 * @value right
 * @default center
 * @desc Choose the Text Element alignment
 * 
 * @param textData
 * @parent textStyle
 * @text Text Description
 * @type multiline_string
 * @default
 * @desc The text to show (compatible with RMMZ text codes)
 * 
 * @param textDataTrans
 * @parent textData
 * @text Text Description (Translations)
 * @type struct<txtDatatrans>[]
 * @default []
 * @desc The text to show (translations)
 */
 /*~struct~logTitleTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param logTitle
 * @text Log Title (Translation)
 * @desc The log title (Translation)
 * @default
 */
 /*~struct~txtDatatrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param textData
 * @parent textStyle
 * @text Text Description
 * @type multiline_string
 * @default
 * @desc The text to show (compatible with RMMZ text codes)
 */
 /*~struct~trackOpt:
 * @param maxQuest
 * @type number
 * @text Max Trackable Quests
 * @desc The number of quests that can be tracked, choose a sensible value based on the size of the HUD
 * @default 3
 * @min 1
 *
 * @param textColor
 * @text Text Color
 * @desc Hex Code for the HUD color (#ffffff default Rpg Maker white)
 * @default #ffffff
 * 
 * @param maxFont
 * @text Max Font Size
 * @type number
 * @desc The max font size fo the HUD elements (can be reduce to fit the descriptions)
 * @default 16
 * @min 5
 * 
 * @param hudSize
 * @text HUD Area Size
 * @type struct<trackOptSize>
 * @desc Set the area of the HUD
 * @default {"width":"20","height":"20","x":"0","y":"0"}
 * 
 * @param trackingStyle
 * @type boolean
 * @text Display Style
 * @desc Choose the display style
 * @on Only Text
 * @off Title + Text
 * @default true
 */
 /*~struct~trackOptSize:
 * @param width
 * @type number
 * @text HUD Width
 * @desc The width of the HUD area
 * @default 20
 * @min 10
 * @max 100
 *
 * @param height
 * @type number
 * @text HUD Height
 * @desc The height of the HUD area
 * @default 20
 * @min 10
 * @max 100
 * 
 * @param x
 * @type number
 * @text HUD X Start
 * @desc The X start of the HUD area (leftmost pixel)
 * @default 0
 * @min -9999
 * 
 * @param y
 * @type number
 * @text HUD Y Start
 * @desc The Y start of the HUD area (uppermost pixel)
 * @default 0
 * @min -9999
 */
 /*~struct~detTrack:
 * @param isTrackable
 * @type boolean
 * @text Can be tracked (only for Player Tracking)
 * @desc Player can track the quest? (Dev can always track quests)
 * @default true
 * @on Allow
 * @off Deny
 *
 * @param text
 * @text HUD Text
 * @desc The tracking text to show, keep it short (You can use RMMZ text codes)
 * @default
 * 
 * @param textTrans
 * @parent text
 * @text HUD Text (Translations)
 * @desc Translations for the HUD Text
 * @default []
 * @type struct<trackTxtTrans>[]
 */
 /*~struct~trackTxtTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param text
 * @text HUD Text (Translated)
 * @desc The tracking text to show, keep it short
 * @default
 */
 /*~struct~questTxtTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param short
 * @type string
 * @text Name (short)
 * @desc The name of the quest
 *
 * @param long
 * @type string
 * @text Long Title
 * @desc A longer title for the description page, leave blank to use the Quest Name
 *
 * @param giver
 * @type string
 * @text Giver
 * @desc Information on the quest giver
 *
 * @param area
 * @type string
 * @text Area
 * @desc Information on the location of the quest
 *
 * @param desc
 * @type string
 * @text Description
 * @desc Information on the quest
 */
 /*~struct~genericSingleTrans:
 * @param language
 * @text Translation Language
 * @type select
 * @default English
 * @option 	Abkhazian
 * @option 	Afar
 * @option 	Afrikaans
 * @option 	Akan
 * @option 	Albanian
 * @option 	Amharic
 * @option 	Arabic
 * @option 	Aragonese
 * @option 	Armenian
 * @option 	Assamese
 * @option 	Avaric
 * @option 	Avestan
 * @option 	Aymara
 * @option 	Azerbaijani
 * @option 	Bambara
 * @option 	Bashkir
 * @option 	Basque
 * @option 	Belarusian
 * @option 	Bengali
 * @option 	Bislama
 * @option 	Bosnian
 * @option 	Breton
 * @option 	Bulgarian
 * @option 	Burmese
 * @option 	Catalan, Valencian
 * @option 	Chamorro
 * @option 	Chechen
 * @option 	Chichewa, Chewa, Nyanja
 * @option 	Chinese
 * @option 	Church Slavonic, Old Slavonic, Old Church Slavonic
 * @option 	Chuvash
 * @option 	Cornish
 * @option 	Corsican
 * @option 	Cree
 * @option 	Croatian
 * @option 	Czech
 * @option 	Danish
 * @option 	Divehi, Dhivehi, Maldivian
 * @option 	Dutch, Flemish
 * @option 	Dzongkha
 * @option 	English
 * @option 	Esperanto
 * @option 	Estonian
 * @option 	Ewe
 * @option 	Faroese
 * @option 	Fijian
 * @option 	Finnish
 * @option 	French
 * @option 	Western Frisian
 * @option 	Fulah
 * @option 	Gaelic, Scottish Gaelic
 * @option 	Galician
 * @option 	Ganda
 * @option 	Georgian
 * @option 	German
 * @option 	Greek, Modern (1453–)
 * @option 	Kalaallisut, Greenlandic
 * @option 	Guarani
 * @option 	Gujarati
 * @option 	Haitian, Haitian Creole
 * @option 	Hausa
 * @option 	Hebrew
 * @option 	Herero
 * @option 	Hindi
 * @option 	Hiri Motu
 * @option 	Hungarian
 * @option 	Icelandic
 * @option 	Ido
 * @option 	Igbo
 * @option 	Indonesian
 * @option 	Interlingua (International Auxiliary Language Association)
 * @option 	Interlingue, Occidental
 * @option 	Inuktitut
 * @option 	Inupiaq
 * @option 	Irish
 * @option 	Italian
 * @option 	Japanese
 * @option 	Javanese
 * @option 	Kannada
 * @option 	Kanuri
 * @option 	Kashmiri
 * @option 	Kazakh
 * @option 	Central Khmer
 * @option 	Kikuyu, Gikuyu
 * @option 	Kinyarwanda
 * @option 	Kirghiz, Kyrgyz
 * @option 	Komi
 * @option 	Kongo
 * @option 	Korean
 * @option 	Kuanyama, Kwanyama
 * @option 	Kurdish
 * @option 	Lao
 * @option 	Latin
 * @option 	Latvian
 * @option 	Limburgan, Limburger, Limburgish
 * @option 	Lingala
 * @option 	Lithuanian
 * @option 	Luba-Katanga
 * @option 	Luxembourgish, Letzeburgesch
 * @option 	Macedonian
 * @option 	Malagasy
 * @option 	Malay
 * @option 	Malayalam
 * @option 	Maltese
 * @option 	Manx
 * @option 	Maori
 * @option 	Marathi
 * @option 	Marshallese
 * @option 	Mongolian
 * @option 	Nauru
 * @option 	Navajo, Navaho
 * @option 	North Ndebele
 * @option 	South Ndebele
 * @option 	Ndonga
 * @option 	Nepali
 * @option 	Norwegian
 * @option 	Norwegian Bokmål
 * @option 	Norwegian Nynorsk
 * @option 	Occitan
 * @option 	Ojibwa
 * @option 	Oriya
 * @option 	Oromo
 * @option 	Ossetian, Ossetic
 * @option 	Pali
 * @option 	Pashto, Pushto
 * @option 	Persian
 * @option 	Polish
 * @option 	Portuguese
 * @option 	Punjabi, Panjabi
 * @option 	Quechua
 * @option 	Romanian, Moldavian, Moldovan
 * @option 	Romansh
 * @option 	Rundi
 * @option 	Russian
 * @option 	Northern Sami
 * @option 	Samoan
 * @option 	Sango
 * @option 	Sanskrit
 * @option 	Sardinian
 * @option 	Serbian
 * @option 	Shona
 * @option 	Sindhi
 * @option 	Sinhala, Sinhalese
 * @option 	Slovak
 * @option 	Slovenian
 * @option 	Somali
 * @option 	Southern Sotho
 * @option 	Spanish, Castilian
 * @option 	Sundanese
 * @option 	Swahili
 * @option 	Swati
 * @option 	Swedish
 * @option 	Tagalog
 * @option 	Tahitian
 * @option 	Tajik
 * @option 	Tamil
 * @option 	Tatar
 * @option 	Telugu
 * @option 	Thai
 * @option 	Tibetan
 * @option 	Tigrinya
 * @option 	Tonga (Tonga Islands)
 * @option 	Tsonga
 * @option 	Tswana
 * @option 	Turkish
 * @option 	Turkmen
 * @option 	Twi
 * @option 	Uighur, Uyghur
 * @option 	Ukrainian
 * @option 	Urdu
 * @option 	Uzbek
 * @option 	Venda
 * @option 	Vietnamese
 * @option 	Volapük
 * @option 	Walloon
 * @option 	Welsh
 * @option 	Wolof
 * @option 	Xhosa
 * @option 	Sichuan Yi, Nuosu
 * @option 	Yiddish
 * @option 	Yoruba
 * @option 	Zhuang, Chuang
 * @option 	Zulu
 * 
 * @param transl
 * @type string
 * @text Translated Term
 * @desc The translation of the term in the selected language
 */

 //TODO 
 //- Quest list skin

!function(){const t=PluginManager.parameters("WD_Quest"),e={mayor:2,minor:4,hotfix:2};class p{constructor(t,e,a,s,i,n,r,o,u,g,l,c,h,d){this.id=e,this.icon=a,this.shortTitle=s,this.longTitle=i,this.index=n,this.giver=r,this.area=o,this.description=u,this.status=g,this.trackData=this.buildTrackData(t?null:l,this.id),this.logs=this.buildLogs(t?null:c),this.translationPacks=h,this.categoryID=t?0:d,this.hidden=!1}buildTrackData(t,e){e={id:e,isTrackable:!1,trackText:null,trackTextTranslations:[]};if(null!=t){var t=JSON.parse(t),a=(e.isTrackable="true"===t.isTrackable,e.trackText=t.text,JSON.parse(t.textTrans));for(let t=0;t<a.length;t++)a[t]=JSON.parse(a[t]);e.trackTextTranslations=a}return e}buildLogs(t){var a=[];if(null!=t){var s=JSON.parse(t);for(let e=0;e<s.length;e++){s[e]=JSON.parse(s[e]),s[e].isVisible="true"===s[e].isVisible,s[e].textStyle="true"===s[e].textStyle,s[e].charSpecial="true"===s[e].charSpecial,s[e].charIndex=parseInt(s[e].charIndex),s[e].faceIndex=parseInt(s[e].faceIndex),s[e].iconID=parseInt(s[e].iconID),s[e].picScale=parseInt(s[e].picScale),s[e].textDataTrans=JSON.parse(s[e].textDataTrans);for(let t=0;t<s[e].textDataTrans.length;t++)s[e].textDataTrans[t]=JSON.parse(s[e].textDataTrans[t]);s[e].logTitleTrans=JSON.parse(s[e].logTitleTrans);for(let t=0;t<s[e].logTitleTrans.length;t++)s[e].logTitleTrans[t]=JSON.parse(s[e].logTitleTrans[t]);var i=s[e],i={id:i.logID,isVisible:i.isVisible,graphics:{style:i.graphStyle,align:i.graphAlign,placement:i.graphPlacement,icon:{id:i.iconID},face:{id:i.faceID,index:i.faceIndex},character:{id:i.charID,index:i.charIndex,isSpecial:i.charSpecial},picture:{id:i.picID,scale:i.picScale}},text:{showText:i.textStyle,align:i.textAlign,data:i.textData,transData:i.textDataTrans},title:{default:i.logTitle,trans:i.logTitleTrans}};a.push(i)}}return a}restoreFromSave(t){Object.assign(this,t)}}class a{constructor(){this.compatibilityLoad=!1,this.questsArray=[]}loadQuests(){F(),this.compatibilityLoad||(this.compatibilityLoad=!0,this.searchOldVersionSave()),this.classCheckQuestList()}searchOldVersionSave(){var t=R();if(0<t.length){for(const e of t){let t=null;t=e.hasOwnProperty("complete")&&!e.hasOwnProperty("status")?e.complete?"completed":"ongoing":e.status,this.addQuest(!0,e.id,e.icon,e.name,e.longTitle,e.index,e.giver,e.area,e.description,t,null,null,[],0)}this.saveQuests()}}saveQuests(){z()}addQuest(t,e,a,s,i,n,r,o,u,g,l,c,h,d){t=new p(t,e,a,s,i,n,r,o,u,g,l,c,h,d);this.noDuplicate(t)&&this.questsArray.push(t)}noDuplicate(t){var e=new Set;for(const a of this.questsArray)e.add(a.id);return!e.has(t.id)||(S(t,0),!1)}removeQuest(e,a){var s={found:!1,index:0};for(let t=0;t<this.questsArray.length;t++)if(!isNaN(e)&&0<e&&this.questsArray[t].id===e||""!==a&&this.questsArray[t].shortTitle===a){s.found=!0,s.index=t;break}s.found&&this.questsArray.splice(s.index,1)}loadFromSave(t){this.compatibilityLoad=t.compatibilityLoad,this.questsArray=t.questsArray,this.classCheckQuestList()}classCheckQuestList(){for(let t=0;t<this.questsArray.length;t++){var e,a=this.questsArray[t];a instanceof p||((e=new p).restoreFromSave(a),this.questsArray[t]=e)}}wipeQuests(){this.questsArray=[],D.extraSettings.tracking.currentlyTracked=[],u=!0,$gameMap.requestRefresh()}}class s{constructor(){this.version=e,this.textData={defaultData:{questTitle:t.Title??"QuestLog",giverPrefix:t.giverprefix??"From:",areaPrefix:t.areaprefix??"Area:",statusName:t.statusname??"Status:",questCompleted:t.questcompleted??"Completed",questOngoing:t.questongoing??"Ongoing",questFailed:t.questfailed??"Failed",questMenuCommandName:t.commandname??"QuestLog",logText:t.logsDefText??"Logs",trackText:t.trackDefText??"Track Quest",untrackText:t.untrackDefText??"Don't Track"},translationData:[],currentLanguage:{questTitle:"",giverPrefix:"",areaPrefix:"",statusName:"",questCompleted:"",questOngoing:"",questFailed:"",questMenuCommandName:"",logText:"",trackText:"",untrackText:""}},this.loadTranslationsPack(),this.textSettings={infoAlign:t.infoalign||"center",listAlign:t.listAlign||"center",textManagement:t.textManagement||"wrap",fontSize:Number(t.fontsize)||40,descriptionSize:Number(t.descriptionSize)||20,listSize:Number(t.listSize)||20,paddingValue:Number(t.paddingValue)||50},this.layoutSettings={showMenuCommand:"true"===t.menucommand,titleFlag:"true"===t.titleFlag,layoutAlign:t.layoutAlign||"layout1",layoutSize:t.layoutSize||"size1",touchCancel:"true"===t.touchCancel,skinSettings:h(t.skinSettings)},this.categoriesSettings=this.elaborateCategoriesParameters(),this.compatibilityLoad=!1,this.extraSettings=this.eleborateExtraParameters(),this.errorManagement=t.errorManagement||"err1"}eleborateExtraParameters(){return{logs:{isActive:"true"===t.logsFlag},tracking:{isActive:"no"!==t.trackSetting,allowPlayerTracking:"player"===t.trackSetting,trackingSettings:this.extractTrackingConfig(JSON.parse(t.trackConfiguration),!0),hudSettings:this.extractTrackingConfig(JSON.parse(t.trackConfiguration),!1),currentlyTracked:[],showTitle:this.extractShowTitle(JSON.parse(t.trackConfiguration))}}}extractTrackingConfig(t,e){return e?{maxQuest:parseInt(t.maxQuest)||3,color:t.textColor||"#ffffff",maxFont:parseInt(t.maxFont)||16}:(e=JSON.parse(t.hudSize),{width:parseInt(e.width)||20,height:parseInt(e.height)||20,x:parseInt(e.x)||0,y:parseInt(e.y)||0})}elaborateCategoriesParameters(){return{isActive:"true"===t.categoryFlag,displayType:function(t){switch(t){case"category":return 0;case"status":return 1;default:return 0}}(t.categoryPriority),categories:function(t){var a=JSON.parse(t);a.uncategorizedNameTrans=JSON.parse(a.uncategorizedNameTrans);for(let t=0;t<a.uncategorizedNameTrans.length;t++)a.uncategorizedNameTrans[t]=JSON.parse(a.uncategorizedNameTrans[t]);a.uncategoryIndex=parseInt(a.uncategoryIndex),a.categoriesDatabase=JSON.parse(a.categoriesDatabase);for(let e=0;e<a.categoriesDatabase.length;e++){a.categoriesDatabase[e]=JSON.parse(a.categoriesDatabase[e]),a.categoriesDatabase[e].categoryID=parseInt(a.categoriesDatabase[e].categoryID),a.categoriesDatabase[e].categoryIndex=parseInt(a.categoriesDatabase[e].categoryIndex),a.categoriesDatabase[e].categoryNameTrans=JSON.parse(a.categoriesDatabase[e].categoryNameTrans);for(let t=0;t<a.categoriesDatabase[e].categoryNameTrans.length;t++)a.categoriesDatabase[e].categoryNameTrans[t]=JSON.parse(a.categoriesDatabase[e].categoryNameTrans[t])}var e=new Set,s=[{id:0,index:a.uncategoryIndex,name:a.uncategorizedName,trans:a.uncategorizedNameTrans}];e.add(0);for(const n of a.categoriesDatabase){var i={id:n.categoryID,index:n.categoryIndex,name:n.categoryName,trans:n.categoryNameTrans};e.has(n.categoryID)?S(n,1):(e.add(n.categoryID),s.push(i))}return s}(t.categoryDatabase)}}extractShowTitle(t){return"false"===t.trackingStyle}loadTranslationsPack(){var e=JSON.parse(t.translationPacks);for(let t=0;t<e.length;t++)e[t]=JSON.parse(e[t]);this.textData.translationData=e}saveSettings(){E(this)}loadSettings(){this.compatibilityLoad||this.checkOldSaves(),J(),this.changeLanguage()}checkOldSaves(){if(this.compatibilityLoad=!0,this.version)this.version.mayor<e.mayor||this.version.mayor===e.mayor&&this.version.minor<e.minor||this.version.mayor===e.mayor&&this.version.minor===e.minor&&(this.version.hotfix,e);else{const n=G();if(null!==n){var t=(t,e)=>{for(const i of t)a=n,s=i,Object.prototype.hasOwnProperty.call(a,s)&&(e[i]=n[i]??e[i]);var a,s};t(["questTitle","areaPrefix","giverPrefix","statusName","questCompleted","questOngoing","questFailed","questMenuCommandName"],this.textData.defaultData),t(["fontSize","descriptionSize","listSize"],this.textSettings),t(["titleFlag","layoutAlign","layoutSize","skinSettings","touchCancel"],this.layoutSettings)}}}changeLanguage(){var t={questTitle:this.textData.defaultData.questTitle,giverPrefix:this.textData.defaultData.giverPrefix,areaPrefix:this.textData.defaultData.areaPrefix,statusName:this.textData.defaultData.statusName,questCompleted:this.textData.defaultData.questCompleted,questOngoing:this.textData.defaultData.questOngoing,questFailed:this.textData.defaultData.questFailed,questMenuCommandName:this.textData.defaultData.questMenuCommandName,logText:this.textData.defaultData.logText,trackText:this.textData.defaultData.trackText,untrackText:this.textData.defaultData.untrackText,language:null},e=this.textData.translationData;this.textData.currentLanguage=window.WD_Interplugin_Core.resolveLanguage(t,e)}updateLanguageTerms(e,t,a){if(t)this.textData.defaultData[e]=a;else for(const i of a){var s=i.language;let t=null;for(const n of this.textData.translationData)if(n.language===s){t=n;break}t&&(t[e]=i.transl)}this.changeLanguage()}restoreFromSave(t){Object.assign(this,t)}}class i{constructor(){this.storage=[]}restoreFromSave(t){t?Array.isArray(t)?this.storage=t:Array.isArray(t.storage)?this.storage=t.storage:this.storage=[]:this.storage=[],this.classCheckQuestList()}classCheckQuestList(){for(const s of this.storage)for(let t=0;t<s.questsArray.length;t++){var e,a=s.questsArray[t];a instanceof p||((e=new p).restoreFromSave(a),s.questsArray[t]=e)}}saveCurrentAsStorage(e,t=!1){M();var a={id:e,questsArray:JSON.parse(JSON.stringify(f.questsArray))},s=this.storage.findIndex(t=>t.id===e);0<=s?this.storage[s]=a:this.storage.push(a),t&&f.wipeQuests(),H()}loadStorageFromId(e,t=!0){M();var a=this.storage.find(t=>t.id===e);if(a){a=JSON.parse(JSON.stringify(a.questsArray));f.wipeQuests(),f.questsArray=a,f.classCheckQuestList()}else if(t)throw new Error("WD_Quest: Unable to find storage with id "+e)}}var n=PluginManager._scripts,r={coreFound:!1,coreIndex:-1,thisIndex:-1};for(let t=0;t<n.length;t++)"WD_Core"===n[t]&&(r.coreFound=!0,r.coreIndex=t),"WD_Quest"===n[t]&&(r.thisIndex=t);if(!r.coreFound)throw new Error("WD_Quest: The plugin WD_Core has not been found! WD_Core is needed to run this plugin, please dowload on Itch or Ko-fi for free (see help file)");if(r.thisIndex<r.coreIndex)throw new Error("WD_Quest: The plugin WD_Core is loaded after this plugin, please move the plugin WD_Core ABOVE this plugin in the Rpg Maker Plugin Manager");if(!window.WD_Interplugin_Core.requiredCoreVersion({major:1,minor:3,hotfix:0}))throw new Error("WD_Quest: The plugin WD_Core is outdated! WD_Core needs to be at least v1.3 for this plugin, please dowload on Itch or Ko-fi for free (see help file)");let f=null,D=null,o=null,u=!1;function g(){!function(){if(!$gameSystem)return;$gameSystem._questContainer?(t=JSON.parse(JSON.stringify($gameSystem._questContainer)),$gameSystem._questContainer=new a,$gameSystem._questContainer.loadFromSave(t)):$gameSystem._questContainer=new a;{var t;$gameSystem._questPluginParams?(t=JSON.parse(JSON.stringify($gameSystem._questPluginParams)),$gameSystem._questPluginParams=new s,$gameSystem._questPluginParams.restoreFromSave(t)):$gameSystem._questPluginParams=new s}{var e;$gameSystem._questStorage?(e=JSON.parse(JSON.stringify($gameSystem._questStorage)),$gameSystem._questStorage=new i,$gameSystem._questStorage.restoreFromSave(e)):$gameSystem._questStorage=new i}return f=$gameSystem._questContainer,D=$gameSystem._questPluginParams,o=$gameSystem._questStorage,1}()&&setTimeout(g,100)}function l(t){return JSON.parse(t||"[]").map(t=>"string"==typeof t?JSON.parse(t):t)}function c(t){if("Width"===t)switch(D.layoutSettings.layoutSize){case"size2":return.9*Graphics.boxWidth;case"size3":return Graphics.width;case"size4":return.9*Graphics.width;default:return Graphics.boxWidth}else if("Height"===t)switch(D.layoutSettings.layoutSize){case"size2":return.9*Graphics.boxHeight;case"size3":return Graphics.height;case"size4":return.9*Graphics.height;default:return Graphics.boxHeight}else{if("Anchor"!==t)return"MaxLines"===t?"size1"===D.layoutSettings.layoutSize||"size3"===D.layoutSettings.layoutSize?11+(D.layoutSettings.titleFlag?0:4):10+(D.layoutSettings.titleFlag?0:3):"totalWidth"===t?"size1"===D.layoutSettings.layoutSize||"size2"===D.layoutSettings.layoutSize?Graphics.boxWidth:Graphics.width:"totalHeight"===t?"size1"===D.layoutSettings.layoutSize||"size2"===D.layoutSettings.layoutSize?Graphics.boxHeight:Graphics.height:"xOff"===t?"size1"===D.layoutSettings.layoutSize||"size2"===D.layoutSettings.layoutSize?0:(Graphics.boxWidth-Graphics.width)/2:"yOff"===t?"size1"===D.layoutSettings.layoutSize||"size2"===D.layoutSettings.layoutSize?0:(Graphics.boxHeight-Graphics.height)/2:void 0;switch(D.layoutSettings.layoutSize){case"size2":return.1*Graphics.boxHeight;case"size3":return 0;case"size4":return.1*Graphics.height;default:return 0}}}function h(t){t=JSON.parse(t);return t.skinFlag="true"===t.skinFlag,t.redT=parseInt(t.redT),t.greenT=parseInt(t.greenT),t.blueT=parseInt(t.blueT),t}function d(){return D.layoutSettings.skinSettings.skinFlag&&""!==D.layoutSettings.skinSettings.skinName?ImageManager.loadSystem(D.layoutSettings.skinSettings.skinName):ImageManager.loadSystem("Window")}function m(){return D.layoutSettings.skinSettings.skinFlag&&""!==D.layoutSettings.skinSettings.skinName?[D.layoutSettings.skinSettings.redT,D.layoutSettings.skinSettings.greenT,D.layoutSettings.skinSettings.blueT]:$gameSystem.windowTone()}function S(t,e){switch(e){case 0:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: This quest ID already exist! Use unique Quest ID! ID: "+t);case"err2":console.error("WD_Quest: Added a quest with a non-unique Quest ID! Bad plugin behaviour expected!!! ID: "+t);break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;case 1:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: The categories have a duplicated ID! Use only unique ID! ID: "+t);case"err2":console.error("WD_Quest: Tracked a duplicate ID in the categories database! Bad Plugin behaviour expected!! ID: "+t);break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;case 2:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: Searching By ID in the Quest Container, no quests or more than one quest found. ID: "+t);case"err2":console.error("WD_Quest: Search returned no result or more than one result while searching for ID "+t+" bad behaviour expected!");break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;case 3:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: TextManager argument is invalid! Argument: "+t);case"err2":console.error("WD_Quest: TextManager argument is invalid! Argument: "+t);break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;case 4:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: Unable to find Category ID for translation. ID: "+t);case"err2":console.error("WD_Quest: Unable to find Category ID for translation. ID: "+t);break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;case 6:switch(D.errorManagement){case"err1":throw new Error("WD_Quest: Trying to add a log with an already existing ID! Please use an unique ID for every log (in the quest)! ID: "+t);case"err2":console.error("WD_Quest: Added a log with an already existing ID! Bad behaviour expected! ID: "+t);break;case"err3":break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected error argument: "+D.errorManagement)}break;default:throw new Error("WD_Quest: Error, in the Call Error Manager, that's ironic! Unexpected type: "+e)}}function y(a,t){var s=D.extraSettings.tracking.currentlyTracked;if(t){let t=null;for(const i of f.questsArray)if(i.id===a){t=i;break}if(t){var e={id:t.id,defaultText:t.trackData.trackText,translationText:t.trackData.trackTextTranslations,needRefresh:function(t,e){var a=[t];let s=!1;for(const i of e)a.push(i.text);for(const n of a)if(n){if(n.includes("V[")){s=!0;break}if(n.includes("N[")){s=!0;break}if(n.includes("P[")){s=!0;break}if(n.includes("G")){s=!0;break}}return s}(t.trackData.trackText,t.trackData.trackTextTranslations)};for(const n of s)if(n.id===e.id)return;s.push(e)}}else{let e=null;for(let t=0;t<s.length;t++)if(s[t].id===a){e=t;break}null!==e&&s.splice(e,1)}D.saveSettings()}const x=Scene_Menu.prototype.create,w=(Scene_Menu.prototype.create=function(){x.call(this),D.loadSettings()},Window_MenuCommand.prototype.addOriginalCommands),I=(Window_MenuCommand.prototype.addOriginalCommands=function(){w.call(this),D.layoutSettings.showMenuCommand&&this.addCommand(D.textData.currentLanguage.questMenuCommandName,"quest",!0)},Scene_Menu.prototype.createCommandWindow),T=(Scene_Menu.prototype.createCommandWindow=function(){I.call(this),D.layoutSettings.showMenuCommand&&this._commandWindow.setHandler("quest",this.commandQuest.bind(this))},Scene_Menu.prototype.commandQuest=function(){SceneManager.push(Q)},Game_Map.prototype.refresh),v=(Game_Map.prototype.refresh=function(){T.call(this),this.checkWdQuestHudRefresh()},Game_Map.prototype.checkWdQuestHudRefresh=function(){if(u){u=!1;var e=SceneManager._scene;e._wdQuestHud&&e._wdQuestHud.updateText()}else{let t=!1;if(0<D.extraSettings.tracking.currentlyTracked.length)for(const a of D.extraSettings.tracking.currentlyTracked)if(a.needRefresh){t=!0;break}t&&(e=SceneManager._scene)._wdQuestHud&&e._wdQuestHud.updateText()}},Scene_Map.prototype.createDisplayObjects);function q(){this.initialize(...arguments)}function Q(){this.initialize(...arguments)}function _(){this.initialize(...arguments)}function k(){this.initialize(...arguments)}Scene_Map.prototype.createDisplayObjects=function(){D.loadSettings(),f.loadQuests(),v.call(this),D.extraSettings.tracking.isActive&&this.wdQuestCreateTrackingHud()},Scene_Map.prototype.wdQuestCreateTrackingHud=function(){var t;this._wdQuestHud||(t=this.wdQuestCreateTrackingHudRect(),this._wdQuestHud=new q(t),t=this.getChildIndex(this._windowLayer),this.addChildAt(this._wdQuestHud,t))},Scene_Map.prototype.wdQuestCreateTrackingHudRect=function(){var t=c("xOff")+D.extraSettings.tracking.hudSettings.x,e=c("yOff")+D.extraSettings.tracking.hudSettings.y,a=c("totalWidth")*(D.extraSettings.tracking.hudSettings.width/100),s=c("totalHeight")*(D.extraSettings.tracking.hudSettings.height/100);return new Rectangle(t,e,a,s)},((q.prototype=Object.create(Window_Base.prototype)).constructor=q).prototype.initialize=function(t){Window_Base.prototype.initialize.call(this,t),this.setBackgroundType(2),this.updateText()},q.prototype.updateText=function(){if(this.contents&&(this.contents.clear(),this.contentsBack.clear()),this.visible=D.extraSettings.tracking.isActive,this.visible&&D.extraSettings.tracking.isActive){let t="";for(const s of D.extraSettings.tracking.currentlyTracked){var e,a;""!==t&&(t+="\n"),D.extraSettings.tracking.showTitle&&(e=this.getQuestTitle(s.id))&&""!==e&&(t=t+e+"\n"),0<s.translationText.length?(e={language:null,text:s.defaultText},a=window.WD_Interplugin_Core.resolveLanguage(e,s.translationText),t+=a.text):t+=s.defaultText}this.changeTextColor(D.extraSettings.tracking.trackingSettings.color),window.WD_Interplugin_Core.autoWrap(this,0,0,this.innerWidth,this.innerHeight,t,D.extraSettings.tracking.trackingSettings.maxFont,"left"),this.resetFontSettings()}},q.prototype.getQuestTitle=function(e){var t,a=f.questsArray.filter(t=>t.id===e);return 1===a.length?(t=(a=a[0]).shortTitle,(a=a.translationPacks)&&0<a.length?window.WD_Interplugin_Core.resolveLanguage({language:null,short:t},a).short:t):""},((Q.prototype=Object.create(Scene_MenuBase.prototype)).constructor=Q).prototype.initialize=function(){Scene_MenuBase.prototype.initialize.call(this),D.loadSettings(),f.loadQuests()},Q.prototype.create=function(){Scene_MenuBase.prototype.create.call(this),D.layoutSettings.titleFlag&&this.createTitleWindow(),this.createQuestListWindow(),this.createQuestInfoWindow()},Q.prototype.createTitleWindow=function(){var t=this.titleWindowRect();this._titleWindow=new _(t),this.addWindow(this._titleWindow)},Q.prototype.titleWindowRect=function(){var t=c("xOff"),e=c("yOff")+c("Anchor"),a=c("totalWidth"),s=.2*c("Height");return new Rectangle(t,e,a,s)},Q.prototype.createQuestListWindow=function(){var t=this.questListWindowRect();this._questListWindow=new k(t),this._questListWindow.setHandler("ok",this.onQuestListOk.bind(this)),this._questListWindow.setHandler("cancel",this.onQuestListCancel.bind(this)),this.addWindow(this._questListWindow)},Q.prototype.questListWindowRect=function(){var t="layout1"===D.layoutSettings.layoutAlign?c("xOff"):c("xOff")+.7*c("totalWidth"),e=c("yOff")+c("Anchor")+(D.layoutSettings.titleFlag?.2*c("Height"):0),a=.3*c("totalWidth"),s=D.layoutSettings.titleFlag?.8*c("Height"):c("Height");return new Rectangle(t,e,a,s)},Q.prototype.createQuestInfoWindow=function(){var t=this.questInfoWindowRect();this._questInfoWindow=new C(t),this._questInfoWindow.setHandler("logs",this.onQuestLogs.bind(this)),this._questInfoWindow.setHandler("track",this.onQuestTrack.bind(this)),this._questInfoWindow.setHandler("cancel",this.onQuestInfoCancel.bind(this)),this.addWindow(this._questInfoWindow)},Q.prototype.questInfoWindowRect=function(){var t="layout1"===D.layoutSettings.layoutAlign?c("xOff")+.3*c("totalWidth"):c("xOff"),e=c("yOff")+c("Anchor")+(D.layoutSettings.titleFlag?.2*c("Height"):0),a=.7*c("totalWidth"),s=D.layoutSettings.titleFlag?.8*c("Height"):c("Height");return new Rectangle(t,e,a,s)},Q.prototype.onQuestListOk=function(){(D.extraSettings.logs.isActive||D.extraSettings.tracking.isActive&&D.extraSettings.tracking.allowPlayerTracking?(this._questInfoWindow.select(0),this._questInfoWindow):this._questListWindow).activate()},Q.prototype.createQuestLogsExtraWindow=function(){var t=this.questInfoWindowRect();this._questLogExtraWindow=new b(t),this._questLogExtraWindow.setHandler("ok",this.onQuestLogOk.bind(this)),this._questLogExtraWindow.setHandler("cancel",this.onQuestLogCancel.bind(this)),this.addWindow(this._questLogExtraWindow)},Q.prototype.createQuestLogsDetailWindow=function(t){var e=this.questInfoWindowRect();this._questLogDetailWindow=new L(e,t),this._questLogDetailWindow.setHandler("ok",this.onQuestDetLogOk.bind(this)),this._questLogDetailWindow.setHandler("cancel",this.onQuestDetLogCancel.bind(this)),this.addWindow(this._questLogDetailWindow)},Q.prototype.onQuestLogs=function(){this._questLogExtraWindow?(this._questLogExtraWindow.reloadLogs(),this._questLogExtraWindow.open(),this._questLogExtraWindow.activate()):this.createQuestLogsExtraWindow()},Q.prototype.onQuestTrack=function(){var t=this._questInfoWindow.questItem.id;y(t,!this._questInfoWindow.checkIfTracked(t)),this._questInfoWindow.refreshCommands(),this._questInfoWindow.activate()},Q.prototype.onQuestInfoCancel=function(){this._questInfoWindow.select(-1),this._questInfoWindow.deactivate(),this._questListWindow.activate()},Q.prototype.onQuestLogOk=function(){var t=this._questLogExtraWindow._index;0<=t?this._questLogDetailWindow?(this._questLogDetailWindow.loadIndex(t),this._questLogDetailWindow.open(),this._questLogDetailWindow.activate()):this.createQuestLogsDetailWindow(t):this._questLogExtraWindow.activate()},Q.prototype.onQuestLogCancel=function(){this._questLogExtraWindow.close(),this._questInfoWindow.activate()},Q.prototype.onQuestDetLogOk=function(){this._questLogDetailWindow.activate()},Q.prototype.onQuestDetLogCancel=function(){this._questLogDetailWindow.close(),this._questLogExtraWindow.activate()},Q.prototype.onQuestListCancel=function(){this.popScene()},Q.prototype.needsCancelButton=function(){return D.layoutSettings.touchCancel},SceneManager.Scene_Quest=Q,((_.prototype=Object.create(Window_Base.prototype)).constructor=_).prototype.initialize=function(t){Window_Base.prototype.initialize.call(this,t);var t=window.WD_Interplugin_Core.realTextDimensions(this,D.textData.currentLanguage.questTitle,D.textSettings.fontSize),e=(this.innerWidth-t.width)/2,t=(this.innerHeight-t.height)/2;window.WD_Interplugin_Core.drawTextExSize(this,D.textData.currentLanguage.questTitle,e,t,this.innerWidth,D.textSettings.fontSize)},_.prototype.loadWindowskin=function(){this.windowskin=d()},_.prototype.updateTone=function(){var t=m();this.setTone(t[0],t[1],t[2])},((k.prototype=Object.create(Window_Selectable.prototype)).constructor=k).prototype.initialize=function(t){Window_Selectable.prototype.initialize.call(this,t),this.questArray=this.hardCopyAndTranslate(f.questsArray),this.sortedQuests=[],this.contents.fontSize=D.textSettings.listSize,0<this.questArray.length&&(this.sortQuests(),this.paint()),this.activate()},k.prototype.hardCopyAndTranslate=function(t){var e,t=JSON.parse(JSON.stringify(t)).filter(t=>!0!==t.hidden);for(const a of t)0<a.translationPacks.length&&(e={short:a.shortTitle,long:a.longTitle,giver:a.giver,area:a.area,desc:a.description,language:null},e=window.WD_Interplugin_Core.resolveLanguage(e,a.translationPacks))&&(a.shortTitle=e.short,a.longTitle=e.long,a.giver=e.giver,a.area=e.area,a.description=e.desc);return t},k.prototype.maxItems=function(){return this.sortedQuests.length},k.prototype.sortQuests=function(){let t=this.questArray.filter(t=>"ongoing"===t.status),e=this.questArray.filter(t=>"completed"===t.status),a=this.questArray.filter(t=>"failed"===t.status);if(t.sort(function(t,e){return t.index-e.index}),e.sort(function(t,e){return t.index-e.index}),a.sort(function(t,e){return t.index-e.index}),D.categoriesSettings.isActive){var s=D.categoriesSettings.categories;if(s.sort(function(t,e){return t.index-e.index}),0===D.categoriesSettings.displayType)for(const u of s){var i=this.questArray.filter(t=>t.categoryID===u.id);if(0<i.length){t=i.filter(t=>"ongoing"===t.status),e=i.filter(t=>"completed"===t.status),a=i.filter(t=>"failed"===t.status),t.sort(function(t,e){return t.index-e.index}),e.sort(function(t,e){return t.index-e.index}),a.sort(function(t,e){return t.index-e.index}),this.sortedQuests.push({isCategory:!0,questID:u.id,questStatus:null});for(const g of t)this.sortedQuests.push({isCategory:!1,questID:g.id,questStatus:"ongoing"});for(const l of e)this.sortedQuests.push({isCategory:!1,questID:l.id,questStatus:"completed"});for(const c of a)this.sortedQuests.push({isCategory:!1,questID:c.id,questStatus:"failed"})}}else{for(const h of s){var n=t.filter(t=>t.categoryID===h.id);if(0<n.length){this.sortedQuests.push({isCategory:!0,questID:h.id,questStatus:null}),n.sort(function(t,e){return t.index-e.index});for(const d of n)this.sortedQuests.push({isCategory:!1,questID:d.id,questStatus:"ongoing"})}}for(const p of s){var r=e.filter(t=>t.categoryID===p.id);if(0<r.length){this.sortedQuests.push({isCategory:!0,questID:p.id,questStatus:null}),r.sort(function(t,e){return t.index-e.index});for(const f of r)this.sortedQuests.push({isCategory:!1,questID:f.id,questStatus:"ongoing"})}}for(const m of s){var o=a.filter(t=>t.categoryID===m.id);if(0<o.length){this.sortedQuests.push({isCategory:!0,questID:m.id,questStatus:null}),o.sort(function(t,e){return t.index-e.index});for(const S of o)this.sortedQuests.push({isCategory:!1,questID:S.id,questStatus:"ongoing"})}}}}else{for(const y of t)this.sortedQuests.push({isCategory:!1,questID:y.id,questStatus:"ongoing"});for(const x of e)this.sortedQuests.push({isCategory:!1,questID:x.id,questStatus:"completed"});for(const w of a)this.sortedQuests.push({isCategory:!1,questID:w.id,questStatus:"failed"})}},k.prototype.paint=function(){this.contents&&(this.contents.clear(),this.contentsBack.clear(),this.drawAllItems(),D.categoriesSettings.isActive)&&this.drawStatics()},k.prototype.drawStatics=function(){var e=[];for(let t=0;t<this.sortedQuests.length;t++)this.sortedQuests[t].isCategory&&e.push({index:t,id:this.sortedQuests[t].questID});if(0<e.length)for(const o of e){var t=this.maxCols(),a=this.itemWidth(),s=this.itemHeight(),i=this.colSpacing(),n=this.rowSpacing(),r=o.index%t,t=Math.floor(o.index/t),r=r*a+i/2-this.scrollBaseX(),t=t*s+n/2-this.scrollBaseY(),n=a-i,a=this.getCategoryName(o.id);this.changePaintOpacity(!0),this.resetTextColor(),window.WD_Interplugin_Core.autoWrap(this,r,t,n,s,a,this.contents.fontSize,this.itemTextAlign()),this.resetQuestListFont()}},k.prototype.resetQuestListFont=function(t){this.resetFontSettings(),this.contents.fontSize=D.textSettings.listSize},k.prototype.getCategoryName=function(t){let e=null;for(const i of D.categoriesSettings.categories)if(i.id===t){e=i;break}e||(S(t,4),e=D.categoriesSettings.categories[0]);var a={categoryName:e.name,language:null},s=e.trans;return window.WD_Interplugin_Core.resolveLanguage(a,s).categoryName},k.prototype.drawItem=function(e){var t,a;this.sortedQuests[e].isCategory||(t=this.itemRect(e),1!==(a=this.questArray.filter(t=>t.id===this.sortedQuests[e].questID)).length&&S(this.sortedQuests[e],2),"completed"===(a=a[0]).status?(this.changePaintOpacity(!1),this.changeTextColor("#808080")):"ongoing"===a.status?(this.changePaintOpacity(!0),this.resetTextColor()):(this.changePaintOpacity(!1),this.changeTextColor("#B22222")),this.resetQuestListFont(),window.WD_Interplugin_Core.autoWrap(this,t.x,t.y,t.width,t.height,a.shortTitle,this.contents.fontSize,this.itemTextAlign()),this.resetQuestListFont())},k.prototype.itemRect=function(t){var e,a,s,i,n,r;return this.sortedQuests[t].isCategory?new Rectangle(-5e3,-5e3,0,0):(n=this.maxCols(),e=this.itemWidth(),a=this.itemHeight(),s=this.colSpacing(),i=this.rowSpacing(),r=t%n,t=Math.floor(t/n),n=r*e+s/2-this.scrollBaseX(),r=t*a+i/2-this.scrollBaseY(),new Rectangle(n,r,e-s,a-i))},k.prototype.itemTextAlign=function(){return D.textSettings.listAlign.toLowerCase()},k.prototype.callInfoWindow=function(e){var t;SceneManager._scene._questInfoWindow&&(-1===e||this.sortedQuests[e].isCategory?SceneManager._scene._questInfoWindow.eraseInfoes():(1!==(t=this.questArray.filter(t=>t.id===this.sortedQuests[e].questID)).length&&S(this.sortedQuests[e],2),SceneManager._scene._questInfoWindow.drawQuest(t[0])))};const W=k.prototype.select;function C(){this.initialize(...arguments)}function b(){this.initialize(...arguments)}function L(){this.initialize(...arguments)}k.prototype.select=function(t){W.call(this,t),0<=this.index()?this.callInfoWindow(this.index()):SceneManager._scene&&SceneManager._scene._questInfoWindow&&SceneManager._scene._questInfoWindow.eraseInfoes()},k.prototype.processCursorMove=function(){var t;this.isCursorMovable()&&(t=this.index(),Input.isRepeated("down")&&this.cursorDown(Input.isTriggered("down")),Input.isRepeated("up")&&this.cursorUp(Input.isTriggered("up")),Input.isRepeated("right")&&this.cursorRight(Input.isTriggered("right")),Input.isRepeated("left")&&this.cursorLeft(Input.isTriggered("left")),!this.isHandled("pagedown")&&Input.isTriggered("pagedown")&&this.cursorPagedown(),!this.isHandled("pageup")&&Input.isTriggered("pageup")&&this.cursorPageup(),this.index()!==t)&&(this.callInfoWindow(this.index()),this.playCursorSound())},k.prototype.cursorDown=function(t){var e,a,s;D.categoriesSettings.isActive?(e=this.checkNextIndex(!0),this.smoothSelect(e)):((e=this.index())<(a=this.maxItems())-(s=this.maxCols())||t&&1===s)&&this.smoothSelect((e+s)%a)},k.prototype.cursorUp=function(t){var e,a,s;D.categoriesSettings.isActive?(e=this.checkNextIndex(!1),this.smoothSelect(e)):(e=Math.max(0,this.index()),a=this.maxItems(),((s=this.maxCols())<=e||t&&1===s)&&this.smoothSelect((e-s+a)%a))},k.prototype.checkNextIndex=function(t){var e=this.index();if(0===this.sortedQuests.length)return-1;if(t){for(let t=e+1;t<this.sortedQuests.length;t++)if(!this.sortedQuests[t].isCategory)return t;this.scrollTo(0,0);for(let t=0;t<this.sortedQuests.length;t++)if(!this.sortedQuests[t].isCategory)return t}else{for(let t=e-1;0<=t;t--)if(!this.sortedQuests[t].isCategory)return t;for(let t=this.sortedQuests.length-1;0<=t;t--)if(!this.sortedQuests[t].isCategory)return t}},((C.prototype=Object.create(Window_HorzCommand.prototype)).constructor=C).prototype.initialize=function(t){Window_HorzCommand.prototype.initialize.call(this,t),this.select(-1),this.deactivate(),this.questItem=null,this.lineAdjust=0},C.prototype.processAllText=function(t){Window_Base.prototype.processAllText.call(this,t)},C.prototype.fixAlign=function(t){},C.prototype.actionCode_ALIGN=function(t,e){var a=Window_Base.prototype.actionCode_ALIGN;"function"==typeof a&&a.call(this,t,e)},C.prototype.makeCommandList=function(){var t;D.extraSettings.logs.isActive&&this.questItem&&this.addCommand(D.textData.currentLanguage.logText,"logs",!0),D.extraSettings.tracking.isActive&&D.extraSettings.tracking.allowPlayerTracking&&this.questItem&&this.questItem.trackData.isTrackable&&(t=this.checkIfTracked(this.questItem.id),this.addCommand(t?D.textData.currentLanguage.untrackText:D.textData.currentLanguage.trackText,"track",this.checkTrackEnabled(t)))},C.prototype.checkTrackEnabled=function(t){return!!this.questItem&&(!!t||D.extraSettings.tracking.currentlyTracked.length<D.extraSettings.tracking.trackingSettings.maxQuest)},C.prototype.checkIfTracked=function(e){if(0<D.extraSettings.tracking.currentlyTracked.length){let t=!1;for(const a of D.extraSettings.tracking.currentlyTracked)if(a.id===e){t=!0;break}return t}return!1},C.prototype.drawItem=function(t){var e=this.itemLineRect(t),a=this.itemTextAlign();this.resetTextColor(),this.changePaintOpacity(this.isCommandEnabled(t)),this.drawText(this.commandName(t),e.x,e.y,e.width,a)},C.prototype.itemLineRect=function(t){return this.specialRect(t)},C.prototype.itemRect=function(t){return this.specialRect(t)},C.prototype.specialRect=function(t){var e=this.commandsOnScreenCount(),a=0<e?.15*c("totalWidth"):0,e=0<e?.1*c("totalHeight"):0,s=this.innerHeight-e-12;return new Rectangle(1===t?24+a:12,s,a,e)},C.prototype.commandsOnScreenCount=function(){let t=0;return D.extraSettings.logs.isActive&&t++,D.extraSettings.tracking.isActive&&D.extraSettings.tracking.allowPlayerTracking&&t++,t},C.prototype.loadWindowskin=function(){this.windowskin=d()},C.prototype.updateTone=function(){var t=m();this.setTone(t[0],t[1],t[2])},C.prototype.eraseInfoes=function(){null!==this.questItem&&(this.contents.clear(),this.lineAdjust=0,this.questItem=null,this.refresh())},C.prototype.drawQuest=function(t){this.questItem!==t&&(this.contents.clear(),this.lineAdjust=0,this.questItem=t,this.refresh(),this.resetFontSettings(),this.drawQuestIcon(this.questItem.icon),this.drawQuestName(this.questItem.shortTitle,this.questItem.longTitle),this.drawQuestGiver(this.questItem.giver),this.drawQuestArea(this.questItem.area),this.drawQuestInfo(this.questItem.description),this.drawQuestStatus(this.questItem.status))},C.prototype.refreshCommands=function(){this.contents.clear(),this.lineAdjust=0,this.refresh(),this.resetFontSettings(),this.drawQuestIcon(this.questItem.icon),this.drawQuestName(this.questItem.shortTitle,this.questItem.longTitle),this.drawQuestGiver(this.questItem.giver),this.drawQuestArea(this.questItem.area),this.drawQuestInfo(this.questItem.description),this.drawQuestStatus(this.questItem.status)},C.prototype.drawQuestIcon=function(t){var e=(this.innerWidth-ImageManager.iconWidth)/2;this.drawIcon(t,e,10)},C.prototype.drawQuestName=function(t,e){var a=1.5*this.lineHeight(),s=this.innerWidth,e=e||t;window.WD_Interplugin_Core.autoWrap(this,0,a,s,1.2*this.lineHeight(),e,this.contents.fontSize,"center"),this.resetFontSettings()},C.prototype.drawQuestGiver=function(t){var e,a,s;t?(e=3*this.lineHeight(),a=this.innerWidth,s=D.textData.currentLanguage.giverPrefix,this.drawText(s?s+" "+t:t,0,e,a,"left")):this.lineAdjust--},C.prototype.drawQuestArea=function(t){var e,a,s;t?(e=this.lineHeight()*(4+this.lineAdjust),a=this.innerWidth,s=D.textData.currentLanguage.areaPrefix,this.drawText(s?s+" "+t:t,0,e,a,"left")):this.lineAdjust--},C.prototype.drawQuestInfo=function(t){var e=this.lineHeight()*(6+this.lineAdjust),a=this.questItem.status?2*this.lineHeight():0,s=this.innerWidth,i=Math.max(0,this.innerHeight-e-a),n=D.textSettings.infoAlign,r=this.prepInfoText(t,n),o=D.textSettings.descriptionSize;switch(D.textSettings.textManagement){case"wrap":window.WD_Interplugin_Core.autoWrap(this,0,e,s,i,t,o,n);break;case"size":this.contents.fontSize=o;var u=window.WD_Interplugin_Core.autoTextSize(this,r,s,i);window.WD_Interplugin_Core.drawTextExSize(this,r,0,e,s,u);break;case"manual":this.contents.fontSize=o,window.WD_Interplugin_Core.drawTextExSize(this,r,0,e,s,o);break;default:S(D.textSettings.textManagement,3)}this.resetFontSettings()},C.prototype.prepInfoText=function(t,e){return window.WD_Interplugin_Core.improvedTextExAligner(this,t,e)},C.prototype.drawQuestStatus=function(t){var e=this.lineHeight()*c("MaxLines"),a=this.innerWidth;let s;var i=D.textData.currentLanguage.statusName;switch(t){case"ongoing":s=i?i+" "+D.textData.currentLanguage.questOngoing:D.textData.currentLanguage.questOngoing;break;case"completed":s=i?i+" "+D.textData.currentLanguage.questCompleted:D.textData.currentLanguage.questCompleted;break;case"failed":s=i?i+" "+D.textData.currentLanguage.questFailed:D.textData.currentLanguage.questFailed}""!==s&&" "!==s&&this.drawText(s,0,e,a,"right")},((b.prototype=Object.create(Window_Selectable.prototype)).constructor=b).prototype.initialize=function(t){Window_Selectable.prototype.initialize.call(this,t),this.visibleLogs=this.getVisibleLogsArray(),this.paint(),0<this.visibleLogs.length&&this.select(0),this.activate()},b.prototype.reloadLogs=function(){this.visibleLogs=this.getVisibleLogsArray(),this.select(0<this.visibleLogs.length?0:-1),this.refresh()},b.prototype.getVisibleLogsArray=function(){return SceneManager._scene._questInfoWindow.questItem.logs.filter(t=>t.isVisible)},b.prototype.maxItems=function(){return this.visibleLogs.length},b.prototype.drawItem=function(t){var e=this.itemRect(t),t=this.getLogTitleTrans(this.visibleLogs[t].title);window.WD_Interplugin_Core.autoWrap(this,e.x,e.y,e.width,e.height,t,this.contents.fontSize,"left"),this.resetFontSettings()},b.prototype.getLogTitleTrans=function(t){var e,a=t.default,t=t.trans;return t&&0!==t.length?(t=t,e={logTitle:a,language:null},window.WD_Interplugin_Core.resolveLanguage(e,t).logTitle):a},((L.prototype=Object.create(Window_Selectable.prototype)).constructor=L).prototype.initialize=function(t,e){Window_Selectable.prototype.initialize.call(this,t),this.currentIndex=e,this.currentLogData=this.getLogData(e),this.drawLog(),this.activate()},L.prototype.getLogData=function(t){return SceneManager._scene._questLogExtraWindow.visibleLogs[t]},L.prototype.maxItems=function(){return 0},L.prototype.clearResidualLogPic=function(){let t=null;for(const e of this.children)if(e.hasOwnProperty("isWdLogSprite")){t=e;break}t&&this.removeChild(t)},L.prototype.drawLog=function(){this.contents&&(this.contents.clear(),this.contentsBack.clear(),this.clearResidualLogPic());let e=0;const a={isNeeded:!1,imageBitmap:void 0};switch(this.currentLogData.graphics.style){case"no":break;case"icon":e=24+ImageManager.iconHeight;break;case"face":e=24+ImageManager.faceHeight;break;case"char":a.isNeeded=!0,a.imageBitmap=ImageManager.loadCharacter(this.currentLogData.graphics.character.id);break;case"pic":a.isNeeded=!0,a.imageBitmap=ImageManager.loadPicture(this.currentLogData.graphics.picture.id);break;default:throw new Error("WD_Quest: Unexpected value for graphic style: "+this.currentLogData.graphics.style)}a.isNeeded?a.imageBitmap.addLoadListener(()=>{var t;e="pic"===this.currentLogData.graphics.style?(t=this.currentLogData.graphics.picture.scale/100,24+a.imageBitmap.height*t):(t=ImageManager.isBigCharacter(this.currentLogData.graphics.character.id),24+a.imageBitmap.height/(t?4:8)),this.drawLogStepTwo(e)}):this.drawLogStepTwo(e)},L.prototype.drawLogStepTwo=function(t){var e;switch(this.currentLogData.text.showText&&(e=this.getTranslatedLogBodyText(this.currentLogData.text.data,this.currentLogData.text.transData),window.WD_Interplugin_Core.autoWrap(this,0,"above"===this.currentLogData.graphics.placement?t:0,this.innerWidth,this.innerHeight-t,e,this.contents.fontSize,this.currentLogData.text.align),this.resetFontSettings()),this.currentLogData.graphics.style){case"no":break;case"icon":var a=(this.innerWidth-ImageManager.iconWidth)/2,s="above"===this.currentLogData.graphics.placement?12:this.innerHeight-24-ImageManager.iconHeight;this.drawIcon(this.currentLogData.graphics.icon.id,a,s);break;case"face":ImageManager.loadFace(this.currentLogData.graphics.face.id).addLoadListener(()=>{var t=(this.innerWidth-ImageManager.faceWidth)/2,e="above"===this.currentLogData.graphics.placement?12:this.innerHeight-24-ImageManager.faceHeight;this.drawFace(this.currentLogData.graphics.face.id,this.currentLogData.graphics.face.index,t,e,ImageManager.faceWidth,ImageManager.faceHeight)});break;case"char":const i=ImageManager.loadCharacter(this.currentLogData.graphics.character.id);i.addLoadListener(()=>{var t=ImageManager.isBigCharacter(this.currentLogData.graphics.character.id),e=i.width/(t?3:12),t=i.height/(t?4:8),e=(this.innerWidth-e/2)/2,t="above"===this.currentLogData.graphics.placement?12+t:this.innerHeight-24;this.drawCharacter(this.currentLogData.graphics.character.id,this.currentLogData.graphics.character.index,e,t)});break;case"pic":const n=new Sprite,r=this.currentLogData.graphics.picture.scale/100;n.bitmap=ImageManager.loadPicture(this.currentLogData.graphics.picture.id),n.isWdLogSprite=!0,n.scale.set(r),n.bitmap.addLoadListener(()=>{n.x=(this.width-n.width*r)/2,n.y="above"===this.currentLogData.graphics.placement?12:this.innerHeight-24-n.height*r}),this.addChild(n);break;default:throw new Error("WD_Quest: Unexpected value for graphic style: "+this.currentLogData.graphics.style)}},L.prototype.getTranslatedLogBodyText=function(t,e){return 0===e.length?t:window.WD_Interplugin_Core.resolveLanguage({textData:t,language:null},e).textData},L.prototype.loadIndex=function(t){this.currentIndex=t,this.currentLogData=this.getLogData(t),this.drawLog()},L.prototype.cursorRight=function(t){this.searchNewIndex(!0)},L.prototype.cursorLeft=function(t){this.searchNewIndex(!1)},L.prototype.searchNewIndex=function(t){var e=SceneManager._scene._questLogExtraWindow.visibleLogs.length-1,a=this.currentIndex,t=t?a+1:a-1;e<t?this.loadIndex(0):t<0?this.loadIndex(e):this.loadIndex(t)},L.prototype.isCursorMovable=function(){return this.isOpenAndActive()&&!this._cursorFixed&&!this._cursorAll},PluginManager.registerCommand("WD_Quest","newCreateQuest",function(t){var e=parseInt(t.id),a=parseInt(t.icon),s=parseInt(t.index),i=parseInt(t.cat),n=JSON.parse(t.questTrans).map(t=>JSON.parse(t));if(isNaN(e)||isNaN(a)||isNaN(s)||isNaN(i))throw new Error("WD_Quest: ID, icon, index and / or category ID are not a number");f.loadQuests(),f.addQuest(!1,e,a,t.short,t.long,s,t.giver,t.area,t.desc,t.status,t.track,t.logs,n,i),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","newSetTitle",function(t){var e=t.title??"",t=l(t.transTitle);D.updateLanguageTerms("questTitle",!0,e),0<t.length&&D.updateLanguageTerms("questTitle",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetGiverPrefix",function(t){var e=t.prefix??"",t=l(t.transPrefix);D.updateLanguageTerms("giverPrefix",!0,e),0<t.length&&D.updateLanguageTerms("giverPrefix",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetAreaPrefix",function(t){var e=t.prefix??"",t=l(t.transPrefix);D.updateLanguageTerms("areaPrefix",!0,e),0<t.length&&D.updateLanguageTerms("areaPrefix",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetStatusName",function(t){var e=t.name??"",t=l(t.transName);D.updateLanguageTerms("statusName",!0,e),0<t.length&&D.updateLanguageTerms("statusName",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetQuestCompleted",function(t){var e=t.completed??"",t=l(t.transCompleted);D.updateLanguageTerms("questCompleted",!0,e),0<t.length&&D.updateLanguageTerms("questCompleted",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetQuestOngoing",function(t){var e=t.ongoing??"",t=l(t.transOngoing);D.updateLanguageTerms("questOngoing",!0,e),0<t.length&&D.updateLanguageTerms("questOngoing",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetQuestFailed",function(t){var e=t.failed??"",t=l(t.transFailed);D.updateLanguageTerms("questFailed",!0,e),0<t.length&&D.updateLanguageTerms("questFailed",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","newSetCommandName",function(t){var e=t.commandName??"",t=l(t.transCommandName);D.updateLanguageTerms("questMenuCommandName",!0,e),0<t.length&&D.updateLanguageTerms("questMenuCommandName",!1,t),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","OpenQuestScene",function(){SceneManager.push(Q)}),PluginManager.registerCommand("WD_Quest","SetQuestTitleFontSize",function(t){t=parseInt(t.fontSize);isNaN(t)||(D.textSettings.fontSize=t,D.saveSettings())}),PluginManager.registerCommand("WD_Quest","SetQuestInfoFontSize",function(t){t=parseInt(t.fontSize);isNaN(t)||(D.textSettings.descriptionSize=t,D.saveSettings())}),PluginManager.registerCommand("WD_Quest","SetQuestListFontSize",function(t){t=parseInt(t.fontSize);isNaN(t)||(D.textSettings.listSize=t,D.saveSettings())}),PluginManager.registerCommand("WD_Quest","editQuestDescriptors",function(t){var e=parseInt(t.questID),a=t.questName,s=parseInt(t.icon),i=parseInt(t.cat),n=t.short,r=t.long,o=t.giver,u=t.area,g=t.desc,t=JSON.parse(t.questTrans).map(t=>JSON.parse(t));let l=null;f.loadQuests();for(const d of f.questsArray)if(!isNaN(e)&&0<e&&d.id===e||""!==a&&d.shortTitle===a){l=d;break}if(l&&(!isNaN(s)&&0<s&&(l.icon=s),!isNaN(i)&&-1<i&&(l.categoryID=i),n&&""!==n&&(l.shortTitle=n),r&&""!==r&&(l.longTitle=r),o&&""!==o&&(l.giver=o),u&&""!==u&&(l.area=u),g&&""!==g&&(l.description=g),0<t.length))for(const p of t){var c=p.language,h={found:!1,index:0};for(let t=0;t<l.translationPacks.length;t++)if(l.translationPacks[t].language===c){h.found=!0,h.index=t;break}h.found&&(p.short&&""!==p.short&&(l.translationPacks[h.index].shortTitle=p.short),p.long&&""!==p.long&&(l.translationPacks[h.index].longTitle=p.long),p.giver&&""!==p.giver&&(l.translationPacks[h.index].giver=p.giver),p.area&&""!==p.area&&(l.translationPacks[h.index].area=p.area),p.desc)&&""!==p.desc&&(l.translationPacks[h.index].description=p.desc)}f.saveQuests()}),PluginManager.registerCommand("WD_Quest","SetCompletion",function(t){var e=parseInt(t.questID),a=String(t.questName);let s=t.status,i=null;void 0!==t.completion&&(s=s||("true"===t.completion?"completed":"ongoing")),f.loadQuests();for(const n of f.questsArray)if(!isNaN(e)&&0<e&&n.id===e||""!==a&&n.shortTitle===a){i=n;break}i&&(i.status=s,f.saveQuests(),"ongoing"!==s)&&D.extraSettings.tracking.isActive&&(y(i.id,!1),u=!0,$gameMap.requestRefresh())}),PluginManager.registerCommand("WD_Quest","RemoveQuestNew",function(t){var e=Number(t.questID),t=String(t.questName);f.loadQuests(),f.removeQuest(e,t),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","hideShowQuest",function(t){var e=Number(t.questID),a=String(t.questName),s=t.showFlag;let i=null;f.loadQuests();for(const r of f.questsArray)if(!isNaN(e)&&0<e&&r.id===e||""!==a&&r.shortTitle===a){i=r;break}if(i)switch(s){case"show":i.hidden=!1;break;case"hide":i.hidden=!0;break;case"toggle":var n=i.hidden;i.hidden=null==n||!n;break;default:throw new Error("WD_Quest: Unexpected argument for Hide Show Quest: "+s)}f.saveQuests()}),PluginManager.registerCommand("WD_Quest","CheckQuestCompletion",function(e){var t=parseInt(e.questID),a=String(e.questName),s=parseInt(e.switchID),e=String(e.selectMode);let i=null;f.loadQuests();for(const n of f.questsArray)if(!isNaN(t)&&0<t&&n.id===t||""!==a&&n.shortTitle===a){i=n;break}if(i){let t=null;if(t=i.hasOwnProperty("complete")&&!i.hasOwnProperty("status")?i.complete?"completed":"ongoing":i.status,"Variable"===e)switch(t){case"completed":$gameVariables.setValue(s,0);break;case"ongoing":$gameVariables.setValue(s,1);break;case"failed":$gameVariables.setValue(s,2)}else"completed"===t?$gameSwitches.setValue(s,!0):$gameSwitches.setValue(s,!1)}}),PluginManager.registerCommand("WD_Quest","changeGraphics",function(t){var e=t.titleFlag,a=t.layoutAlign,s=t.layoutSize,i=t.touchCancel,n=function(t){t=JSON.parse(t);return t.redT=parseInt(t.redT),t.greenT=parseInt(t.greenT),t.blueT=parseInt(t.blueT),t}(t.skinSettings);switch(D.loadSettings(),e){case"title1":D.layoutSettings.titleFlag=!0;break;case"title2":D.layoutSettings.titleFlag=!1}switch(a){case"layout1":case"layout2":D.layoutSettings.layoutAlign=a}switch(s){case"size1":case"size2":D.layoutSettings.layoutSize=s}switch(i){case"cancel1":D.layoutSettings.touchCancel=!0;break;case"cancel2":D.layoutSettings.touchCancel=!1}switch(n.skinFlag){case"skin1":D.layoutSettings.skinSettings.skinFlag=!0,D.layoutSettings.skinSettings.skinName=n.skinName,D.layoutSettings.skinSettings.redT=n.redT,D.layoutSettings.skinSettings.greenT=n.greenT,D.layoutSettings.skinSettings.blueT=n.blueT;break;case"skin2":D.layoutSettings.skinSettings.skinFlag=!1}D.saveSettings()}),PluginManager.registerCommand("WD_Quest","activateLog",function(t){var e=parseInt(t.questID),a=String(t.questName),s=t.logID,i="true"===t.visibleFlag;let n=null;f.loadQuests();for(const r of f.questsArray)if(!isNaN(e)&&0<e&&r.id===e||""!==a&&r.shortTitle===a){n=r;break}if(n){for(const o of n.logs)if(o.id===s){o.isVisible=i;break}f.saveQuests()}}),PluginManager.registerCommand("WD_Quest","addLog",function(e){var t=parseInt(e.questID),a=String(e.questName),s=e.logSettings;let i=null;f.loadQuests();for(const r of f.questsArray)if(!isNaN(t)&&0<t&&r.id===t||""!==a&&r.shortTitle===a){i=r;break}if(i){(s=JSON.parse(s)).isVisible="true"===s.isVisible,s.textStyle="true"===s.textStyle,s.charSpecial="true"===s.charSpecial,s.charIndex=parseInt(s.charIndex),s.faceIndex=parseInt(s.faceIndex),s.iconID=parseInt(s.iconID),s.picScale=parseInt(s.picScale),s.textDataTrans=JSON.parse(s.textDataTrans);for(let t=0;t<s.textDataTrans.length;t++)s.textDataTrans[t]=JSON.parse(s.textDataTrans[t]);s.logTitleTrans=JSON.parse(s.logTitleTrans);for(let t=0;t<s.logTitleTrans.length;t++)s.logTitleTrans[t]=JSON.parse(s.logTitleTrans[t]);var e=s,n={id:e.logID,isVisible:e.isVisible,graphics:{style:e.graphStyle,align:e.graphAlign,placement:e.graphPlacement,icon:{id:e.iconID},face:{id:e.faceID,index:e.faceIndex},character:{id:e.charID,index:e.charIndex,isSpecial:e.charSpecial},picture:{id:e.picID,scale:e.picScale}},text:{showText:e.textStyle,align:e.textAlign,data:e.textData,transData:e.textDataTrans},title:{default:e.logTitle,trans:e.logTitleTrans}};let t=!1;for(const o of i.logs)if(o.id===n.id){t=!0;break}t?S(n.id,6):i.logs.push(n),f.saveQuests()}}),PluginManager.registerCommand("WD_Quest","removeLog",function(t){var e=parseInt(t.questID),a=String(t.questName),s=t.logID;let i=null;f.loadQuests();for(const r of f.questsArray)if(!isNaN(e)&&0<e&&r.id===e||""!==a&&r.shortTitle===a){i=r;break}if(i){var n={found:!1,index:0};for(let t=0;t<i.logs.length;t++)if(i.logs[t].id===s){n.found=!0,n.index=t;break}n.found&&(i.logs.splice(n.index,1),f.saveQuests())}}),PluginManager.registerCommand("WD_Quest","enableTracking",function(t){var t="true"===t.trackingFlag,e=(D.loadSettings(),D.extraSettings.tracking.isActive=t,D.saveSettings(),SceneManager._scene);e instanceof Scene_Map&&(t&&e.wdQuestCreateTrackingHud(),e._wdQuestHud)&&e._wdQuestHud.updateText()}),PluginManager.registerCommand("WD_Quest","enablePlayerTracking",function(t){var e="true"===t.trackingFlag,t="true"===t.wipeFlag;D.loadSettings(),D.extraSettings.tracking.allowPlayerTracking=e,t&&0<D.extraSettings.tracking.currentlyTracked.length&&(D.extraSettings.tracking.currentlyTracked.length=0,u=!0,$gameMap.requestRefresh()),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","addRemoveTracking",function(t){var e="true"===t.addFlag,a=parseInt(t.questID),s=t.questName;let i=null;f.loadQuests();for(const n of f.questsArray)if(!isNaN(a)&&0<a&&n.id===a||""!==s&&n.shortTitle===s){i=n;break}i&&(D.loadSettings(),y(i.id,e),D.saveSettings(),u=!0,$gameMap.requestRefresh())}),PluginManager.registerCommand("WD_Quest","changeTrackingText",function(t){var e=parseInt(t.questID),a=t.questName,s=t.text,t=JSON.parse(t.textTrans).map(t=>JSON.parse(t));let i=null;f.loadQuests();for(const n of f.questsArray)if(!isNaN(e)&&0<e&&n.id===e||""!==a&&n.shortTitle===a){i=n;break}if(i&&(i.trackData.trackText=s,i.trackData.trackTextTranslations=t,f.saveQuests(),D.extraSettings.tracking.isActive)){let t=!1;for(const r of D.extraSettings.tracking.currentlyTracked)if(r.id===i.id){t=!0;break}t&&(y(i.id,!1),u=!0,$gameMap.requestRefresh(),y(i.id,!0),u=!0,$gameMap.requestRefresh())}}),PluginManager.registerCommand("WD_Quest","storeQuests",function(t){var e=t.storeID,t="true"===t.wipe;o.saveCurrentAsStorage(e,t)}),PluginManager.registerCommand("WD_Quest","recoverStore",function(t){var e=t.storeID,t="true"===t.onError;o.loadStorageFromId(e,t)}),PluginManager.registerCommand("WD_Quest","checkExistingQuest",function(t){var e=parseInt(t.questID),a=t.questName,t=parseInt(t.switchID);let s=null;f.loadQuests();for(const i of f.questsArray)if(!isNaN(e)&&0<e&&i.id===e||""!==a&&i.shortTitle===a){s=i;break}s?!isNaN(t)&&0<t&&$gameSwitches.setValue(t,!0):!isNaN(t)&&0<t&&$gameSwitches.setValue(t,!1)}),PluginManager.registerCommand("WD_Quest","CreateQuest",function(t){let e=t.status;void 0!==t.complete&&(e="true"===t.complete?"completed":"ongoing");t={id:Number(t.id),icon:Number(t.icon),name:t.name?String(t.name):"",longTitle:t.longTitle?String(t.longTitle):"",index:Number(t.index),giver:t.giver?String(t.giver):"",area:t.area?String(t.area):"",description:t.description?String(t.description):"",status:String(e)};f.loadQuests(),f.addQuest(!0,t.id,t.icon,t.name,t.longTitle,t.index,t.giver,t.area,t.description,t.status,null,null,[],0),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","SetTitle",function(t){D.updateLanguageTerms("questTitle",!0,t.title),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetGiverPrefix",function(t){D.updateLanguageTerms("giverPrefix",!0,t.prefix),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetAreaPrefix",function(t){D.updateLanguageTerms("areaPrefix",!0,t.title),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetStatusName",function(t){D.updateLanguageTerms("statusName",!0,t.name),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetQuestCompleted",function(t){D.updateLanguageTerms("questCompleted",!0,t.completed),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetQuestOngoing",function(t){D.updateLanguageTerms("questOngoing",!0,t.ongoing),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","EditQuestDescription",function(t){var e=parseInt(t.questID),a=String(t.questName),t=String(t.newDescription);let s=null;f.loadQuests();for(const i of f.questsArray)if(!isNaN(e)&&0<e&&i.id===e||""!==a&&i.shortTitle===a){s=i;break}s&&(s.description=t),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","EditQuestIcon",function(t){var e=Number(t.questID),a=String(t.questName),t=Number(t.iconID);f.loadQuests();for(const s of f.questsArray)if(!isNaN(e)&&0<e&&s.id===e||""!==a&&s.shortTitle===a){questObj=s;break}questObj&&(questObj.icon=t),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","SetCommandName",function(t){D.updateLanguageTerms("questMenuCommandName",!0,t.commandName),D.saveSettings()}),PluginManager.registerCommand("WD_Quest","SetCompletionByName",function(t){var e=t.questName,t="true"===t.completion?"completed":"ongoing";let a=null;f.loadQuests();for(const s of f.questsArray)if(isNaN(0),""!==e&&s.shortTitle===e){a=s;break}a&&(a.status=t,f.saveQuests())}),PluginManager.registerCommand("WD_Quest","SetCompletionByID",function(t){var e=parseInt(t.questID),t="true"===t.completion?"completed":"ongoing";let a=null;f.loadQuests();for(const s of f.questsArray)if(!isNaN(e)&&0<e&&s.id===e){a=s;break}a&&(a.status=t,f.saveQuests())}),PluginManager.registerCommand("WD_Quest","RemoveQuestByID",function(t){t=Number(t.questID);f.loadQuests(),f.removeQuest(t,""),f.saveQuests()}),PluginManager.registerCommand("WD_Quest","RemoveQuest",function(t){t=t.questName;f.loadQuests(),f.removeQuest(0,t),f.saveQuests()});const N=Game_System.prototype.initialize,A=(Game_System.prototype.initialize=function(){N.call(this),this.initWinterDreamQuestParams()},Game_System.prototype.initWinterDreamQuestParams=function(){this._questPluginParams=null,this._questList=null,this._savedWdQuestSettings=null,this._questContainer=null,this._questStorage=null},Game_System.prototype.wdQuestContainer=function(){return this._questContainer||(this._questContainer=new a),this._questContainer},Game_System.prototype.wdQuestSettings=function(){return this._questPluginParams||(this._questPluginParams=new s),this._questPluginParams},DataManager.setupNewGame),O=(DataManager.setupNewGame=function(){A.call(this),g()},DataManager.extractSaveContents);function z(){$gameSystem.saveQuestContainer(f)}function F(){var t=$gameSystem.getQuestContainer();null!==t&&(f.compatibilityLoad=t.compatibilityLoad,f.questsArray=t.questsArray)}function H(){$gameSystem.saveQuestStorage(o)}function M(){var t=$gameSystem.getQuestStorage();null!==t&&(o.storage=t.storage)}function E(t){t=JSON.parse(JSON.stringify(t));$gameSystem.saveWdQuestPluginSettings(t)}function J(){var t=$gameSystem.getWdQuestPluginSettings();null!==t&&(t=JSON.parse(JSON.stringify(t)),D.textData=t.textData,D.textSettings=t.textSettings,D.layoutSettings=t.layoutSettings,D.categoriesSettings=t.categoriesSettings,D.compatibilityLoad=t.compatibilityLoad,D.extraSettings=t.extraSettings,D.errorManagement=t.errorManagement)}function R(){return $gameSystem.getQuestList()}function G(){return $gameSystem.getPluginParams()}function P(t,e){var a=parseInt(t),s=String(e);let i=null;f.loadQuests();for(const quest of f.questsArray)if(!isNaN(a)&&0<a&&quest.id===a||""!==s&&quest.shortTitle===s){i=quest;break}if(i){let t=null;return"completed"===(t=i.hasOwnProperty("complete")&&!i.hasOwnProperty("status")?quest.complete?"completed":"ongoing":quest.status)}return!1}DataManager.extractSaveContents=function(t){O.call(this,t),g()},Game_System.prototype.saveQuestContainer=function(t){this._questContainer=t},Game_System.prototype.getQuestContainer=function(){return this._questContainer||null},Game_System.prototype.saveQuestStorage=function(t){this._questStorage=t},Game_System.prototype.getQuestStorage=function(){return this._questStorage||null},Game_System.prototype.saveWdQuestPluginSettings=function(t){this._savedWdQuestSettings=t},Game_System.prototype.getWdQuestPluginSettings=function(){return this._savedWdQuestSettings||null},Game_System.prototype.getQuestList=function(){return this._questList||[]},Game_System.prototype.getPluginParams=function(){return this._questPluginParams||null},window.WD_Interplugin_Quest={checkCompletionID:function(t){return P(t,"")},checkCompletionName:function(t){return P(0,t)}}}();