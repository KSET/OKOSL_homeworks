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


function change_year(years) {
  console.log('test')
  var selected_year = document.getElementById("homeworks_by_year").value;
  years.forEach(function(year) {
    var year_div = document.getElementById("hw-" + year);
    console.log("Year: " + year + "  --  SelYear: " + selected_year)
    console.log(year == selected_year)
    if (selected_year == 'all') {
      year_div.style.display = "block";
    }
    else if (year == selected_year) {
      year_div.style.display = "block";
    }
    else {
      year_div.style.display = "none";
    }
  });
}


var csrftoken = getCookie('csrftoken');

function pull_solutions(button) {
  var xhr = new XMLHttpRequest();
  var homework_id = button.id;
  xhr.open('GET', '/ajax/' + homework_id + '/pull_solutions');

  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      if (data['success'] == true) {
        flash_message("Homework solutions pulled from Gitea")
      }
      else {
        flash_message("Error while pulling solutions: " + data['error'])
      }
    }
  }
  xhr.send()
}


function push_remarks(button) {
  var xhr = new XMLHttpRequest();
  var homework_id = button.id;
  xhr.open('GET', '/ajax/' + homework_id + '/push_remarks');

  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      if (data['success'] == true) {
        flash_message("Homework solution remarks pushed to Gitea")
      }
      else {
        flash_message("Error while pushing remarks: " + data['error'])
      }
    }
  }
  xhr.send()
}