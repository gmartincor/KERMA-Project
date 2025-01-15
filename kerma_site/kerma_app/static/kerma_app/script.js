function toggleTheme() {
    var body = document.body;
    var toggleBtn = document.querySelector('.theme-toggle');

    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
        toggleBtn.innerHTML = "🌙 Dark Mode";
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
        toggleBtn.innerHTML = "☀️ Light Mode";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var savedTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(savedTheme + '-theme');

    var toggleBtn = document.querySelector('.theme-toggle');
    if (savedTheme === 'dark') {
        toggleBtn.innerHTML = "☀️ Light Mode";
    } else {
        toggleBtn.innerHTML = "🌙 Dark Mode";
    }
});
