function addTodo() {
    const input = document.getElementById('todo-input');
    const todoText = input.value.trim();
    if (todoText === '') return;

    const ul = document.getElementById('todo-list');
    const li = document.createElement('li');
    li.textContent = todoText;

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.className = 'delete-btn';
    delBtn.onclick = function() {
        ul.removeChild(li);
    };

    li.appendChild(delBtn);
    ul.appendChild(li);
    input.value = '';
}

// Allow Enter key to add todo
document.getElementById('todo-input').addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});
