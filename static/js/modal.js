// при клике на кнопку "Добавить"
$('#addReview').on('click', function () {
    $('.modal').fadeIn(300, function () {
      // после того, как модальное окно станет видимым, изменяем свойство CSS элемента .modal-right-side
      $('.modal-right-side').css('right', 0);
    });
  });
  
  // при клике на кнопку закрытия или на фон
  $('.close, .modal').on('click', function () {
    $('.modal').fadeOut(300)
    $('.modal-right-side').css('right', '-700px');
  });
  
  // при клике на содержимое модального окна
  $('.modal-content').on('click', function (event) {
    // останавливаем событие, чтобы не скрывать окно при клике внутри него
    event.stopPropagation();
  });
  
  
  
  function updatePositions() {
    const checkboxes = document.getElementsByName('contract-students');
    const selectedPositions = [];
    for (let i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) {
        selectedPositions.push(checkboxes[i].getAttribute('data-id'));
      }
    }
    document.getElementById('selected_positions').value = selectedPositions.join(',');
  }
  
  function updateSelectedStudents() {
    const selectedPositions = document.getElementById('selected_positions').value.split(',');
    const selectedStudents = selectedPositions.map(id => {
      const checkbox = document.querySelector(`input[data-id='${id}']`);
      return checkbox ? `<span>${checkbox.getAttribute('data-id')}</span>` : '';
    });
    document.getElementById('selected_students').innerHTML = selectedStudents.join(' ');
  }
  document.addEventListener('DOMContentLoaded', updateSelectedStudents);
  document.addEventListener('change', updateSelectedStudents);