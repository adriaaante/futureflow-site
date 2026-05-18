/* FutureFlow site JS — theme, scroll, reveal, drawer, video, cursor, parallax, marquee */
(function(){
  'use strict';

  // ---------- Theme ----------
  var KEY = 'ff-theme';
  function applyTheme(t){
    document.documentElement.setAttribute('data-theme', t);
    try{ localStorage.setItem(KEY, t); }catch(e){}
    var meta = document.querySelector('meta[name="theme-color"]');
    if(meta) meta.setAttribute('content', t==='light' ? '#F7F8FE' : '#06060F');
    syncHeroVideo();
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

  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-theme-toggle]');
    if(!t) return;
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    applyTheme(cur === 'dark' ? 'light' : 'dark');
  });

  // ---------- Hero video swap by theme ----------
  function syncHeroVideo(){
    var theme = document.documentElement.getAttribute('data-theme') || 'dark';
    document.querySelectorAll('.hero-video').forEach(function(v){
      var isMatch = v.dataset.theme === theme;
      v.classList.toggle('active', isMatch);
      if(isMatch){
        try{ v.play(); }catch(e){}
      } else {
        try{ v.pause(); }catch(e){}
      }
    });
  }

  initTheme();

  // ---------- Sticky header ----------
  var header = document.querySelector('.site-header');
  function onScroll(){
    if(header){
      if(window.scrollY > 8) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
    }
    // Scroll progress
    if(scrollProg){
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      scrollProg.style.width = pct.toFixed(2) + '%';
    }
  }

  // ---------- Scroll progress ----------
  var scrollProg = document.createElement('div');
  scrollProg.className = 'scroll-prog';
  document.body.appendChild(scrollProg);

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

    // Pause hero video when offscreen
    var heroBg = document.querySelector('.hero-bg');
    if(heroBg){
      var ioVid = new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          document.querySelectorAll('.hero-video.active').forEach(function(v){
            if(en.isIntersecting){ try{ v.play(); }catch(e){} }
            else { try{ v.pause(); }catch(e){} }
          });
        });
      }, { threshold: 0.05 });
      ioVid.observe(heroBg);
    }
  } else {
    document.querySelectorAll('.rv').forEach(function(el){ el.classList.add('in'); });
  }

  // ---------- Year in footer ----------
  document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  // ---------- Cinematic scroll: scrub video timeline + activate scenes ----------
  var filmScroll = document.querySelector('[data-film-scroll]');
  if(filmScroll && !window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    var filmVideo = filmScroll.querySelector('video');
    var scenes = Array.from(filmScroll.querySelectorAll('.film-scene'));
    var bar = filmScroll.querySelector('.film-progress-bar');
    var chips = Array.from(filmScroll.querySelectorAll('.film-chapters span'));

    var ready = false;
    function readyHandler(){
      ready = true;
      try{ filmVideo.pause(); }catch(e){}
    }
    if(filmVideo){
      filmVideo.addEventListener('loadedmetadata', readyHandler);
      filmVideo.addEventListener('canplay', readyHandler);
      // Force preload
      try{ filmVideo.load(); }catch(e){}
    }

    var ticking = false;
    function update(){
      ticking = false;
      var rect = filmScroll.getBoundingClientRect();
      var winH = window.innerHeight;
      var total = rect.height - winH;
      var passed = Math.min(Math.max(-rect.top, 0), total);
      var prog = total > 0 ? passed / total : 0;

      // Scrub video
      if(ready && filmVideo && filmVideo.duration && isFinite(filmVideo.duration)){
        var t = prog * filmVideo.duration;
        if(Math.abs(filmVideo.currentTime - t) > 0.04){
          try{ filmVideo.currentTime = t; }catch(e){}
        }
      }

      // Progress bar
      if(bar) bar.style.width = (prog * 100).toFixed(2) + '%';

      // Activate scene based on progress
      var n = scenes.length;
      var idx = Math.min(n - 1, Math.floor(prog * n));
      scenes.forEach(function(s,i){ s.classList.toggle('active', i === idx); });
      chips.forEach(function(c,i){ c.classList.toggle('active', i === idx); });
    }
    function onScrollFilm(){
      if(!ticking){
        requestAnimationFrame(update);
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScrollFilm, {passive:true});
    window.addEventListener('resize', onScrollFilm);
    update();
  }

  // ---------- Cursor glow + mouse parallax + magnetic ----------
  var canHover = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if(canHover && !window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    var glow = document.createElement('div');
    glow.className = 'cursor-glow';
    document.body.appendChild(glow);

    var mx = 0, my = 0, gx = 0, gy = 0;
    var heroEl = document.querySelector('.hero');
    var heroBgEl = document.querySelector('.hero-bg');
    var orbEl = document.querySelector('.hero-orb');
    var magnets = Array.from(document.querySelectorAll('.magnet'));

    function onMove(e){
      mx = e.clientX; my = e.clientY;
      glow.classList.add('show');

      // Hero parallax (only when hovering hero area)
      if(heroEl){
        var r = heroEl.getBoundingClientRect();
        if(my >= r.top && my <= r.bottom){
          var cx = (mx - (r.left + r.width/2)) / (r.width/2);  // -1..1
          var cy = (my - (r.top + r.height/2)) / (r.height/2);
          if(heroBgEl) heroBgEl.style.transform = 'translate3d(' + (cx * -10) + 'px,' + (cy * -8) + 'px,0) scale(1.04)';
          if(orbEl) orbEl.style.transform = 'translate3d(' + (cx * 14) + 'px,' + (cy * 10) + 'px,0)';
        } else {
          if(heroBgEl) heroBgEl.style.transform = '';
          if(orbEl) orbEl.style.transform = '';
        }
      }

      // Magnetic CTAs
      magnets.forEach(function(m){
        var r = m.getBoundingClientRect();
        var dx = mx - (r.left + r.width/2);
        var dy = my - (r.top + r.height/2);
        var dist = Math.sqrt(dx*dx + dy*dy);
        var radius = 120;
        if(dist < radius){
          var k = (1 - dist/radius) * 0.45;
          m.style.transform = 'translate(' + (dx*k) + 'px,' + (dy*k) + 'px)';
        } else {
          m.style.transform = '';
        }
      });
    }
    function onLeave(){
      glow.classList.remove('show');
      if(heroBgEl) heroBgEl.style.transform = '';
      if(orbEl) orbEl.style.transform = '';
      magnets.forEach(function(m){ m.style.transform = ''; });
    }

    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseleave', onLeave);
    window.addEventListener('blur', onLeave);

    // RAF tween glow
    (function loop(){
      gx += (mx - gx) * 0.18;
      gy += (my - gy) * 0.18;
      glow.style.transform = 'translate(' + gx + 'px,' + gy + 'px) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    })();
  }
})();
