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
   ============================================ */

class SnowEffect {
  constructor() {
    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.flakes = [];
    this.count = 120; // number of snowflakes

    // Canvas styles — fixed, behind everything, pointer-events off
    Object.assign(this.canvas.style, {
      position: 'fixed',
      top: '0', left: '0',
      width: '100%', height: '100%',
      pointerEvents: 'none',
      zIndex: '9998',
      opacity: '0.75',
    });

    this.canvas.id = 'snow-canvas';
    document.body.appendChild(this.canvas);

    this.resize();
    this.init();
    this.animate();

    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.W = this.canvas.width = window.innerWidth;
    this.H = this.canvas.height = window.innerHeight;
  }

  // Create one snowflake with random properties
  createFlake() {
    return {
      x: Math.random() * this.W,
      y: Math.random() * this.H - this.H,  // start above viewport
      r: Math.random() * 3.5 + 0.8,        // radius 0.8–4.3px
      speed: Math.random() * 1.2 + 0.4,        // fall speed
      drift: Math.random() * 0.8 - 0.4,        // horizontal drift
      angle: Math.random() * Math.PI * 2,      // wobble phase
      wobble: Math.random() * 0.03 + 0.005,    // wobble speed
      opacity: Math.random() * 0.6 + 0.3,
    };
  }

  init() {
    // Spread flakes across full height initially
    for (let i = 0; i < this.count; i++) {
      const f = this.createFlake();
      f.y = Math.random() * this.H; // fill screen on start
      this.flakes.push(f);
    }
  }

  draw() {
    this.ctx.clearRect(0, 0, this.W, this.H);

    this.flakes.forEach(f => {
      // Wobble horizontally
      f.angle += f.wobble;
      f.x += Math.sin(f.angle) * 0.6 + f.drift;
      f.y += f.speed;

      // Reset when off screen
      if (f.y > this.H + 10 || f.x < -20 || f.x > this.W + 20) {
        Object.assign(f, this.createFlake());
        f.y = -5;
      }

      // Draw snowflake — soft glowing circle
      const grad = this.ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r);
      grad.addColorStop(0, `rgba(255,255,255,${f.opacity})`);
      grad.addColorStop(0.5, `rgba(220,210,255,${f.opacity * 0.7})`);
      grad.addColorStop(1, `rgba(180,160,255,0)`);

      this.ctx.beginPath();
      this.ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
      this.ctx.fillStyle = grad;
      this.ctx.fill();
    });
  }

  animate() {
    this.draw();
    this._raf = requestAnimationFrame(() => this.animate());
  }

  // Toggle on/off
  toggle() {
    if (this._paused) {
      this._paused = false;
      this.animate();
      this.canvas.style.display = 'block';
    } else {
      this._paused = true;
      cancelAnimationFrame(this._raf);
      this.canvas.style.display = 'none';
    }
  }

  destroy() {
    cancelAnimationFrame(this._raf);
    this.canvas.remove();
  }
}

// ── Init Snow + Toggle Button ─────────────────
(function initSnow() {
  // Only init after DOM is ready
  const start = () => {
    // Check if user previously disabled snow
    const snowEnabled = localStorage.getItem('snow') !== 'off';

    const snow = new SnowEffect();
    if (!snowEnabled) snow.toggle(); // start hidden if disabled

    // Create floating toggle button
    const btn = document.createElement('button');
    btn.id = 'snow-toggle';
    btn.title = 'Toggle snow effect';
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
      background: 'rgba(13,13,16,0.75)',
      backdropFilter: 'blur(10px)',
      fontSize: '1.2rem',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
      transition: 'transform 0.2s, box-shadow 0.2s',
      lineHeight: '1',
    });

    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'scale(1.15)';
      btn.style.boxShadow = '0 6px 25px rgba(124,106,247,0.4)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = '0 4px 20px rgba(0,0,0,0.4)';
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