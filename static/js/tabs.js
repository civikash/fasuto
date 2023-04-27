const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
  button.addEventListener('click', () => {
    const tab = button.getAttribute('data-tab');
    setActiveTab(tab);
  });
});

function setActiveTab(tab) {
  tabButtons.forEach(button => {
    if (button.getAttribute('data-tab') === tab) {
      button.classList.add('active');
    } else {
      button.classList.remove('active');
    }
  });

  tabContents.forEach(content => {
    if (content.getAttribute('data-tab') === tab) {
      content.classList.add('active');
    } else {
      content.classList.remove('active');
    }
  });
}

// Устанавливаем первый таб активным
setActiveTab('tab1');