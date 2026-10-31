document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());


// Keep the page clear of the fixed top ribbon regardless of line wraps, zoom, or viewport changes.
(()=>{const ribbon=document.querySelector('.support-top');if(!ribbon)return;
const update=()=>document.documentElement.style.setProperty('--support-live-height',Math.ceil(ribbon.getBoundingClientRect().height)+'px');
update();window.addEventListener('resize',update,{passive:true});
if('ResizeObserver' in window){new ResizeObserver(update).observe(ribbon);}
})();


/* v1.7.2 RC4 — a7821b7 image recovery, shared by homepage and photography page. */
(function () {
  const mirror = 'https://raw.githubusercontent.com/mathewursuaventures-ops/mathewursua-com/main/';
  const assets = [
    ['.mu-hero-art img', 'assets/illustrations/mu-intrepid-lens-hero-v01.webp'],
    ['.brand--signature img', 'assets/signature-header.png']
  ];
  function install(selector, relativePath) {
    const img = document.querySelector(selector);
    if (!img || img.getAttribute('src') !== relativePath) return;
    let triedMirror = false;
    function recover() {
      if (!triedMirror) {
        triedMirror = true;
        img.src = mirror + relativePath;
      } else {
        img.hidden = true;
        img.style.display = 'none'; // stronger than earlier author CSS for signature images
        if (selector === '.mu-hero-art img') {
          const holder = img.closest('.mu-hero-art');
          if (holder) {
            holder.classList.add('mu-art-unavailable');
            holder.setAttribute('role','img');
            holder.setAttribute('aria-label','Disaster Images documentary photography and public records');
          }
        } else {
          const substitute = document.createElement('span');
          substitute.className = 'mu-signature-text-fallback';
          substitute.textContent = 'Mathew Ursua Signature';
          img.parentNode.insertBefore(substitute, img);
        }
      }
    }
    img.addEventListener('error', recover);
    if (img.complete && img.naturalWidth === 0) recover();
  }
  function run() { assets.forEach(([selector, relativePath]) => install(selector, relativePath)); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();
