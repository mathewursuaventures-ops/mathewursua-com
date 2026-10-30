document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());
document.querySelectorAll('[data-load-video]').forEach(btn=>btn.addEventListener('click',()=>{const holder=btn.closest('.video-placeholder');if(!holder)return;const frame=document.createElement('iframe');frame.src='https://www.youtube-nocookie.com/embed/j6mDC0QaW_s?autoplay=1';frame.title='Featured video: original site embed';frame.loading='lazy';frame.allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';holder.replaceChildren(frame);}));

// Keep the page clear of the fixed top ribbon regardless of line wraps, zoom, or viewport changes.
(()=>{const ribbon=document.querySelector('.support-top');if(!ribbon)return;
const update=()=>document.documentElement.style.setProperty('--support-live-height',Math.ceil(ribbon.getBoundingClientRect().height)+'px');
update();window.addEventListener('resize',update,{passive:true});
if('ResizeObserver' in window){new ResizeObserver(update).observe(ribbon);}
})();
