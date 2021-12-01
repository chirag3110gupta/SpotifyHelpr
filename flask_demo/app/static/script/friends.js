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

  $(document).delegate("tr", "click", function(e) {
    $.ajax({
      type: "POST",
      url: "/get_averages",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "friendId": $(this).attr("id")
      }),
      success: function(res) {

        console.log(res);

        if(res.user_data.length > 0 && res.friends_data.length > 0) {
          $("#myChart").remove();
          $("div.chart_container").append("<canvas id='myChart' height='600' width='600'></canvas>");
          let myChart = document.getElementById("myChart").getContext('2d');
          let radarChart = new Chart(myChart, {
            type: "radar",
            data: {
              labels: ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "speechiness"],
              datasets: [{
                label: "User",
                data: [
                  res.user_data[0].acousticness,
                  res.user_data[0].danceability,
                  res.user_data[0].energy,
                  res.user_data[0].instrumentalness,
                  res.user_data[0].liveness,
                  res.user_data[0].speechiness
                ],
                backgroundColor: [
                    "rgba(255, 0, 0, 0.2)"
                ],
                borderColor: [
                    "rgba(255, 0, 0, .4)"
                ]
              }, {
                label:"Friend",
                data: [
                  res.friends_data[0].acousticness,
                  res.friends_data[0].danceability,
                  res.friends_data[0].energy,
                  res.friends_data[0].instrumentalness,
                  res.friends_data[0].liveness,
                  res.friends_data[0].speechiness
                ],
                backgroundColor:[
                    "rgba(0, 0, 255, 0.2)"
                ],
                borderColor: [
                    "rgba(0, 0, 255, .4)"
                ]
              }]
            },
            options: {
              responsive: false,
              elements: {
                line: {
                  borderWidth: 3
                }
              }
            }
          })
        } else {
          alert("user or friend has no songs added");
        }
      },
      error: function() {
        console.log("Error");
      }
    });
  });
});
