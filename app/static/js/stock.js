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

    const editProductBtn = document.getElementById('editProductBtn');
    const editProductModal = document.getElementById('editProductModal');

    function openModal() {
        if (editProductModal) {
            editProductModal.style.display = 'block';
        }
    }

    function closeModal() {
        if (editProductModal) {
            editProductModal.style.display = 'none';
        }
    }

    if (editProductBtn) {
        editProductBtn.addEventListener('click', openModal);
    }

    closeButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });
});


