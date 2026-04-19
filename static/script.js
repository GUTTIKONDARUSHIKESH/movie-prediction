document.addEventListener('DOMContentLoaded', () => {
    
    // Fetch genres and stars on load
    fetch('/api/options')
        .then(response => response.json())
        .then(data => {
            const genreSelect = document.getElementById('genre');
            const starSelect = document.getElementById('star');

            data.genres.sort().forEach(genre => {
                let opt = document.createElement('option');
                opt.value = genre;
                opt.textContent = genre;
                genreSelect.appendChild(opt);
            });

            data.stars.sort().forEach(star => {
                let opt = document.createElement('option');
                opt.value = star;
                opt.textContent = star;
                starSelect.appendChild(opt);
            });
        })
        .catch(err => console.error("Error loading options:", err));

    // Handle form submission
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btnText = document.querySelector('.btn-text');
        const spinner = document.querySelector('.spinner');
        const resultBox = document.getElementById('result-box');
        const resultVal = document.getElementById('result-val');
        const resultBadge = document.getElementById('result-badge');

        // Loading state
        btnText.classList.add('hide');
        spinner.classList.remove('hide');
        resultBox.classList.add('hide');

        const payload = {
            budget: document.getElementById('budget').value,
            runtime: document.getElementById('runtime').value,
            votes: document.getElementById('votes').value,
            score: document.getElementById('score').value,
            genre: document.getElementById('genre').value,
            star: document.getElementById('star').value,
        };

        try {
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            // Format number as currency
            const formatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                maximumFractionDigits: 0
            });

            // Update UI
            resultVal.textContent = formatter.format(data.predicted_earnings);

            if (data.is_hit) {
                resultBadge.textContent = "🔥 BLAZING HIT";
                resultBadge.style.color = "var(--text-main)";
                resultBadge.style.background = "linear-gradient(135deg, #f59e0b, #ef4444)";
                resultBadge.style.borderColor = "transparent";
                resultVal.style.background = "linear-gradient(to right, #f59e0b, #ef4444)";
            } else if (data.is_profitable) {
                resultBadge.textContent = "✅ PROFITABLE";
                resultBadge.style.color = "var(--success)";
                resultBadge.style.background = "rgba(16, 185, 129, 0.1)";
                resultBadge.style.borderColor = "rgba(16, 185, 129, 0.2)";
                resultVal.style.background = "linear-gradient(to right, #4ade80, #3b82f6)";
            } else {
                resultBadge.textContent = "📉 FLOP RISK";
                resultBadge.style.color = "var(--danger)";
                resultBadge.style.background = "rgba(239, 68, 68, 0.1)";
                resultBadge.style.borderColor = "rgba(239, 68, 68, 0.2)";
                resultVal.style.background = "linear-gradient(to right, #ef4444, #f43f5e)";
            }
            
            // Text fill for webkit gradient
            resultVal.style.webkitBackgroundClip = "text";
            resultVal.style.webkitTextFillColor = "transparent";

            // Show result
            // Add slight delay for premium feel
            setTimeout(() => {
                spinner.classList.add('hide');
                btnText.classList.remove('hide');
                resultBox.classList.remove('hide');
            }, 600);

        } catch (error) {
            console.error(error);
            spinner.classList.add('hide');
            btnText.classList.remove('hide');
            alert("An error occurred during prediction.");
        }
    });
});
