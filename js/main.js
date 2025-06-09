/**
 * Sales Analytics Dashboard - Main JavaScript
 * 
 * This file contains all the interactive functionality for the Sales Analytics Dashboard.
 * It's organized into logical modules and includes comprehensive documentation.
 * 
 * @module main
 */

// Configuration object for easy customization
const CONFIG = {
    // Animation settings
    animation: {
        scrollOffset: 1.3,  // How much of the element needs to be visible to trigger animation
        scrollTransition: 'opacity 0.5s ease, transform 0.5s ease',
        cardHover: {
            scale: 1.1,
            rotation: '5deg',
            transition: 'transform 0.3s ease'
        }
    },
    // Responsive breakpoints
    breakpoints: {
        mobile: 768,
        tablet: 1024
    },
    // Selectors
    selectors: {
        sidebar: '.sidebar',
        section: '.section',
        navItem: '.sidebar li',
        chartContainer: '.chart-container',
        metricCard: '.metric-card',
        metricIcon: '.metric-icon',
        chartImage: '.chart-img',
        currentDate: '#current-date'
    },
    // Classes
    classes: {
        active: 'active',
        loading: 'loading',
        error: 'error'
    }
};

/**
 * Initializes the dashboard when the DOM is fully loaded
 */
function initDashboard() {
    updateCurrentDate();
    setupNavigation();
    setupAnimations();
    setupMetricCards();
    setupSmoothScrolling();
    handleResponsiveLayout();
    setupImageLoading();
}

/**
 * Updates the current date in the header
 */
function updateCurrentDate() {
    const currentDateElement = document.querySelector(CONFIG.selectors.currentDate);
    if (!currentDateElement) return;
    
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    
    try {
        currentDateElement.textContent = new Date().toLocaleDateString('en-US', options);
    } catch (error) {
        console.error('Error updating date:', error);
    }
}

/**
 * Sets up the navigation between dashboard sections
 */
function setupNavigation() {
    const navItems = document.querySelectorAll(CONFIG.selectors.navItem);
    const sections = document.querySelectorAll(CONFIG.selectors.section);

    // Set first section as active by default if none is active
    const hasActiveSection = Array.from(sections).some(section => 
        section.classList.contains(CONFIG.classes.active)
    );
    
    if (!hasActiveSection && sections.length > 0) {
        sections[0].classList.add(CONFIG.classes.active);
        navItems[0]?.classList.add(CONFIG.classes.active);
    }

    // Add click event listeners to navigation items
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            if (!sectionId) return;
            
            // Update active states
            navItems.forEach(navItem => {
                navItem.classList.toggle(CONFIG.classes.active, navItem === this);
            });
            
            sections.forEach(section => {
                section.classList.toggle(CONFIG.classes.active, section.id === sectionId);
            });
        });
    });
}

/**
 * Handles scroll animations for elements
 */
function handleScrollAnimations() {
    const chartContainers = document.querySelectorAll(CONFIG.selectors.chartContainer);
    const screenPosition = window.innerHeight / CONFIG.animation.scrollOffset;
    
    chartContainers.forEach(container => {
        const containerPosition = container.getBoundingClientRect().top;
        
        if (containerPosition < screenPosition) {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }
    });
}

/**
 * Sets up hover effects for metric cards
 */
function setupMetricCards() {
    const metricCards = document.querySelectorAll(CONFIG.selectors.metricCard);
    
    metricCards.forEach(card => {
        const icon = card.querySelector(CONFIG.selectors.metricIcon);
        if (!icon) return;
        
        card.addEventListener('mouseenter', () => {
            icon.style.transform = `scale(${CONFIG.animation.cardHover.scale}) rotate(${CONFIG.animation.cardHover.rotation})`;
            icon.style.transition = CONFIG.animation.cardHover.transition;
        });
        
        card.addEventListener('mouseleave', () => {
            icon.style.transform = 'scale(1) rotate(0)';
        });
    });
}

/**
 * Sets up smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Handles responsive layout adjustments
 */
function handleResponsiveLayout() {
    const updateSidebarHeight = () => {
        const sidebar = document.querySelector(CONFIG.selectors.sidebar);
        if (!sidebar) return;
        
        if (window.innerWidth <= CONFIG.breakpoints.mobile) {
            sidebar.style.height = 'auto';
        } else {
            sidebar.style.height = 'calc(100vh - 68px)';
        }
    };
    
    // Initial setup
    updateSidebarHeight();
    
    // Update on resize with debounce
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(updateSidebarHeight, 250);
    });
}

/**
 * Sets up loading states and error handling for images
 */
function setupImageLoading() {
    const images = document.querySelectorAll(CONFIG.selectors.chartImage);
    
    const handleImageLoad = (img, container) => {
        container.classList.remove(CONFIG.classes.loading);
    };
    
    const handleImageError = (img, container) => {
        container.classList.remove(CONFIG.classes.loading);
        container.classList.add(CONFIG.classes.error);
        
        // Only add error message if one doesn't already exist
        if (!container.querySelector('.error-message')) {
            const errorMsg = document.createElement('p');
            errorMsg.className = 'error-message';
            errorMsg.textContent = 'Failed to load image';
            errorMsg.style.color = '#dc3545';
            container.appendChild(errorMsg);
        }
    };
    
    images.forEach(img => {
        const container = img.closest(CONFIG.selectors.chartContainer);
        if (!container) return;
        
        // Add loading class
        container.classList.add(CONFIG.classes.loading);
        
        // Set up event listeners
        if (img.complete) {
            handleImageLoad(img, container);
        } else {
            img.addEventListener('load', () => handleImageLoad(img, container));
            img.addEventListener('error', () => handleImageError(img, container));
        }
    });
}

// Initialize the dashboard when the DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}

// Export for testing or potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initDashboard,
        updateCurrentDate,
        setupNavigation,
        setupAnimations,
        setupMetricCards,
        CONFIG
    };
}
