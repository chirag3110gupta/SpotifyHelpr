$(document).ready(function() {
  // example: https://getbootstrap.com/docs/4.2/components/modal/
  // show modal
  $("#task-modal").on("show.bs.modal", function(event) {
    const button = $(event.relatedTarget) // Button that triggered the modal
    const taskID = button.data("source") // Extract info from data-* attributes
    const content = button.data("content") // Extract info from data-* attributes
    const modal = $(this)

    if (taskID === "New Friend") {
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
    $.ajax({
      type: "POST",
      url: "/create_friend",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "friendId": $("#task-modal").find(".form-control").val(),
      }),
      success: function(res) {
        if(res.success) {
          alert("Added FriendId " + res.data.friendId);
          location.reload();

        } else {
          alert("FriendId does not exist");
        }
      },
      error: function() {
        console.log("Error");
      }
    });
  });

  $(".remove").click(function() {
    const remove = $(this)
    $.ajax({
      type: "POST",
      url: "/delete_friend",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "friendId": remove.data("source")
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

  //$(document).delegate("tr", "click", function(e) {
  //  currentPlaylistId = $(this).attr("id");
  //  $.ajax({
  //    type: "POST",
  //    url: "/get_songs",
  //    contentType: "application/json;charset=UTF-8",
  //    data: JSON.stringify({
  //      "playlistId": $(this).attr("id"),
  //      "playlistName": $(this).children('td:first').text()
  //    }),
  //    success: function(res) {
  //      var data = "<h4>" + res.playlistName + "</h4><ul>";
  //      $.each(res.song_list, function(i, value) {
  //        var avg_rating = value.avg_rating;
  //        if (avg_rating == null) {
  //          avg_rating = 0;
  //        }

  //        data += "<li>" + value.name + " - " + value.artist + " - " + avg_rating + "</li>";
  //      });
  //      data += "</ul>";
  //      data += "<p><input type='text' placeholder='songId' id='songId' /></p><p><input type='submit' value='Add' class='btn btn-outline-info btn-sm' id='songIdSubmit' /></p>";
  //      $("#playlist_content").html(data);
  //    },
  //    error: function() {
  //      console.log("Error");
  //    }
  //  });
  //});
});
