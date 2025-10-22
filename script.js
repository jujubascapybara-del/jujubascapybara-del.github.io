// Array of daily wishes
const dailyWishes = [
    "Пусть сегодняшний день принесет вам радость, гармонию и внутреннюю силу!",
    "Желаю вам сегодня почувствовать свою женскую энергию и позволить ей сиять!",
    "Пусть ваша интуиция будет вашим лучшим проводником в этот день!",
    "Желаю вам сегодня найти время для себя и своих мечтаний!",
    "Пусть красота окружающего мира наполнит ваше сердце вдохновением!",
    "Желаю вам сегодня быть нежной с собой и принимать себя такой, какая вы есть!",
    "Пусть ваша творческая энергия расцветет и принесет радость!",
    "Желаю вам сегодня почувствовать связь с природой и своей внутренней мудростью!",
    "Пусть этот день принесет вам моменты тишины и покоя!",
    "Желаю вам сегодня доверять своему сердцу и следовать за мечтами!",
    "Пусть ваша женская энергия привлечет в вашу жизнь только хорошее!",
    "Желаю вам сегодня быть благодарной за все прекрасное в вашей жизни!",
    "Пусть этот день станет началом чего-то удивительного!",
    "Желаю вам сегодня почувствовать себя королевой своего мира!",
    "Пусть ваша внутренняя красота сияет ярче любого солнца!",
    "Желаю вам сегодня найти баланс между заботой о других и заботой о себе!",
    "Пусть ваши мечты сегодня станут на шаг ближе к реальности!",
    "Желаю вам сегодня быть смелой в выражении своих чувств!",
    "Пусть этот день принесет вам новые возможности для роста!",
    "Желаю вам сегодня почувствовать себя любимой и ценной!"
];

// Array of daily affirmations
const dailyAffirmations = [
    "Я достойна любви и счастья",
    "Моя женская энергия - это моя сила",
    "Я доверяю своей интуиции",
    "Я красива внутри и снаружи",
    "Я принимаю себя такой, какая я есть",
    "Моя внутренняя мудрость ведет меня",
    "Я заслуживаю всего самого лучшего",
    "Моя женственность - это мой дар",
    "Я создаю свою реальность с любовью",
    "Я излучаю красоту и гармонию",
    "Моя душа сияет ярким светом",
    "Я привлекаю в свою жизнь только хорошее",
    "Я доверяю процессу жизни",
    "Моя сила в моей мягкости",
    "Я достойна всех своих мечтаний"
];

// DOM elements
const wishText = document.getElementById('wishText');
const newWishBtn = document.getElementById('newWishBtn');
const affirmationItems = document.querySelectorAll('.affirmation-item p');

// Function to get random wish
function getRandomWish() {
    const randomIndex = Math.floor(Math.random() * dailyWishes.length);
    return dailyWishes[randomIndex];
}

// Function to get random affirmations
function getRandomAffirmations() {
    const shuffled = [...dailyAffirmations].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, 4);
}

// Function to update wish with animation
function updateWish() {
    const wishCard = document.querySelector('.wish-card');
    const newWish = getRandomWish();
    
    // Add fade out animation
    wishCard.style.opacity = '0.5';
    wishCard.style.transform = 'scale(0.95)';
    
    setTimeout(() => {
        wishText.textContent = newWish;
        // Add fade in animation
        wishCard.style.opacity = '1';
        wishCard.style.transform = 'scale(1)';
    }, 300);
}

// Function to update affirmations
function updateAffirmations() {
    const randomAffirmations = getRandomAffirmations();
    
    affirmationItems.forEach((item, index) => {
        if (randomAffirmations[index]) {
            // Add animation
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                item.textContent = `"${randomAffirmations[index]}"`;
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 100);
        }
    });
}

// Function to add floating particles animation
function createFloatingParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    `;
    document.body.appendChild(particlesContainer);
    
    function createParticle() {
        const particle = document.createElement('div');
        particle.innerHTML = ['✨', '🌸', '💕', '🦋', '🌙', '💎'][Math.floor(Math.random() * 6)];
        particle.style.cssText = `
            position: absolute;
            font-size: ${Math.random() * 20 + 10}px;
            color: rgba(214, 51, 132, ${Math.random() * 0.5 + 0.3});
            left: ${Math.random() * 100}%;
            top: 100%;
            animation: floatUp ${Math.random() * 3 + 4}s linear forwards;
            pointer-events: none;
        `;
        
        particlesContainer.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 7000);
    }
    
    // Create particles periodically
    setInterval(createParticle, 2000);
}

// Add CSS for particle animation
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .particles-container {
        overflow: hidden;
    }
`;
document.head.appendChild(style);

// Function to add smooth scroll effect
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Function to add intersection observer for animations
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }
        });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.energy-card, .affirmation-item').forEach(card => {
        observer.observe(card);
    });
}

// Function to add time-based greeting
function addTimeBasedGreeting() {
    const hour = new Date().getHours();
    let greeting = '';
    
    if (hour < 6) {
        greeting = 'Доброй ночи';
    } else if (hour < 12) {
        greeting = 'Доброе утро';
    } else if (hour < 18) {
        greeting = 'Добрый день';
    } else {
        greeting = 'Добрый вечер';
    }
    
    const subtitle = document.querySelector('.subtitle');
    subtitle.textContent = `${greeting}! Пожелания хорошего дня и вдохновение`;
}

// Function to add click effects
function addClickEffects() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('new-wish-btn') || 
            e.target.classList.contains('energy-card') || 
            e.target.classList.contains('affirmation-item')) {
            
            // Create ripple effect
            const ripple = document.createElement('div');
            const rect = e.target.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 105, 180, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            e.target.style.position = 'relative';
            e.target.style.overflow = 'hidden';
            e.target.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
    });
}

// Add ripple animation CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Initialize all functions when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set initial wish
    wishText.textContent = getRandomWish();
    
    // Set initial affirmations
    updateAffirmations();
    
    // Add time-based greeting
    addTimeBasedGreeting();
    
    // Add event listeners
    newWishBtn.addEventListener('click', updateWish);
    
    // Add floating particles
    createFloatingParticles();
    
    // Add smooth scroll
    addSmoothScroll();
    
    // Add scroll animations
    addScrollAnimations();
    
    // Add click effects
    addClickEffects();
    
    // Update affirmations every 30 seconds
    setInterval(updateAffirmations, 30000);
    
    // Add some initial animations
    setTimeout(() => {
        document.querySelectorAll('.energy-card').forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }, 100);
});

// Add keyboard support
document.addEventListener('keydown', function(e) {
    if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        updateWish();
    }
});

// Add touch support for mobile
let touchStartY = 0;
let touchEndY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartY = e.changedTouches[0].screenY;
});

document.addEventListener('touchend', function(e) {
    touchEndY = e.changedTouches[0].screenY;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartY - touchEndY;
    
    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            // Swipe up - new wish
            updateWish();
        }
    }
}
