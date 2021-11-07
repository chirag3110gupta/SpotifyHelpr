$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        console.log("taskId", taskID)
        console.log("taskId", taskID)

        const modal = $(this)
        if (taskID === 'New Playlist') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Playlist ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })


    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        if (tID) {
          console.log("edit", tID)
          $.ajax({
              type: 'POST',
              url: '/edit/' + tID,
              contentType: 'application/json;charset=UTF-8',
              data: JSON.stringify({
                  'songId': $('#task-modal').find('.form-control').val(),
                  'playlistId': tID
              }),
              success: function (res) {
                  console.log(res.response)
                  location.reload();
              },
              error: function () {
                  console.log('Error');
              }
          });

        } else {
          console.log("create", tID)
          $.ajax({
              type: 'POST',
              url: '/create',
              contentType: 'application/json;charset=UTF-8',
              data: JSON.stringify({
                  'playlistName': $('#task-modal').find('.form-control').val(),
              }),
              success: function (res) {
                  console.log(res.response)
                  location.reload();
              },
              error: function () {
                  console.log('Error');
              }
          });
        }
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'playlistId': remove.data('source')
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')
        const new_state = ""
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});
