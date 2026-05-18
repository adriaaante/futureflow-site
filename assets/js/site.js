/* FutureFlow site JS — theme toggle, scroll header, reveal, mobile drawer */
(function(){
  'use strict';

  // ---------- Theme ----------
  var KEY = 'ff-theme';
  function applyTheme(t){
    document.documentElement.setAttribute('data-theme', t);
    try{ localStorage.setItem(KEY, t); }catch(e){}
    var meta = document.querySelector('meta[name="theme-color"]');
    if(meta) meta.setAttribute('content', t==='light' ? '#F7F8FE' : '#06060F');
  }
  function initTheme(){
    var saved;
    try{ saved = localStorage.getItem(KEY); }catch(e){}
    if(saved === 'light' || saved === 'dark'){
      applyTheme(saved);
    } else {
      var prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
      applyTheme(prefersLight ? 'light' : 'dark');
    }
  }
  initTheme();

  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-theme-toggle]');
    if(!t) return;
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(cur === 'dark' ? 'light' : 'dark');
  });

  // ---------- Sticky header bg ----------
  var header = document.querySelector('.site-header');
  function onScroll(){
    if(!header) return;
    if(window.scrollY > 8) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  // ---------- Mobile drawer ----------
  var drawer = document.querySelector('[data-drawer]');
  document.addEventListener('click', function(e){
    if(e.target.closest('[data-drawer-open]')){
      drawer && drawer.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    if(e.target.closest('[data-drawer-close]')){
      drawer && drawer.classList.remove('open');
      document.body.style.overflow = '';
    }
  });

  // ---------- Reveal on scroll ----------
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function(el){ el.classList.add('in'); });
  }

  // ---------- Year in footer ----------
  document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });
})();
