const task_list = document.getElementById('task-list');
const add_task_btn = document.querySelector('#add-task-btn');
const task_input = document.querySelector('#new-task-input');

add_task_btn.addEventListener('click', async () => {
    const title = task_input.value.trim();
    if (!title) {
        alert("Task title cannot be empty.");
        return;
    }

    let token = localStorage.getItem('access_token');

    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        let response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, done: false })
        });

        if (response.status === 401) {
            let newtoken = await refreshToken();

            if (!newtoken) {
                window.location.href = '/login';
                return;
            }

            localStorage.setItem('access_token', newtoken);
            token = newtoken;

            response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title, done: false })
            });
        }

        const data = await response.json();

        if (data.status === 'success') {
            renderTask(data.data);
            task_input.value = '';

        } else {
            alert(data.message || 'Failed to add task.');
        }

    } catch (error) {
        console.error(`Error while adding task: ${error}`);
    }
});

function renderTask(task) {
    const li = document.createElement('li');
    li.textContent = task.title;

    if (task.done) {
        li.style.textDecoration = 'line-through';
    }

    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = task.done ? 'Mark Pending' : 'Mark Done';
    toggleBtn.dataset.id = task.id;
    toggleBtn.classList.add('task-btn', task.done ? 'pending' : 'done');

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.dataset.id = task.id;
    deleteBtn.classList.add('delete-btn');

    li.appendChild(toggleBtn);
    li.appendChild(deleteBtn);
    task_list.appendChild(li);

    toggleBtn.addEventListener('click', async () => {
        const toggleId = toggleBtn.dataset.id;
        let token = localStorage.getItem('access_token');

        if (!token) {
            window.location.href = '/login';
            return;
        }

        try {
            let response = await fetch(`/api/tasks/${toggleId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ title: task.title, done: !task.done })
            });

            if (response.status === 401) {
                let newtoken = await refreshToken();

                if (!newtoken) {
                    window.location.href = '/login';
                    return;
                }

                localStorage.setItem('access_token', newtoken);
                token = newtoken;

                response = await fetch(`/api/tasks/${toggleId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ title: task.title, done: !task.done })
                });
            }

            const data = await response.json();

            if (data.status === 'success') {
                task.done = !task.done;
                toggleBtn.textContent = task.done ? 'Mark Pending' : 'Mark Done';
                toggleBtn.classList.toggle('done', !task.done);
                toggleBtn.classList.toggle('pending', task.done);

                li.style.textDecoration = task.done ? 'line-through' : 'none';

            } else {
                console.error(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error(`Failed to toggle task: ${error}`);
        }
    });

    deleteBtn.addEventListener('click', async () => {
        const deleteId = deleteBtn.dataset.id;
        let token = localStorage.getItem('access_token');

        try {
            let response = await fetch(`/api/tasks/${deleteId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status === 401) {
                let newtoken = await refreshToken();

                if (!newtoken) {
                    window.location.href = '/login';
                    return;
                }

                localStorage.setItem('access_token', newtoken);
                token = newtoken;

                response = await fetch(`/api/tasks/${deleteId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                }); // DELETE now has no body
            }

            const data = await response.json();

            if (data.status === 'success') {
                li.remove();
            } else {
                console.error(data.message);
            }

        } catch (error) {
            console.error(`Failed to delete task: ${error}`);
        }
    });
}

async function fetchTasks() {
    let token = localStorage.getItem('access_token');

    let response = await fetch('/api/tasks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        console.log("Access token expired, trying to refresh...");
        let newtoken = await refreshToken();

        if (!newtoken) {
            window.location.href = '/login';
            return;
        }

        localStorage.setItem('access_token', newtoken);
        token = newtoken;

        response = await fetch('/api/tasks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
    }

    return response.json();
}

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        window.location.href = '/login';
        return;
    }

    const data = await fetchTasks();

    for (const task of data.data.tasks) {
        renderTask(task);
    }
});

const logoutBtn = document.getElementById('logout-btn');

logoutBtn.addEventListener('click', async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
        const response = await fetch('/api/logout',{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refreshToken}`
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });

        const data = await response.json();

        if (data.status === 'success') {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            window.location.href = '/auth/login';
        } else {
            console.error(data.message || "Failed to log out.");
        }
    } catch (error) {
        console.log(error);
    }
})