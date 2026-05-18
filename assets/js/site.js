/* FutureFlow site JS — theme, hero crossfade, cinematic scroll, cursor, parallax */
(function(){
  'use strict';

  // ---------- Theme ----------
  var KEY = 'ff-theme';
  function applyTheme(t){
    document.documentElement.setAttribute('data-theme', t);
    try{ localStorage.setItem(KEY, t); }catch(e){}
    var meta = document.querySelector('meta[name="theme-color"]');
    if(meta) meta.setAttribute('content', t==='light' ? '#F7F8FE' : '#06060F');
    syncHeroVideos();
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

  // ---------- Hero seamless crossfade ----------
  // Two video elements per theme, offset by half the loop, cross-fade every halfPeriod
  function syncHeroVideos(){
    var theme = document.documentElement.getAttribute('data-theme') || 'dark';
    document.querySelectorAll('.hero-bg video').forEach(function(v){
      var match = v.dataset.theme === theme;
      if(match){
        try{ v.play(); }catch(e){}
      } else {
        try{ v.pause(); }catch(e){}
      }
    });
  }

  function initHeroCrossfade(){
    var heros = Array.from(document.querySelectorAll('.hero-bg'));
    heros.forEach(function(bg){
      var pairs = {};
      bg.querySelectorAll('video[data-theme]').forEach(function(v){
        var k = v.dataset.theme;
        if(!pairs[k]) pairs[k] = [];
        pairs[k].push(v);
      });
      Object.keys(pairs).forEach(function(theme){
        var pair = pairs[theme];
        if(pair.length < 2) {
          // Single video: still loops natively, mark as front
          pair[0] && pair[0].classList.add('front');
          return;
        }
        var a = pair[0], b = pair[1];
        a.classList.add('front'); b.classList.add('back');

        function start(){
          if(!a.duration || !b.duration) return;
          var halfPeriod = Math.max(2, a.duration / 2); // seconds
          // Offset b by halfPeriod from start
          try{ b.currentTime = halfPeriod; }catch(e){}
          // Toggle front every halfPeriod*1000 ms
          setInterval(function(){
            if(a.classList.contains('front')){
              a.classList.replace('front','back');
              b.classList.replace('back','front');
            } else {
              b.classList.replace('front','back');
              a.classList.replace('back','front');
            }
          }, halfPeriod * 1000);
        }
        // Wait until both ready
        var ready = 0;
        function onReady(){ ready++; if(ready >= 2) start(); }
        if(a.readyState >= 2) onReady(); else a.addEventListener('loadeddata', onReady, {once:true});
        if(b.readyState >= 2) onReady(); else b.addEventListener('loadeddata', onReady, {once:true});
      });
    });
  }

  initTheme();
  initHeroCrossfade();

  // ---------- Sticky header + scroll progress ----------
  var header = document.querySelector('.site-header');
  var scrollProg = document.createElement('div');
  scrollProg.className = 'scroll-prog';
  document.body.appendChild(scrollProg);

  function onScroll(){
    if(header){
      if(window.scrollY > 8) header.classList.add('scrolled');
      else header.classList.remove('scrolled');
    }
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var pct = max > 0 ? (window.scrollY / max) * 100 : 0;
    scrollProg.style.width = pct.toFixed(2) + '%';
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

    // Pause hero videos when offscreen
    document.querySelectorAll('.hero-bg').forEach(function(bg){
      var ioVid = new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          bg.querySelectorAll('video').forEach(function(v){
            if(en.isIntersecting){
              if(v.dataset.theme === (document.documentElement.getAttribute('data-theme') || 'dark')){
                try{ v.play(); }catch(e){}
              }
            } else {
              try{ v.pause(); }catch(e){}
            }
          });
        });
      }, { threshold: 0.05 });
      ioVid.observe(bg);
    });
  } else {
    document.querySelectorAll('.rv').forEach(function(el){ el.classList.add('in'); });
  }

  // ---------- Year in footer ----------
  document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  // ---------- Cinematic film-scroll: multi-scene crossfade ----------
  var filmScroll = document.querySelector('[data-film-scroll]');
  if(filmScroll && !window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    var shots = Array.from(filmScroll.querySelectorAll('.film-shot'));
    var scenes = Array.from(filmScroll.querySelectorAll('.film-scene'));
    var bar = filmScroll.querySelector('.film-progress-bar');
    var chips = Array.from(filmScroll.querySelectorAll('.film-chapters span'));
    var n = Math.max(shots.length, scenes.length);
    // Set scroll height: 80vh per scene
    filmScroll.style.height = (n * 85) + 'vh';

    // Start all videos
    shots.forEach(function(s){
      var v = s.querySelector('video');
      if(v){ try{ v.play(); }catch(e){} }
    });

    var lastIdx = -1;
    var ticking = false;
    function update(){
      ticking = false;
      var rect = filmScroll.getBoundingClientRect();
      var winH = window.innerHeight;
      var total = rect.height - winH;
      var passed = Math.min(Math.max(-rect.top, 0), total);
      var prog = total > 0 ? passed / total : 0;
      // Scene index based on progress
      var raw = prog * n;
      var idx = Math.min(n - 1, Math.max(0, Math.floor(raw)));
      if(idx !== lastIdx){
        lastIdx = idx;
        shots.forEach(function(s,i){ s.classList.toggle('active', i === idx); });
        scenes.forEach(function(s,i){ s.classList.toggle('active', i === idx); });
        chips.forEach(function(c,i){ c.classList.toggle('active', i === idx); });
        // Play active shot's video, pause others
        shots.forEach(function(s,i){
          var v = s.querySelector('video');
          if(!v) return;
          if(i === idx){ try{ v.play(); }catch(e){} } else { try{ v.pause(); }catch(e){} }
        });
      }
      if(bar) bar.style.width = (prog * 100).toFixed(2) + '%';
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

    // Click on chapter chips → scroll to that scene
    chips.forEach(function(c,i){
      c.addEventListener('click', function(){
        var rect = filmScroll.getBoundingClientRect();
        var top = window.scrollY + rect.top + (filmScroll.offsetHeight - window.innerHeight) * (i / n) + 1;
        window.scrollTo({top: top, behavior: 'smooth'});
      });
    });
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

      if(heroEl){
        var r = heroEl.getBoundingClientRect();
        if(my >= r.top && my <= r.bottom){
          var cx = (mx - (r.left + r.width/2)) / (r.width/2);
          var cy = (my - (r.top + r.height/2)) / (r.height/2);
          if(heroBgEl) heroBgEl.style.transform = 'translate3d(' + (cx * -10) + 'px,' + (cy * -8) + 'px,0) scale(1.04)';
          if(orbEl) orbEl.style.transform = 'translate3d(' + (cx * 14) + 'px,' + (cy * 10) + 'px,0)';
        } else {
          if(heroBgEl) heroBgEl.style.transform = '';
          if(orbEl) orbEl.style.transform = '';
        }
      }

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

    (function loop(){
      gx += (mx - gx) * 0.18;
      gy += (my - gy) * 0.18;
      glow.style.transform = 'translate(' + gx + 'px,' + gy + 'px) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    })();
  }
})();
