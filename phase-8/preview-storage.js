/* Hosting-only Phase 8 isolation. Never writes or deletes source farm records.
   Copy the PR #1 farm first if available, otherwise the original preview farm.
   A prior Phase 8 primary OR backup always prevents a later automatic import. */
(function(){
 const target="mgg-phase-8:", keys=["mgg10","mgg10-backup"];
 try {
  if(keys.some(key=>localStorage.getItem(target+key)!==null))return;
  for(const prefix of ["mgg-pr-1:",""]){
   const raw=keys.map(key=>localStorage.getItem(prefix+key));
   const readable=raw.some(value=>{try{return JSON.parse(value)?.version===1;}catch{return false;}});
   if(!readable)continue;
   raw.forEach((value,i)=>{if(value!==null)localStorage.setItem(target+keys[i],value);});
   break;
  }
 }catch{/* Game retains its existing save-warning handling for blocked storage. */}
})();
