const API_BASE_URL = 'http://127.0.0.1:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    const ticketForm = document.getElementById('ticketForm');
    const refreshBtn = document.getElementById('refreshHistory');

    ticketForm.addEventListener('submit', handleTicketSubmit);
    refreshBtn.addEventListener('click', loadHistory);

    // Initial load
    loadHistory();
});

async function handleTicketSubmit(e) {
    e.preventDefault();

    const subject = document.getElementById('subject').value;
    const description = document.getElementById('description').value;
    const submitBtn = e.target.querySelector('button');
    const loader = document.getElementById('submitLoader');

    // UI Loading State
    submitBtn.disabled = true;
    loader.style.display = 'inline-block';

    try {
        const response = await fetch(`${API_BASE_URL}/tickets/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                subject,
                description,
                status: 'open'
            })
        });

        if (!response.ok) throw new Error('Failed to submit ticket');

        const data = await response.json();
        displaySuggestions(data.suggestions);
        loadHistory(); // Refresh history

        // Clear form
        document.getElementById('subject').value = '';
        document.getElementById('description').value = '';

    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting ticket. Please try again.');
    } finally {
        submitBtn.disabled = false;
        loader.style.display = 'none';
    }
}

function displaySuggestions(suggestions) {
    const container = document.getElementById('suggestionsContainer');

    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No high-confidence suggestions found for this query.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = suggestions.map(suggestion => `
        <div class="suggestion-card">
            <div class="suggestion-header">
                <span>AI Confidence</span>
                <span class="confidence-score">${(suggestion.confidence_score * 100).toFixed(1)}%</span>
            </div>
            <div class="suggestion-text">${suggestion.reply_text}</div>
            <div class="suggestion-actions">
                <button class="btn-sm" onclick="copyToClipboard('${suggestion.reply_text.replace(/'/g, "\\'")}')">
                    📋 Copy
                </button>
                <button class="btn-sm" onclick="submitFeedback(${suggestion.id}, true)">
                    👍 Helpful
                </button>
                <button class="btn-sm" onclick="submitFeedback(${suggestion.id}, false)">
                    👎 Not Helpful
                </button>
            </div>
        </div>
    `).join('');
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/tickets/`);
        const tickets = await response.json();

        const tbody = document.getElementById('historyBody');
        tbody.innerHTML = tickets.map(ticket => `
            <tr>
                <td>#${ticket.id}</td>
                <td>${ticket.subject}</td>
                <td><span class="status-pill">${ticket.status}</span></td>
                <td>${new Date(ticket.created_at).toLocaleDateString()}</td>
                <td>
                    <button class="btn-sm" onclick="viewTicket(${ticket.id})">View</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function submitFeedback(suggestionId, isHelpful) {
    try {
        await fetch(`${API_BASE_URL}/feedback/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                suggestion: suggestionId,
                is_helpful: isHelpful
            })
        });
        alert('Thanks for your feedback!');
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        alert('Copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy:', err);
    }
}

function viewTicket(id) {
    // In a real app, this would open a modal or navigate to detail view
    alert(`Viewing details for Ticket #${id}`);
}
