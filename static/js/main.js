/* ============================================
   PORTFOLIO — MAIN JAVASCRIPT
   ============================================ */


document.addEventListener('DOMContentLoaded', () => {

  // ── Loader ──────────────────────────────────
  const loader = document.getElementById('loader');
  if (loader) {
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 600);
  }

  // ── Navbar scroll effect ─────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Mobile nav toggle ────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
      // Animate hamburger
      const spans = navToggle.querySelectorAll('span');
      if (isOpen) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
      } else {
        spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      }
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('open');
      }
    });
  }

  // ── Reveal on scroll ────────────────────────
  const revealEls = document.querySelectorAll('[data-reveal]');
  if (revealEls.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('revealed');
          }, i * 100);
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealEls.forEach(el => revealObserver.observe(el));
  }

  // ── Auto-dismiss messages ────────────────────
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

  // ── Smooth scroll for anchor links ──────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Form input animations ────────────────────
  document.querySelectorAll('.form-input, .form-textarea').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;

    input.addEventListener('focus', () => {
      group.classList.add('focused');
    });
    input.addEventListener('blur', () => {
      group.classList.remove('focused');
    });
  });

  // ── Typed text effect (hero title) ──────────
  const titleEl = document.querySelector('.title-gradient');
  if (titleEl) {
    const titles = [
      titleEl.textContent,
      'Python Developer',
      'Backend Developer'
    ];
    let idx = 0;
    if (titles[0]) {
      setInterval(() => {
        idx = (idx + 1) % titles.length;
        titleEl.style.opacity = '0';
        titleEl.style.transform = 'translateY(-8px)';
        titleEl.style.transition = 'all 0.3s ease';
        setTimeout(() => {
          titleEl.textContent = titles[idx];
          titleEl.style.opacity = '1';
          titleEl.style.transform = 'translateY(0)';
        }, 300);
      }, 3000);
    }
  }

  // ── Active nav link highlight ────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });

  console.log('%c Portfolio Loaded ✓', 'color: #7c6af7; font-weight: bold; font-size: 14px;');
});

/* ============================================
   SNOW EFFECT — Canvas based
 /* ============================================
   SNOW + WIND + FOG EFFECT
   — Behind content (z-index: 0)
   — Wind gusts shift flakes dynamically
   — Fog layers drift slowly across screen
   ============================================ */

class SnowEffect {
  constructor() {
    // ── Two canvases: fog behind snow ──────────
    this.fogCanvas = document.createElement('canvas');
    this.fogCtx = this.fogCanvas.getContext('2d');
    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');

    // Fog canvas — lowest, behind everything
    this._styleCanvas(this.fogCanvas, '-1');
    this.fogCanvas.id = 'fog-canvas';

    // Snow canvas — just above fog, behind page content
    this._styleCanvas(this.canvas, '0');
    this.canvas.id = 'snow-canvas';

    // Insert BEFORE first child so they're behind all content
    document.body.insertBefore(this.fogCanvas, document.body.firstChild);
    document.body.insertBefore(this.canvas, document.body.firstChild);

    // ── State ──────────────────────────────────
    this.flakes = [];
    this.fogBlobs = [];
    this.count = 140;
    this._paused = false;

    // ── Wind system ────────────────────────────
    this.wind = 0;       // current wind speed (px/frame)
    this.windTarget = 0;      // target wind (changes in gusts)
    this.windTimer = 0;       // frames until next gust

    this.resize();
    this.initFlakes();
    this.initFog();
    this.animate();

    window.addEventListener('resize', () => this.resize());
  }

  _styleCanvas(canvas, zIndex) {
    Object.assign(canvas.style, {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      zIndex: zIndex,
    });
  }

  resize() {
    this.W = window.innerWidth;
    this.H = window.innerHeight;
    this.canvas.width = this.W;
    this.canvas.height = this.H;
    this.fogCanvas.width = this.W;
    this.fogCanvas.height = this.H;
  }

  // ── Wind ───────────────────────────────────────
  updateWind() {
    this.windTimer--;
    if (this.windTimer <= 0) {
      // Schedule next gust: every 3–9 seconds at 60fps
      this.windTimer = Math.random() * 360 + 180;
      // New wind target: -2.5 (left) to +2.5 (right), often rightward
      this.windTarget = (Math.random() * 5 - 1.5);
    }
    // Smoothly interpolate toward target (inertia)
    this.wind += (this.windTarget - this.wind) * 0.012;
  }

  // ── Snowflakes ─────────────────────────────────
  createFlake() {
    return {
      x: Math.random() * this.W,
      y: Math.random() * this.H - this.H,
      r: Math.random() * 3.2 + 0.6,
      speed: Math.random() * 1.1 + 0.35,
      drift: Math.random() * 0.5 - 0.25,   // personal micro-drift
      angle: Math.random() * Math.PI * 2,
      wobble: Math.random() * 0.025 + 0.004,
      opacity: Math.random() * 0.55 + 0.25,
      spin: Math.random() * 0.04 - 0.02,  // slow rotation
    };
  }

  initFlakes() {
    for (let i = 0; i < this.count; i++) {
      const f = this.createFlake();
      f.y = Math.random() * this.H; // pre-scatter on first load
      this.flakes.push(f);
    }
  }

  drawFlakes() {
    this.ctx.clearRect(0, 0, this.W, this.H);
    this.updateWind();

    this.flakes.forEach(f => {
      // Wind pushes all flakes, personal drift adds variety
      f.angle += f.wobble;
      f.x += this.wind + f.drift + Math.sin(f.angle) * 0.5;
      f.y += f.speed;

      // Wrap horizontally (wind can carry flakes off-screen)
      if (f.x > this.W + 20) f.x = -20;
      if (f.x < -20) f.x = this.W + 20;
      // Reset when fallen off bottom
      if (f.y > this.H + 10) {
        Object.assign(f, this.createFlake());
        f.y = -5;
        f.x = Math.random() * this.W;
      }

      // Soft glowing snowflake (radial gradient)
      const g = this.ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 2);
      g.addColorStop(0, `rgba(255,255,255,${f.opacity})`);
      g.addColorStop(0.4, `rgba(210,200,255,${f.opacity * 0.6})`);
      g.addColorStop(1, `rgba(160,140,255,0)`);

      this.ctx.beginPath();
      this.ctx.arc(f.x, f.y, f.r * 2, 0, Math.PI * 2);
      this.ctx.fillStyle = g;
      this.ctx.fill();
    });
  }

  // ── Fog ─────────────────────────────────────────
  initFog() {
    // 6 large soft fog blobs at different heights & speeds
    const fogColors = [
      'rgba(80,60,140,',   // deep purple
      'rgba(40,30,80,',    // dark indigo
      'rgba(100,80,160,',  // mid purple
      'rgba(60,50,120,',   // muted violet
      'rgba(30,25,70,',    // near-black purple
      'rgba(90,70,150,',   // light purple
    ];
    for (let i = 0; i < 6; i++) {
      this.fogBlobs.push({
        x: Math.random() * this.W * 1.5 - this.W * 0.25,
        y: Math.random() * this.H,
        w: Math.random() * this.W * 0.7 + this.W * 0.4,  // wide blobs
        h: Math.random() * 180 + 80,
        speed: Math.random() * 0.18 + 0.04,   // slow horizontal drift
        opacity: Math.random() * 0.10 + 0.04,  // very subtle
        color: fogColors[i],
        phase: Math.random() * Math.PI * 2,   // vertical breathing phase
        breathe: Math.random() * 0.005 + 0.002,
      });
    }
  }

  drawFog() {
    this.fogCtx.clearRect(0, 0, this.W, this.H);

    this.fogBlobs.forEach(blob => {
      // Drift rightward (same wind direction, much slower)
      blob.x += blob.speed + this.wind * 0.08;
      blob.phase += blob.breathe;

      // Wrap around screen
      if (blob.x - blob.w / 2 > this.W + 100) blob.x = -blob.w / 2 - 100;
      if (blob.x + blob.w / 2 < -100) blob.x = this.W + blob.w / 2 + 100;

      // Breathing: slight vertical shift
      const yOff = Math.sin(blob.phase) * 18;

      // Draw elliptical gradient blob
      const gx = this.fogCtx.createRadialGradient(
        blob.x, blob.y + yOff, 0,
        blob.x, blob.y + yOff, blob.w / 2
      );
      gx.addColorStop(0, blob.color + blob.opacity + ')');
      gx.addColorStop(0.5, blob.color + (blob.opacity * 0.5) + ')');
      gx.addColorStop(1, blob.color + '0)');

      this.fogCtx.save();
      this.fogCtx.scale(1, blob.h / blob.w); // squash into ellipse
      this.fogCtx.beginPath();
      this.fogCtx.arc(blob.x, (blob.y + yOff) / (blob.h / blob.w), blob.w / 2, 0, Math.PI * 2);
      this.fogCtx.fillStyle = gx;
      this.fogCtx.fill();
      this.fogCtx.restore();
    });

    // Extra: thin ground-level fog strip at bottom
    const groundFog = this.fogCtx.createLinearGradient(0, this.H - 120, 0, this.H);
    groundFog.addColorStop(0, 'rgba(60,40,120,0)');
    groundFog.addColorStop(1, 'rgba(60,40,120,0.18)');
    this.fogCtx.fillStyle = groundFog;
    this.fogCtx.fillRect(0, this.H - 120, this.W, 120);
  }

  // ── Animate ─────────────────────────────────────
  animate() {
    this.drawFog();
    this.drawFlakes();
    this._raf = requestAnimationFrame(() => this.animate());
  }

  // ── Toggle ──────────────────────────────────────
  toggle() {
    if (this._paused) {
      this._paused = false;
      this.animate();
      this.canvas.style.display = 'block';
      this.fogCanvas.style.display = 'block';
    } else {
      this._paused = true;
      cancelAnimationFrame(this._raf);
      this.canvas.style.display = 'none';
      this.fogCanvas.style.display = 'none';
    }
  }

  destroy() {
    cancelAnimationFrame(this._raf);
    this.canvas.remove();
    this.fogCanvas.remove();
  }
}

// ── Init Snow + Toggle Button ─────────────────────
(function initSnow() {
  const start = () => {
    const snowEnabled = localStorage.getItem('snow') !== 'off';
    const snow = new SnowEffect();
    if (!snowEnabled) snow.toggle();

    // Floating toggle button — bottom right
    const btn = document.createElement('button');
    btn.id = 'snow-toggle';
    btn.title = 'Toggle snow & fog effect';
    btn.innerHTML = snowEnabled ? '❄️' : '🌤️';
    btn.setAttribute('aria-label', 'Toggle snow');

    Object.assign(btn.style, {
      position: 'fixed',
      bottom: '1.5rem',
      right: '1.5rem',
      zIndex: '9999',
      width: '44px',
      height: '44px',
      borderRadius: '50%',
      border: '1px solid rgba(255,255,255,0.12)',
      background: 'rgba(13,13,16,0.80)',
      backdropFilter: 'blur(12px)',
      fontSize: '1.2rem',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
      transition: 'transform 0.2s, box-shadow 0.2s',
      lineHeight: '1',
    });

    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'scale(1.15)';
      btn.style.boxShadow = '0 6px 28px rgba(124,106,247,0.5)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
    });
    btn.addEventListener('click', () => {
      snow.toggle();
      const isOn = snow.canvas.style.display !== 'none';
      btn.innerHTML = isOn ? '❄️' : '🌤️';
      localStorage.setItem('snow', isOn ? 'on' : 'off');
    });

    document.body.appendChild(btn);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();