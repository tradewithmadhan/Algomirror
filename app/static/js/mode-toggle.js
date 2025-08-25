// Mode toggle functionality for AlgoMirror
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }
    
    // Initialize mode toggle functionality
    function initModeToggle() {
        // Find all theme toggle buttons
        const themeToggles = document.querySelectorAll('[data-theme-toggle]');
        
        themeToggles.forEach(toggle => {
            toggle.addEventListener('click', handleThemeToggle);
        });
        
        // Update UI to reflect current theme
        updateThemeUI();
        
        // Listen for theme changes
        window.addEventListener('themechange', updateThemeUI);
    }
    
    // Handle theme toggle button clicks
    function handleThemeToggle(event) {
        event.preventDefault();
        const button = event.currentTarget;
        const newTheme = button.getAttribute('data-theme-toggle');
        
        if (newTheme && window.AlgoMirrorTheme) {
            window.AlgoMirrorTheme.setTheme(newTheme);
        } else if (window.AlgoMirrorTheme) {
            // If no specific theme, toggle between light/dark
            window.AlgoMirrorTheme.toggleTheme();
        }
    }
    
    // Update UI elements to reflect current theme
    function updateThemeUI() {
        if (!window.AlgoMirrorTheme) return;
        
        const currentTheme = window.AlgoMirrorTheme.getCurrentTheme();
        const savedTheme = window.AlgoMirrorTheme.getSavedTheme();
        
        // Update theme indicator in navbar or settings
        const themeIndicator = document.querySelector('[data-theme-indicator]');
        if (themeIndicator) {
            themeIndicator.textContent = currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1);
        }
        
        // Update active state of theme buttons
        const themeButtons = document.querySelectorAll('[data-theme-toggle]');
        themeButtons.forEach(button => {
            const buttonTheme = button.getAttribute('data-theme-toggle');
            const isActive = (buttonTheme === savedTheme) || 
                           (buttonTheme === 'auto' && savedTheme === 'auto');
            
            button.classList.toggle('active', isActive);
            button.setAttribute('aria-pressed', isActive.toString());
        });
        
        // Update theme icon if present
        updateThemeIcon(currentTheme);
    }
    
    // Update theme icon based on current theme
    function updateThemeIcon(theme) {
        const themeIcon = document.querySelector('[data-theme-icon]');
        if (!themeIcon) return;
        
        // Clear existing classes
        themeIcon.classList.remove('theme-light', 'theme-dark', 'theme-auto');
        
        // Add current theme class
        themeIcon.classList.add(`theme-${theme}`);
        
        // Update icon content (if using SVG or icon font)
        const iconSvg = themeIcon.querySelector('svg');
        if (iconSvg) {
            // You can update SVG path here based on theme
            updateIconSvg(iconSvg, theme);
        }
    }
    
    // Update SVG icon based on theme
    function updateIconSvg(svg, theme) {
        const paths = {
            light: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z',
            dark: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z',
            auto: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z'
        };
        
        const path = svg.querySelector('path');
        if (path && paths[theme]) {
            path.setAttribute('d', paths[theme]);
        }
    }
    
    // Add keyboard support
    function addKeyboardSupport() {
        document.addEventListener('keydown', function(event) {
            // Toggle theme with Ctrl/Cmd + Shift + T
            if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'T') {
                event.preventDefault();
                if (window.AlgoMirrorTheme) {
                    window.AlgoMirrorTheme.toggleTheme();
                }
            }
        });
    }
    
    // Add system theme detection
    function addSystemThemeDetection() {
        if (!window.matchMedia) return;
        
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        // Listen for changes in system theme preference
        function handleSystemThemeChange(e) {
            if (window.AlgoMirrorTheme && 
                window.AlgoMirrorTheme.getSavedTheme() === 'auto') {
                updateThemeUI();
            }
        }
        
        // Add listener (modern way)
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', handleSystemThemeChange);
        } else {
            // Fallback for older browsers
            mediaQuery.addListener(handleSystemThemeChange);
        }
    }
    
    // Initialize everything
    ready(function() {
        initModeToggle();
        addKeyboardSupport();
        addSystemThemeDetection();
        
        // Announce keyboard shortcut in console (development mode)
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            console.log('💡 AlgoMirror Theme: Press Ctrl+Shift+T (or Cmd+Shift+T) to toggle theme');
        }
    });
    
    // Export for manual initialization if needed
    window.AlgoMirrorModeToggle = {
        init: initModeToggle,
        updateUI: updateThemeUI
    };
})();