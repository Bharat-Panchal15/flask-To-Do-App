const registerForm = document.getElementById('register-form');
const para = document.getElementById('message');

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault() // prevent default page reload

    const data = new FormData(registerForm);
    const username = data.get('username');
    const password = data.get('password');
    const confirmPassword = data.get('confirm-password');

    if (password !== confirmPassword) {
        para.textContent = 'Passwords do not match!';
        para.style.color = 'red';
        return;
    }

    try {
        const response = await fetch('/api/register',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.status === 'success') {
            para.textContent = 'Registration Successful!';
            para.style.color = 'green';
            registerForm.reset();
        } else {
            para.textContent = 'Registration Failed!';
            para.style.color = 'red';
        }

    } catch (error) {
        console.error(error);
        para.textContent = 'Something Went Wrong';
        para.style.color = 'red';
    }
});