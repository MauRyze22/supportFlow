// ================================
// FILTERS - ADVANCED FUNCTIONALITY
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ================================
    // AUTO-OPEN FILTERS IF ACTIVE
    // ================================
    const urlParams = new URLSearchParams(window.location.search);
    const hasActiveFilters = Array.from(urlParams.keys()).some(key => 
        ['q', 'categoria', 'estado', 'prioridad', 'fecha_desde', 'fecha_hasta', 'asignado'].includes(key)
    );
    
    const filterPanel = document.getElementById('filterPanel');
    if (hasActiveFilters && filterPanel) {
        filterPanel.classList.remove('hidden');
    }
    
    // ================================
    // CLEAR INDIVIDUAL FILTERS
    // ================================
    window.clearFilter = function(filterName) {
        const url = new URL(window.location);
        url.searchParams.delete(filterName);
        window.location.href = url.toString();
    };
    
    // ================================
    // CLEAR ALL FILTERS
    // ================================
    window.clearAllFilters = function() {
        const url = new URL(window.location);
        ['q', 'categoria', 'estado', 'prioridad', 'fecha_desde', 'fecha_hasta', 'asignado'].forEach(param => {
            url.searchParams.delete(param);
        });
        window.location.href = url.pathname;
    };
    
    // ================================
    // DATE RANGE VALIDATION
    // ================================
    const fechaDesde = document.querySelector('input[name="fecha_desde"]');
    const fechaHasta = document.querySelector('input[name="fecha_hasta"]');
    
    if (fechaDesde && fechaHasta) {
        fechaDesde.addEventListener('change', function() {
            fechaHasta.min = this.value;
        });
        
        fechaHasta.addEventListener('change', function() {
            fechaDesde.max = this.value;
        });
    }
    
    // ================================
    // FILTER FORM SUBMIT LOADING
    // ================================
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <svg class="animate-spin h-4 w-4 inline-block mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Filtrando...
                `;
            }
        });
    }
    
    // ================================
    // LIVE SEARCH (OPTIONAL)
    // ================================
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput && searchInput.dataset.liveSearch) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            
            searchTimeout = setTimeout(() => {
                // Aquí puedes implementar búsqueda AJAX si lo necesitas
                console.log('Searching for:', query);
            }, 500);
        });
    }
    
    console.log('✅ Filters JS initialized');
});