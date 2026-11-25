# Foundry v14 acceptance checklist — 1.0.0

Use a cloned world. Export GM backup from Settings and create a Foundry world backup before upgrading. Use the D&D 5e version compatible with your Foundry build.

| Area | Expected behavior |
| --- | --- |
| Installation | Manifest displays 1.0.0; module loads without console errors. |
| Migration | Learned recipes, regions, budgets, active/paused projects, links and orders survive. |
| Player access | Only owned world actors open; GM Projects lists player characters only; no duplicate windows. |
| Recipe browser | Grouped rarity, favorites, craftable filters, no overlapping buttons. |
| Learning | Scroll consumed only on success; book reusable; NPC training charges once; downtime decrements. |
| Crafting | Insufficient requirements blocked, materials reserved, GP charged, one active slot, success output and failure loss. Cancel returns materials, not gold. |
| Gathering | GM assigns regions; test search failure/reset, harvest, mining, day regrowth and hidden DC in UI. |
| Cooking | Full/partial servings, share, eat, temp HP, no stacking, long-rest reset. |
| Runes and enchantments | Compatible target, separate slots, attunement, two selected each, charges, rest. |
| NPC orders | Customer/NPC stock, price, approval, progress, result, cancellation and failure. |
| Recovery | In test world only, unlink a result before finishing; restore link, then GM Settings > Recovery queue; verify one output. Never retry if a prior output/refund was moved or merged. |
| Integrations | Test native effect UUID; DAE on/off; Midi single-target GM workflow only. Confirm damage does not double. |
| Multiplayer | Connect separate player client, test approvals, inventory updates, offline character, primary GM switch. |
| Tidy | Check standard and Tidy headers, NPC and item panels. |
| Performance | Measure load and scene FPS with module disabled/enabled; no measured benchmark included. |

Run source-only Node tests with `node --test tests/*.mjs`. These are not a Foundry runtime simulation. No automatic restoration of a GM database backup: use a complete Foundry world backup when inventory consistency matters.
