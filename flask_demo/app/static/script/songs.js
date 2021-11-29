$(document).ready(function () {
  $("#searchbox").on("input", function(e) {
    if ($("#searchbox").val() !== "") {
      $("#songlist").empty();
      $.ajax({
        type: 'POST',
        url: '/search',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
          'text': $("#searchbox").val()
        }),
        success: function (res) {
          var data = "<ul>";
          $.each(res.song_list, function(i, value) {
            data += "<li>" + value.name + " - " + value.artist + "</li>";
          });
          data += "</ul>";
          $("#songlist").html(data);
        },
        error: function () {
          console.log('Error');
        }
      });
    }
  });
});
