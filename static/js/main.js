document.addEventListener('DOMContentLoaded', function() {
    // Включение подсказок
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Включение всплывающих окон
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Урок завершен
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

                    this.classList.remove('btn-primary');
                    this.classList.add('btn-success');
                    this.innerHTML = '<i class="fas fa-check"></i> Completed';
                    this.disabled = true;
                    
                    // Уведомление об успешном выполнении
                    const toast = new bootstrap.Toast(document.getElementById('completion-toast'));
                    toast.show();
                } else {
                    alert(data.message || 'Не удалось отметить урок как завершенный');
                }
            })

            .catch((error) => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отметке урока как завершенного');
            });
        });
    }
    
    // Для мобильной версии
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebarMenu = document.getElementById('sidebar-menu');
    
    if (mobileMenuToggle && sidebarMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebarMenu.classList.toggle('show');
        });
    }
    
    // Автоматическое изсмение текста
    document.querySelectorAll('textarea.auto-resize').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });

        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    });
});
