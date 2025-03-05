// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize date picker if exists
    const datePickers = document.querySelectorAll('input[type="date"]');
    datePickers.forEach(picker => {
        picker.min = new Date().toISOString().split('T')[0];
    });

    // Flash message auto-hide
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});

// Appointment status update confirmation
function confirmStatusUpdate(status, appointmentId) {
    if (confirm(`Are you sure you want to ${status} this appointment?`)) {
        window.location.href = `/appointment/${status}/${appointmentId}`;
    }
}

// Message character counter
const messageInput = document.querySelector('textarea[name="content"]');
if (messageInput) {
    const maxLength = 500;
    const counter = document.createElement('div');
    counter.className = 'text-muted small';
    messageInput.parentNode.appendChild(counter);

    messageInput.addEventListener('input', function() {
        const remaining = maxLength - this.value.length;
        counter.textContent = `${remaining} characters remaining`;
    });
}
