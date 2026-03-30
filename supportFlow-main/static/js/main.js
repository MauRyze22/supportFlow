// ================================
// SUPPORTFLOW - MAIN JAVASCRIPT
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // ================================
    // MOBILE MENU TOGGLE
    // ================================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            
            // Cambiar icono
            const icon = mobileMenuBtn.querySelector('i');
            if (icon) {
                const isOpen = !mobileMenu.classList.contains('hidden');
                icon.setAttribute('data-lucide', isOpen ? 'x' : 'menu');
                lucide.createIcons();
            }
        });
        
        // Cerrar al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!mobileMenuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
    
    // ================================
    // TABS FUNCTIONALITY
    // ================================
    window.switchTab = function(tabName) {
        // Remover clases activas de todos los botones
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('border-violet-500', 'text-violet-400', 'bg-violet-500/10');
            btn.classList.add('border-transparent', 'text-slate-400');
        });
        
        // Ocultar todo el contenido
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });
        
        // Activar el tab clickeado
        event.target.closest('.tab-btn').classList.add('border-violet-500', 'text-violet-400', 'bg-violet-500/10');
        event.target.closest('.tab-btn').classList.remove('border-transparent', 'text-slate-400');
        
        // Mostrar contenido correspondiente
        const content = document.getElementById(tabName + '-content');
        if (content) {
            content.classList.remove('hidden');
        }
        
        // Re-inicializar iconos
        lucide.createIcons();
    };
    
    // ================================
    // AUTO-HIDE MESSAGES
    // ================================
    setTimeout(() => {
        const messages = document.querySelectorAll('[class*="animate-slideDown"]');
        messages.forEach(msg => {
            msg.style.transition = 'opacity 0.5s, transform 0.5s';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 500);
        });
    }, 5000);
    
    // ================================
    // SMOOTH SCROLL
    // ================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ================================
    // CONFIRM DELETE
    // ================================
    const deleteButtons = document.querySelectorAll('.btn-delete, [data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || '¿Estás seguro de que deseas eliminar este elemento?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // ================================
    // TEXTAREA AUTO-RESIZE
    // ================================
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const resize = () => {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        };
        
        textarea.addEventListener('input', resize);
        resize(); // Inicializar tamaño
    });
    
    // ================================
    // FORM LOADING STATE
    // ================================
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && this.checkValidity()) {
                submitBtn.disabled = true;
                
                const originalContent = submitBtn.innerHTML;
                submitBtn.innerHTML = `
                    <svg class="animate-spin h-5 w-5 inline-block mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Procesando...
                `;
                
                // Restaurar después de 10 segundos por si hay error
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalContent;
                }, 10000);
            }
        });
    });
    
    // ================================
    // KEYBOARD SHORTCUTS
    // ================================
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K para buscar
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[name="q"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Escape para cerrar modales
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('[data-modal]');
            modals.forEach(modal => modal.classList.add('hidden'));
            
            // Cerrar menú móvil
            if (mobileMenu) {
                mobileMenu.classList.add('hidden');
            }
        }
    });
    
    // ================================
    // TOOLTIPS
    // ================================
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        let tooltip = null;
        
        element.addEventListener('mouseenter', function() {
            tooltip = document.createElement('div');
            tooltip.className = 'absolute z-50 px-3 py-2 text-sm text-white bg-slate-900 rounded-lg shadow-xl border border-slate-700 whitespace-nowrap';
            tooltip.textContent = this.dataset.tooltip;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 8}px`;
            tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
        });
        
        element.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.remove();
                tooltip = null;
            }
        });
    });
    
    // ================================
    // STATISTICS COUNTER ANIMATION
    // ================================
    function animateCounter(element, target, duration = 1000) {
        const start = 0;
        const increment = target / (duration / 16); // 60fps
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
    
    // Animar números en las stats cards
    const statNumbers = document.querySelectorAll('.stat-number, [data-animate-number]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const value = parseInt(entry.target.textContent);
                if (!isNaN(value) && value > 0) {
                    entry.target.textContent = '0';
                    animateCounter(entry.target, value);
                    entry.target.dataset.animated = 'true';
                }
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(el => observer.observe(el));
    
    // ================================
    // COPY TO CLIPBOARD
    // ================================
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copiado al portapapeles', 'success');
        }).catch(() => {
            showNotification('Error al copiar', 'error');
        });
    };
    
    // ================================
    // NOTIFICATION SYSTEM
    // ================================
    window.showNotification = function(message, type = 'info') {
        const colors = {
            success: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300',
            error: 'bg-red-500/10 border-red-500/30 text-red-300',
            warning: 'bg-amber-500/10 border-amber-500/30 text-amber-300',
            info: 'bg-blue-500/10 border-blue-500/30 text-blue-300'
        };
        
        const icons = {
            success: 'check-circle',
            error: 'x-circle',
            warning: 'alert-triangle',
            info: 'info'
        };
        
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 rounded-xl p-4 backdrop-blur-sm border shadow-lg ${colors[type]} animate-slideIn max-w-md`;
        notification.innerHTML = `
            <div class="flex items-start gap-3">
                <i data-lucide="${icons[type]}" class="w-5 h-5 mt-0.5 flex-shrink-0"></i>
                <div class="flex-1">${message}</div>
                <button onclick="this.parentElement.parentElement.remove()" class="text-current opacity-60 hover:opacity-100 transition-opacity">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        lucide.createIcons();
        
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    };
    
    // ================================
    // FILTER PANEL TOGGLE
    // ================================
    window.toggleFilters = function() {
        const panel = document.getElementById('filterPanel');
        const icon = event.target.querySelector('[data-lucide]');
        
        if (panel) {
            panel.classList.toggle('hidden');
            
            if (icon) {
                const isOpen = !panel.classList.contains('hidden');
                icon.setAttribute('data-lucide', isOpen ? 'chevron-up' : 'chevron-down');
                lucide.createIcons();
            }
        }
    };
    
    // ================================
    // DROPDOWN MENUS
    // ================================
    document.querySelectorAll('[data-dropdown]').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const dropdown = trigger.nextElementSibling;
            if (dropdown) {
                dropdown.classList.toggle('hidden');
            }
        });
    });
    
    // Cerrar dropdowns al hacer clic fuera
    document.addEventListener('click', () => {
        document.querySelectorAll('[data-dropdown] + *').forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
    });
    
    // ================================
    // INITIALIZE
    // ================================
    console.log('✅ SupportFlow JS initialized');
});