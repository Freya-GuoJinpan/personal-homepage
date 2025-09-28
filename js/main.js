const darkModeButton = document.getElementById('toggle-dark-mode');
const bodyElement = document.body;
darkModeButton.addEventListener('click', function() {
    bodyElement.classList.toggle('dark-mode');
});
const addProjectBtn = document.getElementById('add-project-btn');
const newProjectInput = document.getElementById('new-project-input');
const projectList = document.querySelector('.section-title + .list-group'); 
addProjectBtn.addEventListener('click', function() {
    const newProjectText = newProjectInput.value;
    if (newProjectText.trim() !== '') {
        alert('请输入项目名称');
        return;
     }
    const newListItem = document.createElement('li');
    newListItem.className = 'list-group-item'; 
    newListItem.textContent = newProjectText;
    projectList.appendChild(newListItem);
    newProjectInput.value = '';
});
$(document).ready(function() {
     $('#skills-list li').on('click', function() {
     $(this).fadeOut();
    });
    const bioTitle = $('#bio-content').prev('.section-title');
    bioTitle.css('cursor', 'pointer');
    bioTitle.on('click', function() {
        $('#bio-content').toggle();
    });
});

