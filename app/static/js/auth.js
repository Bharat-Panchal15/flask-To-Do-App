const login_form = document.getElementById('login-form');
const message = document.getElementById('login-message');

if (login_form) {
    login_form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        const response = await fetch('/api/login',{method: 'POST',headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username,password}) });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            localStorage.setItem('access_token',data.data.access_token);
            localStorage.setItem('refresh_token',data.data.refresh_token);
            window.location.href = '/dashboard/tasks';
        } else {
            message.textContent = data.message || "Login failed, try again.";
            message.style.color = 'red';
        }

        setTimeout(() => {
            message.textContent = '';
        },3000);
    });
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
        window.location.href = '/login';
        return null;
    }

    const response = await fetch('/api/refresh',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${refreshToken}`
        }
    });

    const data = await response.json();

    if (data.status === 'success') {
        localStorage.setItem('access_token',data.data.access_token);
        return data.data.access_token;
    } else {
        window.location.href = '/login';
        return null;
    }
}