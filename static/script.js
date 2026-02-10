// Добавьте в начало файла
document.addEventListener('DOMContentLoaded', function() {
    // Быстрая установка темы до полной загрузки
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Показываем контент после загрузки
    setTimeout(() => {
        document.querySelector('.app-container').classList.add('loaded');
    }, 50);
    
    // Плавные переходы для всех элементов
    const style = document.createElement('style');
    style.textContent = `
        * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, opacity 0.3s ease !important;
        }
        
        .task-card, .quick-add-card, .tasks-container, .auth-card {
            transition: all 0.3s ease !important;
        }
    `;
    document.head.appendChild(style);
});

// Обновите функцию переключения темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Плавное переключение
    document.documentElement.style.transition = 'all 0.3s ease';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    setTimeout(() => {
        document.documentElement.style.transition = '';
    }, 300);
}

// Добавим функции для темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// PWA Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(() => console.log('SW registered'))
        .catch(err => console.log('SW registration failed:', err));
}

// Проверка установки PWA
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    const installButton = document.createElement('button');
    installButton.textContent = 'Установить приложение';
    installButton.className = 'install-btn';
    installButton.onclick = () => e.prompt();
    
    document.body.appendChild(installButton);
});

// Плавные переходы при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Быстрая установка темы
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Показываем контент плавно
    setTimeout(() => {
        document.querySelector('.app-container').classList.add('loaded');
    }, 50);
});

// Функция переключения темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Плавные переходы при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Показываем контент плавно
    setTimeout(() => {
        document.querySelector('.app-container').classList.add('loaded');
    }, 50);
});

// Функция переключения темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Функция для формы "Добавить подробно"
function toggleExtendedForm() {
    const form = document.getElementById('extendedForm');
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

// PWA регистрация
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}

// Добавьте эту функцию
function toggleExtendedForm() {
    const form = document.getElementById('extendedForm');
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

// Остальной код оставьте без изменений