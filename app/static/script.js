
document.querySelectorAll('.post label').forEach(label => {
    label.addEventListener('click', () => {
        if (window.innerWidth > 768) {
            var parentElementId = label.parentElement.id
            openPost(parentElementId)
            
            setTimeout(() => {
                var targetElement = document.getElementById(parentElementId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
            , 100);
        } else {
            setTimeout(() => {
                const navHeight = document.getElementById('navigation-container').offsetHeight;
                const elementTop = label.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementTop - navHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }, 100);
}
        
    });
})
