function toggleTheme() {
    var themeElement = document.getElementById('theme');

    // Проверяем текущую тему
    if (themeElement.getAttribute('href') === 'styles.css') {
        // Если текущая тема - светлая, переключаем на темную
        themeElement.setAttribute('href', 'dark-theme.css');
    } else {
        // Если текущая тема - темная, переключаем на светлую
        themeElement.setAttribute('href', 'styles.css');
    }
}