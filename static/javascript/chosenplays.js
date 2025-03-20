const ratings = { soundtrack: null, set: null, cast: null };
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const submitBtn = document.getElementById('submit-rating-btn');

const handleStarSelect = (stars, size) => {
    stars.forEach((star, index) => {
        if (index < size) {
            star.classList.add('checked'); 
            star.classList.remove('hovered'); 
        } else {
            star.classList.remove('checked');
        }
    });
};


const handleRating = (category) => {
    const stars = document.querySelectorAll(`.${category}`);
    const form = document.getElementById(`${category}-form`);
    const playID = form.getAttribute('data-playid');

    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            handleStarHover(stars, star.dataset.value);
        });

        star.addEventListener('mouseleave', () => {
            stars.forEach(star => star.classList.remove('hovered')); 
        });

        star.addEventListener('click', () => {
            const rating = star.dataset.value;
            ratings[category] = rating;
            handleStarSelect(stars, rating);
            checkRatingsCompletion(); 
        });
    });
};

const checkRatingsCompletion = () => {
    submitBtn.disabled = !(ratings.soundtrack && ratings.set && ratings.cast);
};

submitBtn.addEventListener('click', () => {
    const playID = document.getElementById('soundtrack-form').getAttribute('data-playid');

    Object.keys(ratings).forEach(category => {
        $.ajax({
            type: 'POST',
            url: '/submit-rating/',
            data: {
                'csrfmiddlewaretoken': csrf,
                'el_id': playID,
                'val': ratings[category],
                'category': category
            },
            success: function(response) {
                console.log(`${category} rating submitted successfully: ${response.score}`);
            },
            error: function(error) {
                console.error(`Error submitting ${category} rating`, error);
            }
        });
    });

    alert('Ratings submitted successfully!');
});

handleRating('soundtrack');
handleRating('set');
handleRating('cast');
checkRatingsCompletion(); 