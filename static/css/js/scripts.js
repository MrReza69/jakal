// مثال: افزودن انیمیشن به دکمه‌ها
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.classList.add('animate__pulse');
    });
    button.addEventListener('mouseleave', () => {
        button.classList.remove('animate__pulse');
    });
});