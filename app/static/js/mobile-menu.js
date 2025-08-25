// Mobile menu functionality for AlgoMirror
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
    
    // Initialize mobile menu
    function initMobileMenu() {
        const drawer = document.getElementById('main-drawer');
        const drawerToggle = document.querySelector('[for="main-drawer"]');
        const drawerOverlay = document.querySelector('.drawer-overlay');
        const menuLinks = document.querySelectorAll('.drawer-side .menu a');
        
        if (!drawer || !drawerToggle) return;
        
        // Close menu when clicking overlay
        if (drawerOverlay) {
            drawerOverlay.addEventListener('click', closeMobileMenu);
        }
        
        // Close menu when clicking menu links (on mobile)
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 1024) { // lg breakpoint
                    setTimeout(closeMobileMenu, 150); // Small delay for better UX
                }
            });
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && drawer.checked) {
                closeMobileMenu();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', handleResize);
        
        // Prevent body scroll when menu is open
        drawer.addEventListener('change', function() {
            document.body.style.overflow = drawer.checked ? 'hidden' : '';
        });
    }
    
    // Close mobile menu
    function closeMobileMenu() {
        const drawer = document.getElementById('main-drawer');
        if (drawer) {
            drawer.checked = false;
            document.body.style.overflow = '';
        }
    }
    
    // Open mobile menu
    function openMobileMenu() {
        const drawer = document.getElementById('main-drawer');
        if (drawer) {
            drawer.checked = true;
        }
    }
    
    // Handle window resize
    function handleResize() {
        // Close mobile menu if window becomes large
        if (window.innerWidth >= 1024) { // lg breakpoint
            closeMobileMenu();
        }
    }
    
    // Toggle mobile menu
    function toggleMobileMenu() {
        const drawer = document.getElementById('main-drawer');
        if (drawer) {
            if (drawer.checked) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        }
    }
    
    // Add touch gestures (swipe to close)
    function addTouchGestures() {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;
        
        const drawerSide = document.querySelector('.drawer-side');
        if (!drawerSide) return;
        
        // Touch start
        drawerSide.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            isDragging = true;
        }, { passive: true });
        
        // Touch move
        drawerSide.addEventListener('touchmove', function(e) {
            if (!isDragging) return;
            
            currentX = e.touches[0].clientX;
            const diffX = startX - currentX;
            
            // If swiping left significantly, close menu
            if (diffX > 50) {
                closeMobileMenu();
                isDragging = false;
            }
        }, { passive: true });
        
        // Touch end
        drawerSide.addEventListener('touchend', function() {
            isDragging = false;
        }, { passive: true });
    }
    
    // Add accessibility improvements
    function addA11yImprovements() {
        const drawerToggle = document.querySelector('[for="main-drawer"]');
        const drawer = document.getElementById('main-drawer');
        
        if (!drawerToggle || !drawer) return;
        
        // Add ARIA attributes
        drawerToggle.setAttribute('aria-expanded', 'false');
        drawerToggle.setAttribute('aria-controls', 'mobile-menu');
        
        // Update aria-expanded when menu state changes
        drawer.addEventListener('change', function() {
            drawerToggle.setAttribute('aria-expanded', drawer.checked.toString());
        });
        
        // Add role to menu
        const menu = document.querySelector('.drawer-side .menu');
        if (menu) {
            menu.setAttribute('role', 'navigation');
            menu.setAttribute('aria-label', 'Main navigation');
        }
    }
    
    // Handle focus management
    function handleFocusManagement() {
        const drawer = document.getElementById('main-drawer');
        const drawerToggle = document.querySelector('[for="main-drawer"]');
        const firstMenuItem = document.querySelector('.drawer-side .menu a');
        
        if (!drawer || !drawerToggle) return;
        
        drawer.addEventListener('change', function() {
            if (drawer.checked) {
                // Menu opened - focus first menu item
                setTimeout(() => {
                    if (firstMenuItem) {
                        firstMenuItem.focus();
                    }
                }, 100);
            } else {
                // Menu closed - return focus to toggle button
                setTimeout(() => {
                    drawerToggle.focus();
                }, 100);
            }
        });
        
        // Trap focus within menu when open
        document.addEventListener('keydown', function(event) {
            if (!drawer.checked || event.key !== 'Tab') return;
            
            const menuItems = document.querySelectorAll('.drawer-side .menu a, .drawer-side .menu button');
            const firstItem = menuItems[0];
            const lastItem = menuItems[menuItems.length - 1];
            
            if (event.shiftKey) {
                // Shift + Tab
                if (document.activeElement === firstItem) {
                    event.preventDefault();
                    lastItem.focus();
                }
            } else {
                // Tab
                if (document.activeElement === lastItem) {
                    event.preventDefault();
                    firstItem.focus();
                }
            }
        });
    }
    
    // Initialize everything
    ready(function() {
        initMobileMenu();
        addTouchGestures();
        addA11yImprovements();
        handleFocusManagement();
    });
    
    // Export for manual control
    window.AlgoMirrorMobileMenu = {
        open: openMobileMenu,
        close: closeMobileMenu,
        toggle: toggleMobileMenu
    };
    
})();