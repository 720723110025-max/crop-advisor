/**
 * Admin Panel JavaScript for Crop Advisory System
 * Handles admin-specific functionality including user management,
 * system monitoring, reports, and analytics.
 */

$(document).ready(function() {
    // Initialize admin charts
    if (document.getElementById('userGrowthChart')) {
        initUserGrowthChart();
    }
    
    if (document.getElementById('systemUsageChart')) {
        initSystemUsageChart();
    }
    
    if (document.getElementById('diseaseTrendChart')) {
        initDiseaseTrendChart();
    }
    
    // Setup user management
    setupUserManagement();
    
    // Setup report generation
    setupReportGeneration();
    
    // Setup system monitoring
    setupSystemMonitoring();
    
    // Load initial stats
    loadSystemStats();
});

/**
 * Initialize User Growth Chart
 * Shows user registration trends over time
 */
function initUserGrowthChart() {
    const ctx = document.getElementById('userGrowthChart').getContext('2d');
    
    // Fetch user growth data
    fetch('/admin/api/reports/usage-trends')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error loading user growth data:', data.error);
                return;
            }
            
            const labels = data.map(item => item.date);
            const newUsers = data.map(item => item.new_users);
            const predictions = data.map(item => item.predictions);
            
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'New Users',
                        data: newUsers,
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#198754',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }, {
                        label: 'Predictions',
                        data: predictions,
                        borderColor: '#0dcaf0',
                        backgroundColor: 'rgba(13, 202, 240, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#0dcaf0',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 20
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.dataset.label}: ${context.parsed.y}`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching user growth data:', error);
            showToast('Failed to load user growth data', 'danger');
        });
}

/**
 * Initialize System Usage Chart
 * Shows distribution of system features usage
 */
function initSystemUsageChart() {
    const ctx = document.getElementById('systemUsageChart').getContext('2d');
    
    // Fetch system stats
    fetch('/admin/api/reports/system-stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error loading system stats:', data.error);
                return;
            }
            
            const chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Users', 'Disease Reports', 'Yield Predictions', 'Fertilizer Plans', 'Irrigation Schedules'],
                    datasets: [{
                        data: [
                            data.total_users || 0,
                            data.total_disease_reports || 0,
                            data.total_predictions || 0,
                            data.total_fertilizer_recs || 0,
                            data.total_irrigation || 0
                        ],
                        backgroundColor: [
                            '#198754',
                            '#dc3545',
                            '#ffc107',
                            '#0dcaf0',
                            '#6f42c1'
                        ],
                        borderWidth: 3,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true,
                                font: {
                                    size: 12
                                }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                                    return `${context.label}: ${context.parsed} (${percentage}%)`;
                                }
                            }
                        }
                    },
                    cutout: '65%'
                }
            });
            
            // Add center text
            const centerText = {
                id: 'centerText',
                beforeDraw: function(chart) {
                    const { width, height, ctx } = chart;
                    ctx.save();
                    const centerX = width / 2;
                    const centerY = height / 2 - 10;
                    
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    
                    ctx.font = 'bold 24px Inter, sans-serif';
                    ctx.fillStyle = '#212529';
                    ctx.fillText('System', centerX, centerY - 10);
                    
                    ctx.font = '14px Inter, sans-serif';
                    ctx.fillStyle = '#6c757d';
                    ctx.fillText('Total Usage', centerX, centerY + 20);
                    
                    ctx.restore();
                }
            };
            
            // Register the plugin
            Chart.register(centerText);
        })
        .catch(error => {
            console.error('Error fetching system stats:', error);
            showToast('Failed to load system stats', 'danger');
        });
}

/**
 * Initialize Disease Trend Chart
 * Shows disease detection trends
 */
function initDiseaseTrendChart() {
    const ctx = document.getElementById('diseaseTrendChart').getContext('2d');
    
    // Sample data - in production, fetch from API
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Disease Reports',
                data: [12, 19, 15, 17, 14, 22, 18, 25, 20, 16, 13, 10],
                backgroundColor: 'rgba(220, 53, 69, 0.6)',
                borderColor: '#dc3545',
                borderWidth: 2,
                borderRadius: 8
            }, {
                label: 'Verified Cases',
                data: [8, 14, 10, 12, 9, 16, 13, 18, 15, 11, 8, 6],
                backgroundColor: 'rgba(255, 193, 7, 0.6)',
                borderColor: '#ffc107',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 5
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Setup user management functionality
 * Handles user status toggling, deletion, and role management
 */
function setupUserManagement() {
    // Toggle user status (activate/deactivate)
    $('.toggle-user-status').on('click', function() {
        const userId = $(this).data('user-id');
        const statusBadge = $(this).closest('tr').find('.status-badge');
        const username = $(this).data('username');
        
        if (!confirm(`Are you sure you want to change the status of user "${username}"?`)) {
            return;
        }
        
        // Show loading state
        $(this).prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i>Processing...');
        
        fetch(`/admin/api/users/${userId}/toggle-status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update status badge
                const isActive = data.is_active;
                statusBadge
                    .removeClass('bg-success bg-danger')
                    .addClass(isActive ? 'bg-success' : 'bg-danger')
                    .text(isActive ? 'Active' : 'Inactive');
                
                // Update button text
                $(this)
                    .removeClass('btn-warning btn-success')
                    .addClass(isActive ? 'btn-warning' : 'btn-success')
                    .html(isActive ? '<i class="fas fa-ban me-1"></i>Deactivate' : '<i class="fas fa-check me-1"></i>Activate');
                
                showToast(data.message, 'success');
            } else {
                showToast('Failed to update user status', 'danger');
            }
        })
        .catch(error => {
            console.error('Error toggling user status:', error);
            showToast('An error occurred. Please try again.', 'danger');
        })
        .finally(() => {
            $(this).prop('disabled', false).html($(this).data('original-text') || 'Toggle Status');
        });
    });
    
    // Delete user
    $('.delete-user').on('click', function() {
        const userId = $(this).data('user-id');
        const username = $(this).data('username');
        
        if (!confirm(`⚠️ Are you sure you want to delete user "${username}"?\n\nThis action cannot be undone and will permanently remove all associated data.`)) {
            return;
        }
        
        // In production, implement delete API endpoint
        showToast('Delete functionality coming soon. Please use the admin panel to manage users.', 'warning');
    });
    
    // Promote to admin
    $('.promote-admin').on('click', function() {
        const userId = $(this).data('user-id');
        const username = $(this).data('username');
        
        if (!confirm(`Are you sure you want to promote "${username}" to admin?`)) {
            return;
        }
        
        // In production, implement promote API endpoint
        showToast(`User "${username}" would be promoted to admin (feature coming soon)`, 'info');
    });
}

/**
 * Setup report generation functionality
 * Handles generating and downloading reports
 */
function setupReportGeneration() {
    // Generate report button
    $('#generateReportBtn').on('click', function() {
        const reportType = $('#reportType').val();
        const dateRange = $('#dateRange').val();
        const format = $('#reportFormat').val() || 'pdf';
        
        if (!reportType) {
            showToast('Please select a report type.', 'warning');
            return;
        }
        
        if (!dateRange) {
            showToast('Please select a date range.', 'warning');
            return;
        }
        
        // Show loading state
        $(this).prop('disabled', true);
        $(this).html('<i class="fas fa-spinner fa-spin me-2"></i>Generating...');
        
        // Simulate report generation
        setTimeout(() => {
            $(this).prop('disabled', false);
            $(this).html('<i class="fas fa-file-pdf me-2"></i>Generate Report');
            
            // Show success with download link
            showToast(`📄 ${reportType.charAt(0).toUpperCase() + reportType.slice(1)} report generated successfully!`, 'success');
            
            // In production, would trigger download
            // window.location.href = `/admin/api/reports/download/${reportType}?format=${format}&range=${dateRange}`;
            
            // Show download button
            $('#downloadReportBtn').show();
        }, 2000);
    });
    
    // Download report
    $('#downloadReportBtn').on('click', function() {
        showToast('📥 Downloading report...', 'info');
        // In production, would download the generated report
        // window.location.href = `/admin/api/reports/download/${reportType}`;
    });
    
    // Export data
    $('#exportDataBtn').on('click', function() {
        const exportType = $('#exportType').val();
        const format = $('#exportFormat').val() || 'csv';
        
        if (!exportType) {
            showToast('Please select data to export.', 'warning');
            return;
        }
        
        // Show loading
        $(this).prop('disabled', true);
        $(this).html('<i class="fas fa-spinner fa-spin me-2"></i>Exporting...');
        
        setTimeout(() => {
            $(this).prop('disabled', false);
            $(this).html('<i class="fas fa-download me-2"></i>Export Data');
            showToast(`✅ Data exported as ${format.toUpperCase()} successfully!`, 'success');
            
            // In production, would trigger download
            // window.location.href = `/admin/api/data/export/${exportType}?format=${format}`;
        }, 1500);
    });
}

/**
 * Setup system monitoring
 * Handles real-time system monitoring features
 */
function setupSystemMonitoring() {
    // Refresh system stats
    $('#refreshStats').on('click', function() {
        $(this).html('<i class="fas fa-spinner fa-spin me-1"></i>Refreshing...');
        loadSystemStats();
        setTimeout(() => {
            $(this).html('<i class="fas fa-sync me-1"></i>Refresh Stats');
        }, 1000);
    });
    
    // System health check
    if ($('#systemHealth').length) {
        setInterval(checkSystemHealth, 60000); // Check every minute
        checkSystemHealth();
    }
}

/**
 * Load system statistics
 * Fetches and updates system stats on the admin dashboard
 */
function loadSystemStats() {
    fetch('/admin/api/reports/system-stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error loading system stats:', data.error);
                return;
            }
            
            // Update stats counters
            updateStatCounter('totalUsers', data.total_users);
            updateStatCounter('activeUsers', data.active_users);
            updateStatCounter('totalDiseaseReports', data.total_disease_reports);
            updateStatCounter('verifiedReports', data.verified_reports);
            updateStatCounter('totalPredictions', data.total_predictions);
            updateStatCounter('totalCrops', data.total_crops);
            updateStatCounter('totalFertilizerRecs', data.total_fertilizer_recs);
            updateStatCounter('totalIrrigation', data.total_irrigation);
        })
        .catch(error => {
            console.error('Error loading system stats:', error);
        });
}

/**
 * Update a stat counter with animation
 */
function updateStatCounter(elementId, value) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const currentValue = parseInt(element.textContent) || 0;
    if (currentValue === value) return;
    
    // Animate counter
    let start = 0;
    const duration = 500;
    const step = Math.max(1, Math.floor(value / 30));
    
    const interval = setInterval(() => {
        start += step;
        if (start >= value) {
            start = value;
            clearInterval(interval);
        }
        element.textContent = start;
    }, duration / 30);
}

/**
 * Check system health
 * Verifies database connection and system status
 */
function checkSystemHealth() {
    fetch('/admin/api/health-check')
        .then(response => response.json())
        .then(data => {
            const statusIndicator = $('#systemHealth');
            if (data.status === 'healthy') {
                statusIndicator
                    .removeClass('bg-danger bg-warning')
                    .addClass('bg-success')
                    .text('✅ System Healthy');
            } else if (data.status === 'degraded') {
                statusIndicator
                    .removeClass('bg-success bg-danger')
                    .addClass('bg-warning')
                    .text('⚠️ Degraded Performance');
            } else {
                statusIndicator
                    .removeClass('bg-success bg-warning')
                    .addClass('bg-danger')
                    .text('❌ System Issues');
            }
        })
        .catch(() => {
            $('#systemHealth')
                .removeClass('bg-success bg-warning')
                .addClass('bg-danger')
                .text('❌ Connection Failed');
        });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${icons[type] || 'info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

/**
 * Create toast container if it doesn't exist
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

/**
 * Export functions for use in other scripts
 */
window.AdminPanel = {
    initUserGrowthChart,
    initSystemUsageChart,
    initDiseaseTrendChart,
    setupUserManagement,
    setupReportGeneration,
    setupSystemMonitoring,
    loadSystemStats,
    showToast
};

console.log('🛠️ Admin Panel scripts loaded successfully!');