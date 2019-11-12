$(window).scroll(function() {
	sessionStorage.scrollTop = $(this).scrollTop();
});

$(document).ready(function() {
	if (sessionStorage.scrollTop != "undefined") {
		$(window).scrollTop(sessionStorage.scrollTop);
	}
});

// $("#FORM-ID").on("submit", function() {
// 	var form = $(this);
// 	console.log("this");
// 	$.ajax({
// 		url: "/news/",
// 		data: form.serialize(),
// 		type: form.attr("method"),
// 		dataType: "json",
// 		error: function() {
// 			console.log("error");
// 		},
// 		success: function(data) {
// 			console.log("woooo");
// 			var jData = JSON.parse(data["post"]);
// 			var content = jData[jData.length - 1].fields.content;
// 			var sans = "Fira Sans";
// 			var html =
// 				'<tr><td class="pc-fb-font" style="vertical-align: top; text-align: center; font-family: ' +
// 				sans +
// 				', Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 300; line-height: 1.56; letter-spacing: -0.2px; color: #9B9B9B;" valign="top" align="center" style="white-space: pre-line;">' +
// 				content +
// 				"</td></tr>";
// 			$(html).insertBefore(".ajax");
// 		}
// 	});
// 	return false;
// });
