document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Mark lesson as completed
    const markAsCompleted = document.getElementById('mark-lesson-completed');
    if (markAsCompleted) {
        markAsCompleted.addEventListener('click', function() {
            const lessonId = this.getAttribute('data-lesson-id');
            
            fetch(`/lessons/${lessonId}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Change button appearance and disable it
                    this.classList.remove('btn-primary');
                    this.classList.add('btn-success');
                    this.innerHTML = '<i class="fas fa-check"></i> Completed';
                    this.disabled = true;
                    
                    // Show success notification
                    const toast = new bootstrap.Toast(document.getElementById('completion-toast'));
                    toast.show();
                } else {
                    alert(data.message || 'Failed to mark lesson as completed');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while marking the lesson as completed');
            });
        });
    }
    
    // Handle mobile navigation menu
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebarMenu = document.getElementById('sidebar-menu');
    
    if (mobileMenuToggle && sidebarMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebarMenu.classList.toggle('show');
        });
    }
    
    // Auto-resize textareas
    document.querySelectorAll('textarea.auto-resize').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Initial adjustment
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    });
});
