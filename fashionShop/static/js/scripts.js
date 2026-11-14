window.addEventListener('DOMContentLoaded', initPage);

function initPage() {
    initSearchForm();
}

function initSearchForm() {
    const searchForm = document.getElementById('search-form');
    const searchToggle = document.querySelector('.search-toggle');
    const searchInput = searchForm.querySelector('input');

    searchToggle.addEventListener('click', () => {
        if (!searchForm.classList.contains('expand')) {
            return;
        }
        
        searchInput.value = '';
        searchInput.focus();
    });
}