console.log('AJAX - КОНТРАКТ - РАБОТАЕТ')
var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
$(document).ready(function () {
    // обработчик отправки формы
    $('#addReviewForm').on('submit', function (event) {
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var method = form.attr('method');
        var data = form.serialize();

        // отправляем AJAX запрос на сервер
        $.ajax({
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: url,
            method: method,
            data: data,
            success: function (response) {
                // добавляем новую запись в таблицу
                var newRow = '<tr><td>' + response.id + '</td><td>' + response.date + '</td><td>' + response.type_stuff + '</td><td>' + response.re_login + '</td><td>' + response.re_password + '</td><td>' + response.re_firstname + '</td><td>' + response.re_lastname + '</td><td>' + response.space + '</td><td>' + response.office + '</td><td>' + response.status + '</td><td>' + response.type_review + '</td></tr>';
                $('#reviewBody tbody').append(newRow);

                // очищаем поля формы
                $('#addReviewForm input').val('');
                $('#addReviewForm select').val('');
                $('#selected_positions').find('span').empty();
                $('input[name="contract-students"]').prop('checked', false);

                // скрываем модальное окно
                $('.modal').modal('hide');
            },
            error: function (xhr, status, error) {
                console.log('Ошибка:', error);
            }
        });
    });
});