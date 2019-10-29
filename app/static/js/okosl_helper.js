function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function flash_message(msg) {
  var flash_well = document.getElementById('ajax-message-well');
  flash_well.innerHTML = msg;
  flash_well.style.display = 'inline'
}

var csrftoken = getCookie('csrftoken');

function pull_solutions(button) {
  var xhr = new XMLHttpRequest();
  var homework_id = button.id;
  xhr.open('GET', '/homeworks/' + homework_id + '/pull_solutions');

  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      if (data['success'] == true) {
        flash_message("Homework solutions pulled from Gitea")
      }
    }
  }
  xhr.send()
}


function push_remarks(button) {
  var xhr = new XMLHttpRequest();
  var homework_id = button.id;
  xhr.open('GET', '/homeworks/' + homework_id + '/push_remarks');

  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      if (data['success'] == true) {
        flash_message("Homework solution remarks pushed to Gitea")
      }
    }
  }
  xhr.send()
}