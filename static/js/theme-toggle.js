/**
 * Theme Toggle - Manual Dark/Light Mode Control
 * Xer Project
 */

(function () {
    'use strict';

    const THEME_KEY = 'xer-theme';
    const THEME_LIGHT = 'light';
    const THEME_DARK = 'dark';

    /**
     * Get current theme from localStorage or default to light
     */
    function getCurrentTheme() {
        return localStorage.getItem(THEME_KEY) || THEME_LIGHT;
    }

    /**
     * Apply theme to document
     */
    function applyTheme(theme) {
        if (theme === THEME_DARK) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }

    /**
     * Save theme preference
     */
    function saveTheme(theme) {
        localStorage.setItem(THEME_KEY, theme);
    }

    /**
     * Toggle between light and dark theme
     */
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === THEME_LIGHT ? THEME_DARK : THEME_LIGHT;

        applyTheme(newTheme);
        saveTheme(newTheme);
        updateToggleButton(newTheme);
    }

    /**
     * Update toggle button appearance
     */
    function updateToggleButton(theme) {
        const button = document.getElementById('theme-toggle');
        if (!button) return;

        if (theme === THEME_DARK) {
            button.innerHTML = '☀️';
            button.setAttribute('aria-label', 'Mudar para modo claro');
        } else {
            button.innerHTML = '🌙';
            button.setAttribute('aria-label', 'Mudar para modo escuro');
        }
    }

    /**
     * Initialize theme on page load
     */
    function initTheme() {
        const theme = getCurrentTheme();
        applyTheme(theme);
        updateToggleButton(theme);

        // Add event listener to toggle button
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.addEventListener('click', toggleTheme);
        }
    }

    // Apply theme immediately (before page renders) to avoid flash
    applyTheme(getCurrentTheme());

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    // Expose toggle function globally for inline usage if needed
    window.toggleTheme = toggleTheme;
})();
