document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('queryForm');
    const queryInput = document.getElementById('queryInput');
    const loading = document.getElementById('loading');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsList = document.getElementById('resultsList');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');

    queryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        
        if (!query) {
            showError('Please enter a legal question');
            return;
        }
        
        // Clear previous results and show loading
        resultsList.innerHTML = '';
        hideError();
        showLoading();
        hideResults();
        
        // Send the search request
        const formData = new FormData();
        formData.append('query', query);
        
        fetch('/search', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            
            if (data.error) {
                showError(data.error);
                return;
            }
            
            if (data.results && data.results.length > 0) {
                displayResults(data.results);
            } else {
                showError('No results found. Please try a different query.');
            }
        })
        .catch(error => {
            hideLoading();
            showError('Error: ' + error.message);
            console.error('Error:', error);
        });
    });

    function displayResults(results) {
        results.forEach(result => {
            const resultCard = document.createElement('div');
            resultCard.className = 'card result-card p-3 mb-3';
            
            // Format the content with proper paragraph breaks
            const formattedContent = result.snippet.replace(/\n\n/g, '<br><br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            resultCard.innerHTML = `
                <h3 class="result-title">${result.title}</h3>
                <div class="result-content mt-3">${formattedContent}</div>
                ${result.displayLink ? `<div class="source-reference mt-3"><small class="text-muted">Source: ${result.displayLink}</small></div>` : ''}
            `;
            
            resultsList.appendChild(resultCard);
        });
        
        showResults();
    }

    function showLoading() {
        loading.classList.remove('d-none');
    }

    function hideLoading() {
        loading.classList.add('d-none');
    }

    function showResults() {
        resultsContainer.classList.remove('d-none');
    }

    function hideResults() {
        resultsContainer.classList.add('d-none');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.classList.remove('d-none');
    }

    function hideError() {
        errorContainer.classList.add('d-none');
    }
});