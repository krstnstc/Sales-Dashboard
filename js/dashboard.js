/**
 * Sales Analytics Dashboard - Main JavaScript
 * A modern, accessible, and interactive dashboard for sales analytics
 */

// Configuration object for easy customization
const config = {
    // Animation settings
    animation: {
        duration: 300,
        easing: 'ease-in-out',
        visibleThreshold: 0.8
    },
    
    // Chart settings
    charts: {
        animationOffset: 0.7, // Percentage of viewport height to trigger animation
        lazyLoadThreshold: 0 // Pixels from viewport to start loading images
    },
    
    // API endpoints (if applicable)
    api: {
        baseUrl: '/api',
        endpoints: {
            salesData: '/sales',
            customerData: '/customers'
        }
    }
};

// Theme Manager removed - using light theme only

/**
 * Navigation Manager - Handles sidebar navigation and mobile menu
 */
class NavigationManager {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebar-toggle');
        this.navLinks = document.querySelectorAll('.sidebar-nav-link');
        this.sections = document.querySelectorAll('.section');
        this.init();
    }
    
    init() {
        // Set up sidebar toggle for mobile
        if (this.sidebarToggle) {
            this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        }
        
        // Set up navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
        
        // Handle window resize for responsive behavior
        window.addEventListener('resize', () => this.handleResize());
        
        // Initialize first section as active
        this.setActiveSection('overview');
    }
    
    toggleSidebar(forceClose = false) {
        const isExpanded = this.sidebarToggle.getAttribute('aria-expanded') === 'true';
        const shouldClose = forceClose || isExpanded;
        
        this.sidebarToggle.setAttribute('aria-expanded', !shouldClose);
        this.sidebar.classList.toggle('collapsed', shouldClose);
        
        // Update aria-label for better screen reader feedback
        this.sidebarToggle.setAttribute(
            'aria-label', 
            shouldClose ? 'Open navigation menu' : 'Close navigation menu'
        );
    }
    
    handleNavClick(e) {
        e.preventDefault();
        const sectionId = e.currentTarget.getAttribute('data-section');
        
        // Update active states
        this.navLinks.forEach(link => {
            link.classList.toggle('active', link === e.currentTarget);
            link.setAttribute('aria-selected', link === e.currentTarget);
        });
        
        // Show the selected section
        this.setActiveSection(sectionId);
        
        // Close sidebar on mobile after selection
        if (window.innerWidth < 992) {
            this.toggleSidebar(true);
        }
        
        // Update URL hash without scrolling
        history.pushState(null, '', `#${sectionId}`);
    }
    
    setActiveSection(sectionId) {
        this.sections.forEach(section => {
            const isActive = section.id === sectionId;
            section.hidden = !isActive;
            section.setAttribute('aria-hidden', !isActive);
            
            if (isActive) {
                section.classList.add('active');
                // Focus the section for keyboard users
                section.focus();
            } else {
                section.classList.remove('active');
            }
        });
    }
    
    handleResize() {
        // Automatically show sidebar on larger screens
        if (window.innerWidth >= 992) {
            this.sidebar.classList.remove('collapsed');
            this.sidebarToggle.setAttribute('aria-expanded', 'true');
        }
    }
}

/**
 * Chart Manager - Handles chart animations and interactions
 */
class ChartManager {
    constructor() {
        this.chartContainers = document.querySelectorAll('.chart-container');
        this.observer = null;
        this.init();
    }
    
    init() {
        // Set up Intersection Observer for scroll animations
        this.setupIntersectionObserver();
        
        // Set up chart interactions
        this.setupChartInteractions();
    }
    
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        this.observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateChart(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, options);
        
        // Observe all chart containers
        this.chartContainers.forEach(chart => {
            this.observer.observe(chart);
        });
    }
    
    animateChart(chartContainer) {
        chartContainer.classList.add('visible');
        
        // Animate the chart image if it exists
        const chartImg = chartContainer.querySelector('.chart-img');
        if (chartImg) {
            chartImg.style.opacity = '1';
            chartImg.style.transform = 'translateY(0)';
        }
    }
    
    setupChartInteractions() {
        // Handle chart actions (download, fullscreen, etc.)
        document.addEventListener('click', (e) => {
            const actionBtn = e.target.closest('[data-action]');
            if (!actionBtn) return;
            
            const action = actionBtn.dataset.action;
            const chartId = actionBtn.dataset.chart;
            
            switch (action) {
                case 'download':
                    this.downloadChart(chartId);
                    break;
                case 'fullscreen':
                    this.toggleFullscreen(chartId);
                    break;
            }
        });
    }
    
    downloadChart(chartId) {
        // In a real implementation, this would trigger a download
        console.log(`Downloading chart: ${chartId}`);
        // Example: window.location.href = `/api/charts/${chartId}/download`;
    }
    
    toggleFullscreen(chartId) {
        const chartContainer = document.querySelector(`[data-chart="${chartId}"]`).closest('.chart-container');
        
        if (!document.fullscreenElement) {
            chartContainer.requestFullscreen().catch(err => {
                console.error(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    }
}

/**
 * Dashboard - Main application class
 */
class Dashboard {
    constructor() {
        this.themeManager = null;
        this.navManager = null;
        this.chartManager = null;
        this.init();
    }
    
    init() {
        // Initialize navigation manager
        this.navManager = new NavigationManager();
        
        // Initialize chart manager
        this.chartManager = new ChartManager();
        
        // Set current date
        this.setCurrentDate();
        
        // Set up any additional event listeners
        this.setupEventListeners();
    }
    
    setCurrentDate() {
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        
        const currentDate = new Date();
        const dateElement = document.getElementById('current-date');
        
        if (dateElement) {
            dateElement.textContent = currentDate.toLocaleDateString('en-US', options);
        }
    }
    
    setupEventListeners() {
        // Handle hash changes for direct linking to sections
        window.addEventListener('hashchange', () => {
            const sectionId = window.location.hash.substring(1);
            if (sectionId) {
                this.navManager.setActiveSection(sectionId);
            }
        });
        
        // Theme change handling removed
    }
}

// Initialize the dashboard when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new Dashboard();
    
    // Make dashboard instance available globally for debugging if needed
    window.dashboard = dashboard;
});
