// Insurance Policy Dashboard - JavaScript functionality
// Read-only version - no activation functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('TMHCC Insurance Dashboard initialized successfully!');
    setupEventListeners();
});

// Set up all event listeners
function setupEventListeners() {
    // Listen for HTMX events to handle loading states and errors
    document.body.addEventListener('htmx:beforeRequest', handleHtmxBeforeRequest);
    document.body.addEventListener('htmx:responseError', handleHtmxResponseError);
    document.body.addEventListener('htmx:afterRequest', handleHtmxAfterRequest);
    document.body.addEventListener('htmx:beforeOnLoad', handleHtmxBeforeOnLoad);
    
    // Close modal when clicking outside of it
    document.getElementById('policyModal').addEventListener('click', function(event) {
        if (event.target === this) {
            closeModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

// HTMX Event Handlers
function handleHtmxBeforeRequest(event) {
    console.log('Making API request to:', event.detail.pathInfo.requestPath);
    
    // Show loading state for the target element
    const target = event.detail.target;
    if (target && target.id === 'policiesTable') {
        target.innerHTML = '<tr><td colspan="6" class="loading">Loading policies...</td></tr>';
    } else if (target && target.id === 'singlePolicyResult') {
        target.innerHTML = '<div class="loading">Searching for policy...</div>';
    } else if (target && target.id === 'policyDetails') {
        target.innerHTML = '<div class="loading">Loading policy details...</div>';
    }
}

function handleHtmxResponseError(event) {
    console.error('API request failed:', event.detail);
    const target = event.detail.target;
    
    if (target && target.id === 'policiesTable') {
        target.innerHTML = '<tr><td colspan="6" class="error">Error loading policies. Please try again.</td></tr>';
    } else if (target && target.id === 'singlePolicyResult') {
        // Show friendly error message for search
        const policyNumber = extractPolicyNumberFromUrl(event.detail.pathInfo.requestPath);
        target.innerHTML = generatePolicyNotFoundMessage(policyNumber);
    } else if (target) {
        target.innerHTML = '<div class="error">Error loading data. Please try again.</div>';
    }
    
    showNotification('Error loading data from API', 'error');
}

function handleHtmxAfterRequest(event) {
    console.log('API request completed:', event.detail.pathInfo.requestPath);
}

function handleHtmxBeforeOnLoad(event) {
    const target = event.detail.target;
    const xhr = event.detail.xhr;
    
    // Handle policies table response
    if (target.id === 'policiesTable') {
        try {
            const response = JSON.parse(xhr.responseText);
            target.innerHTML = generatePoliciesTable(response);
            event.detail.shouldSwap = false;
        } catch (error) {
            console.error('Error processing policies response:', error);
        }
    }
    // Handle single policy search response
    else if (target.id === 'singlePolicyResult') {
        try {
            // Check if response is successful
            if (xhr.status === 200) {
                const policy = JSON.parse(xhr.responseText);
                target.innerHTML = generateSinglePolicyView(policy);
            } else if (xhr.status === 404) {
                // Policy not found - show friendly message
                const policyNumber = extractPolicyNumberFromUrl(event.detail.pathInfo.requestPath);
                target.innerHTML = generatePolicyNotFoundMessage(policyNumber);
            } else {
                // Other error
                target.innerHTML = '<div class="error">Error loading policy data. Please try again.</div>';
            }
            event.detail.shouldSwap = false;
        } catch (error) {
            console.error('Error processing single policy response:', error);
            const policyNumber = extractPolicyNumberFromUrl(event.detail.pathInfo.requestPath);
            target.innerHTML = generatePolicyNotFoundMessage(policyNumber);
        }
    }
    // Handle policy details modal response
    else if (target.id === 'policyDetails') {
        try {
            const policy = JSON.parse(xhr.responseText);
            target.innerHTML = generatePolicyDetailsModal(policy);
            event.detail.shouldSwap = false;
        } catch (error) {
            console.error('Error processing policy details response:', error);
        }
    }
}

// Extract policy number from URL for error messages
function extractPolicyNumberFromUrl(url) {
    const parts = url.split('/');
    return parts[parts.length - 1] || 'unknown';
}

// Generate policy not found message
function generatePolicyNotFoundMessage(policyNumber) {
    return `
        <div class="policy-not-found">
            <div class="not-found-header">
                <h3>Policy Not Found</h3>
                <button class="close-search-btn" onclick="closeSearchResults()" title="Close search results">
                    &times;
                </button>
            </div>
            <div class="not-found-content">
                <div class="not-found-icon">🔍</div>
                <div class="not-found-text">
                    <p><strong>Policy "${escapeHtml(policyNumber)}" was not found</strong></p>
                    <p>Please check the policy number and try again.</p>
                    <p>Make sure the policy number is correct and exists in the system.</p>
                </div>
            </div>
            <div class="not-found-actions">
                <button class="btn btn-secondary" onclick="closeSearchResults()">
                    Close Search
                </button>
                <button class="btn btn-primary" onclick="loadAllPolicies()">
                    View All Policies
                </button>
            </div>
        </div>
    `;
}

// Generate HTML table from policies data
function generatePoliciesTable(policies) {
    if (!policies || policies.length === 0) {
        return '<tr><td colspan="6" class="loading">No policies found</td></tr>';
    }

    return policies.map(policy => `
        <tr>
            <td><strong>${escapeHtml(policy.policy_number)}</strong></td>
            <td>${escapeHtml(policy.insured_name)}</td>
            <td>${escapeHtml(policy.policy_type)}</td>
            <td class="premium">${escapeHtml(policy.premium)}</td>
            <td>
                <span class="status-badge status-${getStatusClass(policy.status)}">
                    ${escapeHtml(policy.status)}
                </span>
            </td>
            <td>${escapeHtml(policy.start_date)} to ${escapeHtml(policy.end_date)}</td>
            <td>
                <button class="view-btn" onclick="viewPolicyDetails('${escapeHtml(policy.policy_number)}')">
                    View Details
                </button>
            </td>
        </tr>
    `).join('');
}

// Generate single policy view for search results
function generateSinglePolicyView(policy) {
    if (!policy) {
        return generatePolicyNotFoundMessage('unknown');
    }

    return `
        <div class="policy-search-result">
            <div class="search-header">
                <h3>Policy Found</h3>
                <button class="close-search-btn" onclick="closeSearchResults()" title="Close search results">
                    &times;
                </button>
            </div>
            <div class="policy-card">
                <div class="policy-header">
                    <h4>${escapeHtml(policy.policy_number)}</h4>
                    <span class="status-badge status-${getStatusClass(policy.status)}">
                        ${escapeHtml(policy.status)}
                    </span>
                </div>
                <div class="policy-info">
                    <div class="info-row">
                        <span class="label">Insured Name:</span>
                        <span class="value">${escapeHtml(policy.insured_name)}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Policy Type:</span>
                        <span class="value">${escapeHtml(policy.policy_type)}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Premium:</span>
                        <span class="value premium">${escapeHtml(policy.premium)}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Coverage Period:</span>
                        <span class="value">${escapeHtml(policy.start_date)} to ${escapeHtml(policy.end_date)}</span>
                    </div>
                </div>
                <div class="policy-actions">
                    <button class="view-btn" onclick="viewPolicyDetails('${escapeHtml(policy.policy_number)}')">
                        View Full Details
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Generate detailed policy view for modal
function generatePolicyDetailsModal(policy) {
    if (!policy) {
        return '<div class="error">Policy details not available</div>';
    }

    return `
        <div class="policy-details-modal">
            <div class="detail-section">
                <h3>Policy Information</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Policy Number</div>
                        <div class="detail-value">${escapeHtml(policy.policy_number)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Insured Name</div>
                        <div class="detail-value">${escapeHtml(policy.insured_name)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Policy Type</div>
                        <div class="detail-value">${escapeHtml(policy.policy_type)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Status</div>
                        <div class="detail-value">
                            <span class="status-badge status-${getStatusClass(policy.status)}">
                                ${escapeHtml(policy.status)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Financial Details</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Premium Amount</div>
                        <div class="detail-value premium">${escapeHtml(policy.premium)}</div>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h3>Coverage Period</h3>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Start Date</div>
                        <div class="detail-value">${escapeHtml(policy.start_date)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">End Date</div>
                        <div class="detail-value">${escapeHtml(policy.end_date)}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Policy ID</div>
                        <div class="detail-value">${escapeHtml(policy.id)}</div>
                    </div>
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal()">
                    Close
                </button>
            </div>
        </div>
    `;
}

// Policy Management Functions
function loadAllPolicies() {
    console.log('Refreshing all policies...');
    
    // Clear any search results first
    closeSearchResults();
    
    // Clear search input
    document.getElementById('searchInput').value = '';
    
    // Use HTMX to reload the policies table
    htmx.ajax('GET', '/policies/', {
        target: '#policiesTable',
        swap: 'none'
    }).then(() => {
        showNotification('Policies refreshed successfully', 'success');
    });
}

function searchPolicy() {
    const policyNumber = document.getElementById('searchInput').value.trim();
    
    if (!policyNumber) {
        showNotification('Please enter a policy number to search', 'error');
        return;
    }

    const resultsDiv = document.getElementById('searchResults');
    const singlePolicyResult = document.getElementById('singlePolicyResult');
    
    // Show loading state
    singlePolicyResult.innerHTML = '<div class="loading">Searching for policy...</div>';
    resultsDiv.classList.remove('hidden');

    // Use HTMX to fetch the single policy
    htmx.ajax('GET', `/policies/${encodeURIComponent(policyNumber)}`, {
        target: '#singlePolicyResult',
        swap: 'none'
    });
}

function closeSearchResults() {
    console.log('Closing search results...');
    
    const resultsDiv = document.getElementById('searchResults');
    const searchInput = document.getElementById('searchInput');
    
    // Hide search results
    resultsDiv.classList.add('hidden');
    
    // Clear search input
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Clear search results content
    document.getElementById('singlePolicyResult').innerHTML = '';
}

function handleSearchKeypress(event) {
    // If user presses Enter in search box, trigger search
    if (event.key === 'Enter') {
        searchPolicy();
    }
}

function viewPolicyDetails(policyNumber) {
    console.log('Viewing details for policy:', policyNumber);
    
    // Use HTMX to load policy details into modal
    htmx.ajax('GET', `/policies/${encodeURIComponent(policyNumber)}`, {
        target: '#policyDetails',
        swap: 'none'
    }).then(() => {
        // Show modal after content is loaded
        document.getElementById('policyModal').classList.remove('hidden');
    }).catch(error => {
        console.error('Error loading policy details:', error);
        showNotification('Error loading policy details', 'error');
    });
}

function closeModal() {
    document.getElementById('policyModal').classList.add('hidden');
}

// Utility Functions
function getStatusClass(status) {
    if (!status) return 'unknown';
    return status.toLowerCase();
}

function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return '';
    return unsafe.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 4000);
}

// Export functions to global scope so HTML can call them
window.loadAllPolicies = loadAllPolicies;
window.searchPolicy = searchPolicy;
window.viewPolicyDetails = viewPolicyDetails;
window.closeModal = closeModal;
window.closeSearchResults = closeSearchResults;
window.handleSearchKeypress = handleSearchKeypress;