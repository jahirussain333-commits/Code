gsap.registerPlugin(ScrollTrigger);

const isTouch = window.matchMedia("(hover: none), (pointer: coarse)").matches;
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------------------------------------------
   Smooth scroll (Lenis) wired into GSAP ticker
--------------------------------------------- */
let lenis;
if (!prefersReducedMotion) {
  lenis = new Lenis({ duration: 1.1, smoothWheel: true });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
}

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (e) => {
    const target = document.querySelector(link.getAttribute("href"));
    if (!target) return;
    e.preventDefault();
    if (lenis) lenis.scrollTo(target, { offset: -20 });
    else target.scrollIntoView({ behavior: "smooth" });
  });
});

/* ---------------------------------------------
   Preloader
--------------------------------------------- */
const preloader = document.querySelector(".preloader");
const preloaderNum = document.getElementById("preloader-num");
const counter = { val: 0 };

const introTl = gsap.timeline({
  onComplete: () => {
    document.body.classList.add("loaded");
    ScrollTrigger.refresh();
  },
});

introTl.to(counter, {
  val: 100,
  duration: 1.6,
  ease: "power2.inOut",
  onUpdate: () => (preloaderNum.textContent = Math.floor(counter.val)),
});

introTl.to(preloader, {
  yPercent: -100,
  duration: 0.9,
  ease: "power4.inOut",
}, "+=0.1");

introTl.to(
  ".hero .line-inner",
  { y: 0, duration: 1, ease: "power4.out", stagger: 0.08 },
  "-=0.6"
);

introTl.to(
  ".hero__sub, .hero__meta",
  { opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.1 },
  "-=0.5"
);

/* ---------------------------------------------
   Nav hide/show + solid bg past hero
--------------------------------------------- */
ScrollTrigger.create({
  start: 100,
  onUpdate: (self) => {
    document.querySelector(".nav").classList.toggle("is-scrolled", self.scroll() > 100);
  },
});

/* ---------------------------------------------
   Scroll reveals
--------------------------------------------- */
gsap.utils.toArray(".reveal-up").forEach((el) => {
  gsap.to(el, {
    opacity: 1,
    y: 0,
    duration: 1,
    ease: "power3.out",
    scrollTrigger: { trigger: el, start: "top 88%" },
  });
});

gsap.utils.toArray(".reveal-clip").forEach((el) => {
  gsap.to(el, {
    clipPath: "inset(0 0 0% 0)",
    duration: 1.2,
    ease: "power4.inOut",
    scrollTrigger: { trigger: el, start: "top 80%" },
  });
});

/* Split heading lines into words for staggered reveal */
document.querySelectorAll(".split-lines").forEach((heading) => {
  const words = heading.textContent.trim().split(/\s+/);
  heading.innerHTML = words
    .map((w) => `<span class="word"><span class="word-inner">${w}</span></span>`)
    .join(" ");
  heading.querySelectorAll(".word").forEach((w) => (w.style.cssText = "display:inline-block;overflow:hidden;"));
  heading.querySelectorAll(".word-inner").forEach((w) => (w.style.cssText += "display:inline-block;transform:translateY(110%);"));

  gsap.to(heading.querySelectorAll(".word-inner"), {
    y: 0,
    duration: 0.9,
    ease: "power3.out",
    stagger: 0.02,
    scrollTrigger: { trigger: heading, start: "top 85%" },
  });
});

/* ---------------------------------------------
   Animated stat counters
--------------------------------------------- */
gsap.utils.toArray(".stat__num").forEach((el) => {
  const target = parseInt(el.dataset.count, 10);
  const obj = { val: 0 };
  ScrollTrigger.create({
    trigger: el,
    start: "top 90%",
    once: true,
    onEnter: () => {
      gsap.to(obj, {
        val: target,
        duration: 1.6,
        ease: "power2.out",
        onUpdate: () => (el.textContent = Math.floor(obj.val)),
      });
    },
  });
});

/* ---------------------------------------------
   Marquee infinite scroll
--------------------------------------------- */
const marqueeTrack = document.querySelector(".marquee__track");
if (marqueeTrack) {
  const marqueeTween = gsap.to(marqueeTrack, {
    xPercent: -50,
    duration: 22,
    ease: "none",
    repeat: -1,
  });
  marqueeTrack.parentElement.addEventListener("mouseenter", () => marqueeTween.timeScale(0.15));
  marqueeTrack.parentElement.addEventListener("mouseleave", () => marqueeTween.timeScale(1));
}

/* ---------------------------------------------
   Custom cursor
--------------------------------------------- */
if (!isTouch) {
  const dot = document.querySelector(".cursor-dot");
  const ring = document.querySelector(".cursor-ring");

  const dotX = gsap.quickTo(dot, "x", { duration: 0.1, ease: "power3.out" });
  const dotY = gsap.quickTo(dot, "y", { duration: 0.1, ease: "power3.out" });
  const ringX = gsap.quickTo(ring, "x", { duration: 0.4, ease: "power3.out" });
  const ringY = gsap.quickTo(ring, "y", { duration: 0.4, ease: "power3.out" });

  window.addEventListener("mousemove", (e) => {
    dotX(e.clientX);
    dotY(e.clientY);
    ringX(e.clientX);
    ringY(e.clientY);
  });

  document.querySelectorAll('[data-cursor="link"]').forEach((el) => {
    el.addEventListener("mouseenter", () => ring.classList.add("is-hover"));
    el.addEventListener("mouseleave", () => ring.classList.remove("is-hover"));
  });

  document.querySelectorAll('[data-cursor="view"]').forEach((el) => {
    el.addEventListener("mouseenter", () => ring.classList.add("is-hover", "is-view"));
    el.addEventListener("mouseleave", () => ring.classList.remove("is-hover", "is-view"));
  });
}

/* ---------------------------------------------
   Magnetic buttons
--------------------------------------------- */
if (!isTouch) {
  document.querySelectorAll(".magnetic").forEach((el) => {
    const strength = 0.4;
    const moveX = gsap.quickTo(el, "x", { duration: 0.5, ease: "power3.out" });
    const moveY = gsap.quickTo(el, "y", { duration: 0.5, ease: "power3.out" });

    el.addEventListener("mousemove", (e) => {
      const rect = el.getBoundingClientRect();
      const relX = e.clientX - rect.left - rect.width / 2;
      const relY = e.clientY - rect.top - rect.height / 2;
      moveX(relX * strength);
      moveY(relY * strength);
    });

    el.addEventListener("mouseleave", () => {
      moveX(0);
      moveY(0);
    });
  });
}
