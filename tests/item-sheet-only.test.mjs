import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const source = fs.readFileSync(new URL('../scripts/main.js', import.meta.url), 'utf8');
const start = source.indexOf('function isArtisanItemSheet(');
const end = source.indexOf('function itemArtisanPanel(', start);
assert.ok(start >= 0 && end > start, 'item-sheet guard exists');

class ItemSheetV2 {}
const isArtisanItemSheet = new Function('foundry', source.slice(start, end) + 'return isArtisanItemSheet;')({
  applications: { sheets: { ItemSheetV2 } }
});

test('Artisan modifications appear on an actual item sheet', () => {
  const sheet = {};
  const item = { documentName: 'Item', sheet };
  assert.equal(isArtisanItemSheet(sheet, item), true);
});

test('Artisan modifications never appear in item-use activity dialogs', () => {
  const realSheet = {};
  const item = { documentName: 'Item', sheet: realSheet };
  const useDialog = { document: item, item };
  assert.equal(isArtisanItemSheet(useDialog, item), false);
});

test('Foundry ItemSheetV2 subclasses receive Artisan controls', () => {
  const item = { documentName: 'Item', sheet: {} };
  const customSheet = new ItemSheetV2();
  assert.equal(isArtisanItemSheet(customSheet, item), true);
});

test('Unrelated app document types are not item sheets', () => {
  const sheet = {};
  assert.equal(isArtisanItemSheet(sheet, { documentName: 'Actor', sheet }), false);
  assert.equal(isArtisanItemSheet(sheet, null), false);
});

test('Both Artisan and learning controls use item-sheet guard', () => {
  assert.match(source, /function itemArtisanPanel\(app,html\)[^\n]*if\(!isArtisanItemSheet\(app,i\)\|\|/);
  assert.match(source, /doc\?\.documentName==='Item'&&isArtisanItemSheet\(app,doc\)/);
});
