# Averis — Artisan System v0.2.0 (Foundry v14 preview)

**Development preview, not production-ready.** Target: Foundry VTT v14, D&D 5e 5.3.3. English UI, dark fantasy/gold. Do not enable in your only copy of a live campaign. No Foundry runtime was available to run integration tests. Nine pure JavaScript rule/catalog tests passed; this does not verify the Foundry APIs, sheet hooks, or D&D item schema.

## Install via Foundry Manifest URL

In Setup → Add-on Modules → Install Module, paste:

```text
https://raw.githubusercontent.com/Daikaze/Crafting/v14/module.json
```

Versioned source archive: https://github.com/Daikaze/Crafting/archive/refs/heads/v0.1.1-v14.zip. Install in a test world first. Remote installation has not been runtime-tested.

## Install locally
1. Back up your world. Stop Foundry. Extract the `averis-artisan-system` folder into your Foundry User Data `Data/modules/` directory. On a typical Windows default install this is `%LOCALAPPDATA%/FoundryVTT/Data/modules/`, but check your actual User Data path.
2. Start a **test copy** of your world using Foundry v13 and dnd5e 5.3.3. Enable **Averis — Artisan System** from Manage Modules. Refresh after enabling.
3. As GM, open **Artisan GM** in scene controls if available. A fallback **Script** macro (works independently of the sheet/control hooks once the module initializes):

```js
game.modules.get("averis-artisan-system")?.api?.openGM();
```

Player/selected actor fallback Script macro:

```js
const actor = canvas.tokens.controlled[0]?.actor ?? game.user.character;
game.modules.get("averis-artisan-system")?.api?.openActor(actor);
```

If neither opens, open F12 > Console and look for `averis-artisan-system` errors. Check that the module is enabled and the GM is active.

## First test: Stormforged Blade

- GM → **Actors**: select an owned test actor. Assign 240+ minutes of downtime, grant Forge workshop access and save. Confirm Smith's Tools proficiency on the actual actor sheet.
- GM → **Recipes**: find `Stormforged Blade`, click Unlock for actor. Link a correctly configured D&D Item using its UUID (from the item sheet or compendium). The result is copied from that template, **not** automatically given a Storm Ore damage activity. Configure the linked item yourself in this preview.
- GM → **Compendiums**: create materials pack, verify its visibility, then drag 2 Iron Ore and 1 Storm Ore into actor inventory (adjust quantities). Give the actor at least 15 GP. Or use existing matching items/links.
- Player: use actor macro, choose Recipes → Stormforged Blade → Start Crafting. Under Projects, add 4 hours, then Crafting Check. The GM resolves which materials are lost on failure. Cancel a different test project to check material returns.
- GM → Regions: Seed Journal Regions or create a region and add resource patches. Set its in-game day; assign a region to the actor under Actors. Gather from that region. Advance day manually to test regrowth.
- All new actors start with zero unlocked recipes, zero downtime, and no workshop access. Unlock content manually.

## Implemented in the preview

- Parsed 267 recipes: 160 Hybrid Crafting (including 24 rune recipes), 48 Enchanting, 59 Cooking. 171 unique materials (72 field resources + 12 ores + 87 pantry ingredients), 84 gathering/mining records. Source requirements and descriptions retained in `data/catalog.json`. The four input journals are not modified.
- Player overview, recipe list and detail panes, gathering, inventory materials, recipe scrolls, prepared meals, projects, history, NPC order list. GM dashboard, request queue, recipe editor (basic form), actor settings, regions, workshops, projects, NPC orders, and catalog import/export.
- Recipe unlock/revoke, scroll creation and learning, proficiency/workshop checks, manual work time, one active project, pause/resume/cancel, material escrow, gold payment, outcome resolution, Smart Approval, GM-assigned regions, shared patch depletion and day-based regrowth. GM-only private Journal is authoritative; actor views are derived from it, and requests are validated in a serialized primary-GM queue. A connected GM is required for player actions.
- Cooking creates servings as inventory items. Eating consumes one serving, spends 10 minutes from the actor's budget and records the meal benefit. Basic temporary HP and a descriptive timed Active Effect are implemented; conditional meal bonuses are manual. Temporary HP cleanup and rest hook must be tested, and no existing temporary HP is automatically removed on timer expiry to avoid deleting HP from unrelated sources.
- Enchanting and rune engraving record an occupied slot and append the effect text to the existing item. **No automatic combat effect is applied yet**. Item eligibility checks are broad and need stricter D&D schema verification. Attunement and active-pair enforcement are future work. Do not use on valuable live items.
- NPC equipment/Alchemy orders with player-supplied materials, configurable fee and capacity, GM progress, NPC roll/guaranteed success, collection. Failure returns materials; this is a preview decision. NPC-supplied materials, training, cancellation and item-modification services are not implemented.
- World Item compendiums for material and scroll templates are created by GM command, not prebuilt module database packs. Output weapons/armor/potions/tools are linked manually to existing Items; prepared food is generated automatically. Verify world pack permissions before giving access.

## Decisions and limitations to review

- For gathering, Field Guide rules are used in preference to the contradictory old herbalism rules, and creature yields remain one by default. Current search/harvest uses Survival; other skills, tool selection, assistance, seasons/hazards and specific harvesting times are not fully automated. GM can adjust patches manually. Rare searches and mining require Smart Approval; Very Rare regions should be configured by GM.
- Missing required tool proficiency blocks crafting; Arcana requirements are checked directly on the actor. Assistant/Help logic is not implemented. Manual project time doesn't advance the Foundry world clock. Resource day is manually managed separately; no calendar integration yet.
- Cooking partial failure consumes the entire batch ingredients (not explicitly quantified by the source); severe failure consumes half, rounded up. Cooking is classified Common for approval/filtering only; actual difficulty uses source DC. Some recipes may require a specific kitchen or different ability; edit recipe fields to suit. NPC fee payment is spent, not credited to a separate merchant cashbox. Some special recipes need hand verification before use.
- Unknown recipes and DCs are withheld in the normal player UI, but the shipped catalog is a static module asset and is **not confidential against a player inspecting the module files**. Do not add private story content to the distributed catalog. Actor owners can also alter their displayed actor flags; the GM database remains authoritative. The preview has not been security-audited.
- No multi-document transactional rollback or recovery journal for interrupted writes yet; operation queue reduces simultaneous requests, but crashes or manual inventory/target edits can still cause inconsistency. Use only a test world. Item flags do not enforce non-transferability of reserved enchantment targets.
- Deferred: actual native combat Activities for all 160 crafted items, 48 enchantments and 24 runes, Midi-QOL/DAE integrations, complete item-slot tab, full stacking and attunement enforcement, automatic recipe experiments, drag/drop links, favorites, advanced filtering, item sheet navigation, complete service orders, UI state persistence, Tidy Classic verification, true confidential catalog storage, robust transaction rollback. Blacksmith Refinements was not supplied and remains outside scope.
- The database is a GM-only Journal `Averis Artisan — GM Database (do not delete)`. Back it up alongside your world; don't edit it manually. Uninstalling does not delete this world data or created Items.

## Development
`node --test tests/rules.test.mjs` tests the independent rules and parsed catalog. `node --check scripts/main.js` checks syntax. `tools/build_data.py /path/to/journal-exports` regenerates the catalog (Python + beautifulsoup4). The four source filenames must contain `hybrid`, `gathering`, `enchanting`, `cooking` respectively. Import into a GM-managed test world and test all action flows before a release. Do not overwrite the GM database by updating the package; use the catalog import UI only after backing up. Version 0.1.0 is intentionally not marked verified in its manifest.

Repository: https://github.com/Daikaze/Crafting. The original v0.1.0 preview source is published here; the manifest points to a versioned source archive.

## v14 compatibility preview
Main windows now extend ApplicationV2; existing dialogs use the documented v14 legacy namespace. Actor header controls and scene controls have been adapted. Existing data, recipes and unfinished feature limitations remain unchanged. D&D 5e minimum remains 5.3.3; install a system version supported by your v14 build. Foundry runtime and Tidy Classic have not been tested. The v13 version remains on main.

## v0.2.0
- Dashboard card heights corrected, Gathering category filters, human-readable hours/minutes.
- Recipe scrolls now have a Learn Recipe utility activity; old scrolls have a direct Learn action on supported sheets and remain usable through Artisan > Materials.
- GM > Compendiums > Build all Artisan packs creates world Item packs for materials, scrolls, equipment, alchemy, meals, rune and enchantment references. Uses installed SRD bases where found and preserves existing custom links. Custom conditional mechanics or missing base templates are marked manual review. Generated templates do not assert fully automated combat effects. Existing worlds are not reset. Test on a copy.

## v0.2.1
GM Projects and the Dashboard project count now include only character actors assigned to, or owned by, non-GM users (including offline users). NPCs and GM-only actors remain available in Actor Management and NPC Orders. No projects or actor records are deleted. Recipe learning is unchanged.

## v0.2.2 — Learning System
- Player Learning: instant Recipe Scrolls, reusable Recipe Books, NPC Training, active/paused lessons. Direct GM Unlock remains available in GM Learning and Actors. No learning rolls. Proficiency is required for scrolls, book study, and training; direct GM unlock overrides learning prerequisites, not crafting requirements.
- NPC training defaults: Common 10 GP / 2h; Uncommon 35 GP / 4h; Rare 100 GP / 8h; Very Rare 300 GP / 16h. GM configures each NPC's eligible students, teachable recipes (must already be learned by NPC), rates and duration. NPC must have required proficiency. Fees paid once at start; cancel does not refund. Book study is free, takes 1/2/4/8h, requires book in inventory, and never consumes book. Both use manual downtime budget and share one active project slot with crafting; paused lessons allowed. Smart approval applies to book study and NPC training, scrolls remain immediate.
- GM → Learning → Create Recipe Book creates an item directly in selected actor inventory; configure NPC training after giving NPC recipes and proficiency. Existing data retained. Foundry runtime not tested.

## v0.3.0 — Rarity organization & Advanced Gathering
- Recipe browsers and material inventory group by rarity; recipes/gathering have rarity filters. GM → Compendiums → Organize existing packs by rarity moves module-tagged entries into numbered rarity folders, preserving IDs and links. Build packs also organizes. Untagged items are untouched. Source materials without a stated rarity go into Unclassified.
- Gathering has selectable Survival/Nature/relevant tools, mining STR/Survival methods, per-patch GM conditions, hidden patches, reset search, configurable attempts, regrowth days, approved one-use advantage, creature duration and large-specimen yield. Search is 30 min, harvest 10 min (creatures 15–30), mining 30 min. GM adjudicates hazards, seasons and access, logs private DC/results. A failed search requires GM reset; depleted creature/Very Rare sources require manual reset. Mining ore-unit cap (optional) requires explicit GM replenishment when exhausted. Rare and Very Rare checks follow Smart Approval. Existing data retained. No automatic damage or poison effects from gathering hazards; no automatic salvage. Foundry runtime not tested.

## v0.4.0 — Cooking and UI fixes
- Recipe entries now have automatic height, padding and gaps; rarity displayed at group heading rather than repeated. One window per actor UUID and one GM window; repeated open focuses the existing window. Removed duplicate legacy header hook on ApplicationV2 and dual scene callback.
- Cooking tab lists learned recipes, servings and prepared meals. Cooked meals are consumables with Eat Serving activity; old loot meals continue via Cooking/Materials. Share servings to player character inventories, with validation of quantity and recipients. Eating consumes one serving and 10 minutes of downtime. One special benefit per Long Rest, 4h world time or earlier when GM advances artisan day; no stacking temporary HP. Meal-granted temporary HP tracked on actor update, expires only if tracked remainder matches current HP (same-value replacement cannot be detected). Fresh/Warming/Festival +1 are one-use, manually applied to eligible rolls via Use Bonus chat action (no permanent effect). Comfort Food +1 HP uses rest result dhd when provided by system; runtime verification required. Legacy meals with no tracked grant retain existing temp HP until normal rules remove it. No automatic food spoilage. GM must adjudicate clean prep/quiet meal, ingredient substitutions and cooking help manually; those are not fully automated. Existing world data retained. Foundry runtime not tested.
