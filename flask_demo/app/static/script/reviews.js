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
      modal.find(".modal-title").text("Edit Review " + taskID)
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
      url: "/create_review",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "rating": $("#task-modal").find(".rating-input").val(),
        "body": $("#task-modal").find(".body-input").val(),
        "songId": $("#task-modal").find(".songId-input").val()
      }),
      success: function(res) {
        if(res.success) {
          alert("Created Review");
          location.reload();

        } else {
          alert("Some input invalid. Make sure rating is a number and songId exists");
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
      url: "/delete_review",
      contentType: "application/json;charset=UTF-8",
      data: JSON.stringify({
        "reviewId": remove.data("source")
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
});
