/* ============================================
   PORTFOLIO — MAIN JAVASCRIPT
   ============================================ */

const canvas = document.getElementById('snowfall');
const ctx = canvas.getContext('2d');
let width, height, flakes = [];

function init() {
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;
  flakes = Array.from({ length: 100 }, () => ({
    x: Math.random() * width,
    y: Math.random() * height,
    r: Math.random() * 3 + 1, // radius
    d: Math.random() * 1 // density/speed
  }));
}

function draw() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
  ctx.beginPath();
  flakes.forEach(f => {
    ctx.moveTo(f.x, f.y);
    ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2, true);
  });
  ctx.fill();
  update();
}

function update() {
  flakes.forEach(f => {
    f.y += Math.pow(f.d, 2) + 1;
    f.x += Math.sin(f.y / 50);
    if (f.y > height) {
      f.y = -10;
      f.x = Math.random() * width;
    }
  });
  requestAnimationFrame(draw);
}

window.addEventListener('resize', init);
init();
draw();

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
