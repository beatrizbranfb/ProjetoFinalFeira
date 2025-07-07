document.addEventListener('DOMContentLoaded', function() {

    const addProductBtn = document.getElementById('addProductBtn');
    const addProductModal = document.getElementById('addProductModal');
    
    const closeButtons = document.querySelectorAll('.close-modal');

    function openModal() {
        if (addProductModal) {
            addProductModal.style.display = 'block';
        }
    }

    function closeModal() {
        if (addProductModal) {
            addProductModal.style.display = 'none';
        }
    }

    if (addProductBtn) {
        addProductBtn.addEventListener('click', openModal);
    }

    closeButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });
});


