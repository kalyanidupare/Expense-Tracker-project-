// Show notifications to users
function showNotification(message, isError = false) {
    const notification = document.createElement('div');
    notification.className = `alert ${isError ? 'alert-danger' : 'alert-success'} notification`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

// Initialize Bootstrap modal
let editModal;

document.addEventListener('DOMContentLoaded', function() {
    editModal = new bootstrap.Modal(document.getElementById('editModal'));
    
    // Add search input event listener
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchExpenses(this.value);
        }, 300);
    });
    
    fetchExpenses();
});

async function fetchExpenses() {
    try {
        const response = await fetch('/get_expenses');
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to fetch expenses');
        }
        const expenses = await response.json();
        displayExpenses(expenses);
    } catch (error) {
        showNotification(error.message, true);
    }
}

function displayExpenses(expenses) {
    const expenseList = document.getElementById('expense-list');
    expenseList.innerHTML = '';

    expenses.forEach(exp => {
        const date = new Date(exp.date).toLocaleDateString();
        const row = `<tr>
            <td>${exp.description}</td>
            <td>$${parseFloat(exp.amount).toFixed(2)}</td>
            <td>${exp.category}</td>
            <td>${date}</td>
            <td>
                <button class="btn btn-primary btn-sm btn-edit" onclick="editExpense('${exp._id}', '${exp.description}', ${exp.amount}, '${exp.category}')">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteExpense('${exp._id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        </tr>`;
        expenseList.innerHTML += row;
    });
}

async function searchExpenses(query) {
    if (!query.trim()) {
        await fetchExpenses();
        return;
    }

    try {
        const response = await fetch(`/search_expenses?query=${encodeURIComponent(query)}`);
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to search expenses');
        }
        const expenses = await response.json();
        displayExpenses(expenses);
    } catch (error) {
        showNotification(error.message, true);
    }
}

async function addExpense() {
    const description = document.getElementById('description').value.trim();
    const amount = document.getElementById('amount').value.trim();
    const category = document.getElementById('category').value.trim();

    // Validate inputs
    if (!description || !amount || !category) {
        showNotification('Please fill in all fields', true);
        return;
    }

    if (isNaN(amount) || parseFloat(amount) <= 0) {
        showNotification('Please enter a valid amount', true);
        return;
    }

    try {
        const response = await fetch('/add_expense', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description, amount, category })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to add expense');
        }

        const result = await response.json();
        showNotification(result.message);
        
        // Clear form
        document.getElementById('description').value = '';
        document.getElementById('amount').value = '';
        document.getElementById('category').value = '';
        
        await fetchExpenses();
    } catch (error) {
        showNotification(error.message, true);
    }
}

function editExpense(id, description, amount, category) {
    document.getElementById('editId').value = id;
    document.getElementById('editDescription').value = description;
    document.getElementById('editAmount').value = amount;
    document.getElementById('editCategory').value = category;
    editModal.show();
}

async function saveEdit() {
    const id = document.getElementById('editId').value;
    const description = document.getElementById('editDescription').value.trim();
    const amount = document.getElementById('editAmount').value.trim();
    const category = document.getElementById('editCategory').value.trim();

    // Validate inputs
    if (!description || !amount || !category) {
        showNotification('Please fill in all fields', true);
        return;
    }

    if (isNaN(amount) || parseFloat(amount) <= 0) {
        showNotification('Please enter a valid amount', true);
        return;
    }

    try {
        const response = await fetch(`/update_expense/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description, amount, category })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to update expense');
        }

        const result = await response.json();
        showNotification(result.message);
        editModal.hide();
        await fetchExpenses();
    } catch (error) {
        showNotification(error.message, true);
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }

    try {
        const response = await fetch(`/delete_expense/${id}`, { method: 'DELETE' });
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to delete expense');
        }
        const result = await response.json();
        showNotification(result.message);
        await fetchExpenses();
    } catch (error) {
        showNotification(error.message, true);
    }
}

async function exportMonthlyStatement() {
    try {
        const response = await fetch('/export_monthly_statement');
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to export statement');
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'monthly_statement.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        showNotification('Statement exported successfully');
    } catch (error) {
        showNotification(error.message, true);
    }
}

// Add some CSS for notifications
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
`;
document.head.appendChild(style);