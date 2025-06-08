/**
 * ERP ROMA - JavaScript principal
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização do sistema
    console.log('ERP ROMA inicializado');
    
    // Toggle para sidebar em dispositivos móveis
    const toggleSidebar = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    
    if (toggleSidebar && sidebar) {
        toggleSidebar.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }
    
    // Fechar alertas automaticamente após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // Inicializar tooltips
    initTooltips();
    
    // Inicializar máscaras de input
    initInputMasks();
});

/**
 * Inicializa tooltips
 */
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(function(tooltip) {
        tooltip.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.textContent = text;
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = rect.top - tooltipEl.offsetHeight - 5 + 'px';
            tooltipEl.style.left = rect.left + (rect.width / 2) - (tooltipEl.offsetWidth / 2) + 'px';
            tooltipEl.style.opacity = '1';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltipEl = document.querySelector('.tooltip');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });
}

/**
 * Inicializa máscaras de input
 */
function initInputMasks() {
    // Máscara para CNPJ
    const cnpjInputs = document.querySelectorAll('.mask-cnpj');
    cnpjInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 14) {
                value = value.slice(0, 14);
            }
            
            if (value.length > 12) {
                value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2}).*/, '$1.$2.$3/$4-$5');
            } else if (value.length > 8) {
                value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d+).*/, '$1.$2.$3/$4');
            } else if (value.length > 5) {
                value = value.replace(/^(\d{2})(\d{3})(\d+).*/, '$1.$2.$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d+).*/, '$1.$2');
            }
            
            e.target.value = value;
        });
    });
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('.mask-cep');
    cepInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 8) {
                value = value.slice(0, 8);
            }
            
            if (value.length > 5) {
                value = value.replace(/^(\d{5})(\d+).*/, '$1-$2');
            }
            
            e.target.value = value;
        });
    });
    
    // Máscara para telefone
    const phoneInputs = document.querySelectorAll('.mask-phone');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            if (value.length > 10) {
                value = value.replace(/^(\d{2})(\d{5})(\d+).*/, '($1) $2-$3');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{2})(\d{4})(\d+).*/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d+).*/, '($1) $2');
            }
            
            e.target.value = value;
        });
    });
    
    // Máscara para moeda
    const currencyInputs = document.querySelectorAll('.mask-currency');
    currencyInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value === '') {
                e.target.value = '';
                return;
            }
            
            value = (parseInt(value) / 100).toFixed(2);
            e.target.value = value.replace('.', ',');
        });
    });
}

/**
 * Formata um valor para moeda brasileira
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Formata uma data para o formato brasileiro
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

/**
 * Confirma uma ação antes de executá-la
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

