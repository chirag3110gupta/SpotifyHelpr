$(document).ready(function() {
  // example: https://getbootstrap.com/docs/4.2/components/modal/
  // show modal
  $("#task-modal").on("show.bs.modal", function(event) {
    const button = $(event.relatedTarget) // Button that triggered the modal
    const taskID = button.data("source") // Extract info from data-* attributes
    const content = button.data("content") // Extract info from data-* attributes
    const modal = $(this)

    if (taskID === "New Playlist") {
      modal.find(".modal-title").text(taskID)
      $("#task-form-display").removeAttr("taskID")

    } else {
      modal.find(".modal-title").text("Edit Playlist " + taskID)
      $("#task-form-display").attr("taskID", taskID)
    }

    if (content) {
      modal.find(".form-control").val(content);

    } else {
      modal.find(".form-control").val("");
    }
  })

  $("#submit-task").click(function() {
    const tID = $("#task-form-display").attr("taskID");
    if (tID) {
      $.ajax({
        type: "POST",
        url: "/edit",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify({
          "playlistId": tID,
          "playlistName": $("#task-modal").find(".form-control").val(),
        }),
        success: function(res) {
          console.log(res.response)
          location.reload();
        },
        error: function() {
          console.log("Error");
        }
      });

    } else {
      $.ajax({
        type: "POST",
        url: "/create",
        contentType: "application/json;charset=UTF-8",
        data: JSON.stringify({
          "playlistName": $("#task-modal").find(".form-control").val(),
        }),
        success: function(res) {
          console.log(res.response)
          location.reload();
        },
        error: function() {
          console.log("Error");
        }
      });
    }
  });

  $(".remove").click(function() {
    const remove = $(this)
    $.ajax({
      type: "POST",
      url: "/delete",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "playlistId": remove.data("source")
      }),
      success: function(res) {
        console.log(res.response)
        location.reload();
      },
      error: function() {
        console.log("Error");
      }
    });
  });

  var currentPlaylistId = 0;

  $(document).delegate("tr", "click", function(e) {
    currentPlaylistId = $(this).attr("id");
    $.ajax({
      type: "POST",
      url: "/get_songs",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "playlistId": $(this).attr("id"),
        "playlistName": $(this).children('td:first').text()
      }),
      success: function(res) {
        var data = "<h4>" + res.playlistName + "</h4><ul>";
        $.each(res.song_list, function(i, value) {
          var avg_rating = value.avg_rating;
          if (avg_rating == null) {
            avg_rating = 0;
          }

          data += "<li>" + value.name + " - " + value.artist + " - " + avg_rating + "</li>";
        });
        data += "</ul>";
        data += "<p><input type='text' placeholder='songId' id='songId' /></p><p><input type='submit' value='Add' class='btn btn-outline-info btn-sm' id='songIdSubmit' /></p>";
        $("#playlist_content").html(data);
      },
      error: function() {
        console.log("Error");
      }
    });
  });

  $(document).on("click", "#songIdSubmit", function() {
    $.ajax({
      type: "POST",
      url: "/add_song",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "playlistId": currentPlaylistId,
        "songId": $("#songId").val()
      }),
      success: function(res) {
        if(res.success) {
          alert("Added Song to PlaylistId " + res.data.playlistId);
          location.reload();

        } else {
          alert("SongId does not exist");
        }
      },
      error: function() {
        console.log("Error");
      }
    });
  });


});
