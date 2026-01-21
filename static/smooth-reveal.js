// Smooth scroll reveal animation
// Usage: add 'js-loaded' to <body> and use .reveal-on-scroll etc.
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('js-loaded');
    const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-on-scroll, .reveal-scroll-left, .reveal-scroll-right');
    const options = {
        threshold: 0.15
    };
    const observer = new window.IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            } else {
                entry.target.classList.remove('active');
            }
        });
    }, options);
    reveals.forEach(function(el) {
        observer.observe(el);
    });
});
