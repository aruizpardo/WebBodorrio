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
    const submitButton = e.target.querySelector('.submit-button');
    const originalText = submitButton.textContent;
    
    // Deshabilitar botón mientras se envía
    submitButton.disabled = true;
    submitButton.textContent = 'Enviando...';
    
    try {
        // Send data to API as form-urlencoded
        const response = await fetch('/invitados', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Mostrar éxito (verde)
            submitButton.classList.add('success');
            submitButton.textContent = '✓ ¡Confirmación enviada!';
            
            // Resetear formulario después de 3 segundos
            setTimeout(() => {
                submitButton.classList.remove('success');
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                e.target.reset();
            }, 3000);
        } else {
            // Mostrar error (vermello)
            submitButton.classList.add('error');
            submitButton.textContent = '✗ Error al enviar';
            
            // Volver al estado original después de 3 segundos
            setTimeout(() => {
                submitButton.classList.remove('error');
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }, 3000);
        }
    } catch (error) {
        console.error('Error:', error);
        
        // Mostrar error (vermello)
        submitButton.classList.add('error');
        submitButton.textContent = '✗ Error de conexión';
        
        // Volver al estado original después de 3 segundos
        setTimeout(() => {
            submitButton.classList.remove('error');
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }, 3000);
    }
});