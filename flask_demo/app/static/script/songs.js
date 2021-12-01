$(document).ready(function() {
  $("#searchbox").on("input", function(e) {
    if ($("#searchbox").val() !== "") {
      $.ajax({
        type: "POST",
        url: "/search",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify({
          "text": $("#searchbox").val()
        }),
        success: function(res) {
          $("#songlist").empty();
          var data = "<ul>";
          $.each(res.song_list, function(i, value) {
            data += "<li>" + value.name + " - " + value.artist + " - (" + value.songId + ") - <a target='_blank' href=https://" + value.url + ">" + value.url + "</a></li>";
          });
          data += "</ul>";
          $("#songlist").html(data);
        },
        error: function() {
          console.log("Error");
        }
      });
    }
  });

  $("#submit-song-rec").click(function() {
    if ($("#rec_searchbox").val() !== "") {
      $.ajax({
        type: "POST",
        url: "/get_song_recs",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify({
          "songId": $("#rec_searchbox").val()
        }),
        success: function(res) {
          $("#song_rec_list").empty();
          var data = "<ul>";
          $.each(res.song_list, function(i, value) {
            data += "<li>" + value.name + " - " + value.artist + " - (" + value.songId + ")</li>";
          });
          data += "</ul>";
          $("#song_rec_list").html(data);
        },
        error: function() {
          console.log("Error");
        }
      });
    }
  });
});
