export const clone = x => JSON.parse(JSON.stringify(x));
export const slug = s => String(s).toLowerCase().replace(/[’‘]/g,"'").replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
export const approval = (r,mode='smart')=>Boolean(mode==='manual'||(mode==='smart'&&(['Rare','Very Rare'].includes(r.rarity)||r.experimental||r.artifact))); 
export function outcome(r,total,nat){const margin=total-r.dc; const success=margin>=0; let loss=0,quantity=success?r.quantity:0;
 if(r.category==='Cooking'){if(success)quantity+=nat===20?1:0;else if(margin>=-4)quantity=Math.ceil(r.quantity/2);return {success,margin,quantity,loss:success||margin>=-4?'all':'half',benefit:success};}
 if(success)loss='all';else if(r.category==='Alchemy')loss=margin<=-5?'all':1;else if(r.category==='Runecrafting')loss=1;else if(r.category==='Enchanting')loss=margin<=-5?'all':1;else loss=margin<=-5?2:1;
 return {success,margin,quantity,loss,masterwork:success&&margin>=5&&!['Alchemy','Runecrafting'].includes(r.category)};
}
export function lossPlan(materials,loss,chosen=[]){let map={};for(const m of materials)map[m.id]=(map[m.id]||0)+m.qty; if(loss==='all')return map;if(loss==='half')return Object.fromEntries(Object.entries(map).map(([k,v])=>[k,Math.ceil(v/2)]));let out={};const cap=Math.min(loss,Object.values(map).reduce((a,b)=>a+b,0));if(chosen.length!==cap)throw Error(`Choose ${cap} lost unit(s).`);for(const id of chosen){if((out[id]||0)>= (map[id]||0))throw Error('Invalid loss selection');out[id]=(out[id]||0)+1;}return out;}
export function advance(p,minutes,budget){if(p.status!=='active')throw Error('Project not active');if(!Number.isInteger(minutes)||minutes<=0||minutes>budget||minutes>p.recipe.minutes-p.progress)throw Error('Invalid work time');p.progress+=minutes;if(p.progress===p.recipe.minutes)p.status='ready';return budget-minutes;}
export function patchAvailable(p,day){return !p.hidden&&(p.remaining>0||p.regrowAt!=null&&day>=p.regrowAt);}
export function harvestPatch(p,resource,day){if(p.remaining<=0&&p.regrowAt!=null&&day>=p.regrowAt){p.remaining=resource.attempts;p.regrowAt=null;}if(p.remaining<=0)throw Error('Patch depleted');p.remaining--;if(p.remaining===0)p.regrowAt=resource.regrowth==null?null:day+resource.regrowth;}
