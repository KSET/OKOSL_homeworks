function drag_solution(ev) {
	ev.dataTransfer.setData('text', ev.target.id);
}

function allow_drop(ev) {
	ev.preventDefault();
}

function move_solution(source_sg_id, target_sg_id, solution_li) {
	var xhr = new XMLHttpRequest();
	var solution_id = solution_li.id.split('-')[1]
	//var params = "source_sg_id=" + source_sg_id + "&target_sg_id=" + target_sg_id + "&solution_id=" + solution_id;
	var params = {
		"source_sg_id" : source_sg_id,
		"target_sg_id" : target_sg_id,
		"solution_id" : solution_id
	};
	xhr.open('POST', '/ajax/move_solution');
	xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
	xhr.onload = function() {
		if (xhr.status === 200) {
			var data = JSON.parse(xhr.responseText);
			if (data['success'] == true) {
				flash_message("Solution moved");
			}
			else {
				flash_message("Error while pulling solutions: " + data['error'])
			}
		}
	}
	xhr.send(JSON.stringify(params))
}

function drop_solution(ev) {
	ev.preventDefault();
	var solution_li_id = ev.dataTransfer.getData('text');
	var solution_li = document.getElementById(solution_li_id);

	// fetch the <ul> to extract the SGID from its ID
	var source_sg_ul = solution_li.parentNode;
	var source_sg_id = source_sg_ul.id.split('-')[1];

	// iterate through DOM target parents to reach the <ul> node
	var target_sg_ul = ev.target;
	while (target_sg_ul.tagName != 'UL'){
		target_sg_ul = target_sg_ul.parentNode;
	}
	var target_sg_id = target_sg_ul.id.split('-')[1];

	move_solution(source_sg_id, target_sg_id, solution_li)
	target_sg_ul.appendChild(solution_li);
}

