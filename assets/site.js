document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());


// Keep the page clear of the fixed top ribbon regardless of line wraps, zoom, or viewport changes.
(()=>{const ribbon=document.querySelector('.support-top');if(!ribbon)return;
const update=()=>document.documentElement.style.setProperty('--support-live-height',Math.ceil(ribbon.getBoundingClientRect().height)+'px');
update();window.addEventListener('resize',update,{passive:true});
if('ResizeObserver' in window){new ResizeObserver(update).observe(ribbon);}
})();
