// Capstone - client-side helpers

// Get CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

// Wire up the post-review form (only present on dealer detail page)
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const dealerId = reviewForm.dataset.dealerId;
        const review = reviewForm.querySelector('[name="review"]').value;
        const carYear = reviewForm.querySelector('[name="car_year"]').value;
        const purchase = reviewForm.querySelector('[name="purchase"]').checked;
        const carMakeSelect = reviewForm.querySelector('[name="car_make"]');
        const carMake = carMakeSelect.value || null;
        const payload = { dealer_id: parseInt(dealerId, 10), review, purchase, car_year: parseInt(carYear, 10) };
        if (carMake) payload.car_make = carMake;
        try {
            const resp = await fetch('/djangoapp/reviews/add', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(payload),
            });
            const data = await resp.json();
            if (data.status) {
                alert(`Review posted! Sentiment: ${data.sentiment}`);
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'unknown'));
            }
        } catch (err) {
            alert('Network error: ' + err.message);
        }
    });
}
