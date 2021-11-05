function drag_solution(ev) {
	ev.dataTransfer.setData('text', ev.target.id);
}

function allow_drop(ev) {
	ev.preventDefault();
}

function add_solution_group(sg_id) {
	var xhr = new XMLHttpRequest();
	var params = {
		"sg_id" : sg_id,
	};
	xhr.open('POST', '/ajax/add_solution_group');
	xhr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
	xhr.onload = function() {
		if (xhr.status === 200) {
			var data = JSON.parse(xhr.responseText);
			var sg_list_ul = document.getElementById("solution-groups-list")
			sg_list_ul.insertAdjacentHTML("beforeend", data['sg_html']);
		}
	}
	xhr.send(JSON.stringify(params))
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
				if (data['target_added'] == true) {
					console.log("Target added!");
					flash_message("Target SG added!");
					target_sg_id = data['target_sg_id'];
					add_solution_group(target_sg_id);
					solution_li.style.display = 'none';
				}
				if (data['source_removed'] == true) {
					console.log("Source removed!")
					flash_message("Source SG removed");
					var sg_li = document.getElementById("solution-group-" + source_sg_id)
					// var source_remarks_div = document.getElementById("remarks-" + source_sg_id)
					var source_remarks_ul = document.getElementById("remark-list-" + source_sg_id)
					var target_remarks_ul = document.getElementById("remark-list-" + target_sg_id)

					var remarks = source_remarks_ul.getElementsByTagName("li");
					for (var i = 0; i < remarks.length; ++i) {
						target_remarks_ul.appendChild(remarks[i])
					}

					sg_li.style.display = 'none'
				}
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
	if (target_sg_ul.id.match("solution_list-[0-9]+")) {
		var target_sg_id = target_sg_ul.id.split('-')[1];
	}
	else {
		var target_sg_id = null
	}

	move_solution(source_sg_id, target_sg_id, solution_li)
	target_sg_ul.appendChild(solution_li);
}

$('body').on('click', '.list-group-item-fix-toggle', function() {
  $(this).closest('.list-group-item').toggleClass('list-item-fixed').siblings().removeClass('list-item-fixed');
});
