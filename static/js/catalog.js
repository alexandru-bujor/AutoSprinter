document.querySelectorAll('.product').forEach(product => {
    const mainImg = product.querySelector('figure img');
    const originalSrc = mainImg.src;
    product.querySelectorAll('.brazzers_button').forEach(button => {
        const newSrc = button.dataset.altSrc;
        button.addEventListener('mouseenter', () => {
            mainImg.src = newSrc;
        });
        button.addEventListener('mouseleave', () => {
            mainImg.src = originalSrc;
        });
    });
});
