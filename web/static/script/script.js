const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
const homeScreen = document.getElementById('homeScreen');
const menuLinks = document.querySelectorAll('.menu-item a');

// Toggle menu
menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    sidebar.classList.toggle('active');
});

// Navigate to sections
menuLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('data-section');
        
        // Hide all sections and home
        document.querySelectorAll('.content').forEach(content => {
            content.classList.remove('active');
        });
        homeScreen.style.display = 'none';
        
        // Show selected section
        document.getElementById(sectionId).classList.add('active');
        
        // Close menu
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
    });
});

// Go back to home
function goHome() {
    document.querySelectorAll('.content').forEach(content => {
        content.classList.remove('active');
    });
    homeScreen.style.display = 'flex';
}

document.getElementById('questionarioForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    
    try {
        // Send data to API as form-urlencoded
        const response = await fetch('/invitados', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Show success message
            alert('Grazas! A túa confirmación foi enviada correctamente.');
            e.target.reset();
            goHome();
        } else {
            // Show error message
            alert('Houbo un erro ao enviar a confirmación. Por favor, inténtao de novo.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Houbo un erro ao enviar a confirmación. Por favor, inténtao de novo.');
    }
});