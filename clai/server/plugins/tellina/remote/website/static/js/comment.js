/* A set of library functions for commenting annotations. */

// open a comment box
function open_comment_panel(object, comment_id, comment_place_holder) {
    object.append(
        `<div class="comment-panel" id="comment-panel-${comment_id}">
            <textarea class="form-control comment-input vresize" placeholder="${comment_place_holder}"></textarea>
            <br>
            <button type="button" class="btn btn-primary btn-sm submit-update" style="float: right">Submit</button>
            <button type="button" class="btn btn-default btn-sm cancel-update" style="float: right; margin-right: 20px;">Cancel</button>
        </div>
        <br>`
    );
    set_up_comment_panel(object, comment_id);
}

function set_up_comment_panel(object, comment_id) {
    var annotation_box = object.closest('.annotation-box');
    var comment_panel = object.find(`#comment-panel-${comment_id}`);
    var change_object = annotation_box.find('.nl-submission');
    var submit_btn = comment_panel.find('.submit-update');
    var cancel_btn = comment_panel.find('.cancel-update');

    // submit-button click wraps the update (same value as object) and comment
    // and wraps them in a panel appended to object
    submit_btn.click(function() {
        var update = change_object.text();
        var comment = comment_panel.find('.comment-input').val();
        if (comment.length < 10) {
            alert("Please explain your rejection of the modification in more detail.");
        } else {
            var annotation_backend_id = annotation_box.find('.backend-id').text();
            console.log(annotation_backend_id);
            var update_backend_id = object.find('.comment-backend-id').text();
            $.get(`reject_update`, {update_id: update_backend_id});
            $.get(`submit_annotation_update`, {annotation_id: annotation_backend_id,
                    update: update, comment: comment, update_id: update_backend_id}, function(data) {
                if (data.status == 'ANNOTATION_UPDATE_SAVE_SUCCESS') {
                    change_object.show();
                    object.find('.accept-update').hide();
                    object.find('.reject-update').hide();
                    object.find('.change-update').hide();
                    comment_panel.remove();
                    var update_id = add_update_and_comment(annotation_box, data.access_code,
                        data.submission_time, update, comment, 'by-author', data.update_id);
                    set_up_update_and_comment(update_id, data.update_id,
                            annotation_box, data.access_code)
                }
            });
        }
    });

    cancel_btn.click(function() {
        comment_panel.remove();
    });
}

// change the content of an object and open a comment box
function open_change_and_comment_panel(object, object_type, comment_id, comment_place_holder) {
    var change_object = object.find('.nl-submission');
    object.append(
        `<div class="comment-panel" id="comment-panel-${comment_id}">
            <br>
            <br>
            <textarea class="form-control comment-input vresize" placeholder="${comment_place_holder}"></textarea>
            <br>
            <button type="button" class="btn btn-primary btn-sm submit-update" style="float: right">Submit</button>
            <button type="button" class="btn btn-default btn-sm cancel-update" style="float: right; margin-right: 20px;">Cancel</button>
            <br>
        </div>`
    );
    set_up_change_and_comment_panel(object, object_type, comment_id);
}

function set_up_change_and_comment_panel(object, object_type, comment_id) {
    var comment_panel = object.find(`#comment-panel-${comment_id}`);
    var annotation_box = object;
    var change_object = object.find('.nl-submission');
    var change_object_input = object.find('.nl-submission-edit-input');
    var submit_btn = comment_panel.find('.submit-update');
    var cancel_btn = comment_panel.find('.cancel-update');
    // submit-button click checks the update and comment are valid and wraps
    // them in a panel appended to object
    submit_btn.click(function() {
        if (change_object_input.val() != change_object.text()) {
            var comment = comment_panel.find('.comment-input').val();
            if (comment.length < 10) {
                alert("Please explain your edits in more detail for the reference of others.");
            } else {
                var annotation_backend_id = annotation_box.find('.backend-id').text();
                var update = change_object_input.val();
                $.get(`submit_annotation_update`, {annotation_id: annotation_backend_id, update: update, comment: comment}, function(data) {
                    if (data.status == 'ANNOTATION_UPDATE_SAVE_SUCCESS') {
                        change_object.show();
                        change_object.find('.nl-submission-edit').hide();
                        change_object_input.hide();
                        comment_panel.remove();
                        var update_id = add_update_and_comment(object, data.access_code,
                            data.submission_time, update, comment, 'by-judger', data.update_id);
                        set_up_update_and_comment(update_id, data.update_id,
                            annotation_box, data.access_code)
                    }
                });
            }
        }
    });

    // cancel-button click restores the change object display and hide the
    // change object input box; it also destroys the comment panel object
    cancel_btn.click(function() {
        object.find('.nl-submission-edit-input').hide();
        comment_panel.remove();
        change_object.show();
    });
}

function add_update_and_comment(object, user_id, submission_time, update, comment, comment_box_type, update_backend_id) {
    // add a main level comment to an annotation
    var comment_list = object.find('.comment-list');
    var update_id = comment_list.children().length;
    comment_list.append(
        `<li>
            <div class="comment-box" id="comment-box-${update_id}">
                <div class="comment-backend-id" style="display: none">${update_backend_id}</div>
                <div class="comment-head">
                    <div class="comment-name ${comment_box_type}">${user_id}</div>
                    <span class="submission-time">${submission_time}</span>
                </div>
                <div class="update-content">
                    ${update}<!-- <i class="glyphicon glyphicon-pencil update-content-edit" style="float: right"></i> -->
                </div>
                <div class="comment-content">
                    <i class="glyphicon glyphicon-list-alt"></i>&nbsp;${comment}
                    <div class="tiny-push"></div>
                </div>
            </div>
        </li>`
    );
    return update_id;
}

// set up annotation update display panel
function set_up_update_and_comment(update_id, update_backend_id, annotation_box, access_code) {
    var comment_box = annotation_box.find(`#comment-box-${update_id}`);
    var num_updates = annotation_box.find('.comment-list').children().length;
    $.get(`get_update_status`, {update_id: update_backend_id}, function(data) {
        if (data.update_status == 'open') {
            // append retract or reply button if there is no replies on the updates yet
            var update_user = comment_box.find('.comment-name').text();
            if (update_user != access_code) {
                // append reply button
                comment_box.append(
                     `<button type="button" class="btn btn-default btn-sm change-update" id="change-update-${update_id}" style="float: right; margin-right: 20px">Change
                     </button>
                     <button type="button" class="btn btn-warning btn-sm reject-update" id="reject-update-${update_id}" style="float: right; margin-right: 20px">Reject
                     </button>
                     <button type="button" class="btn btn-primary btn-sm accept-update" id="accept-update-${update_id}" style="float: right; margin-right: 20px">Accept
                     </button>
                     <br>
                    `);

                comment_box.find(`#accept-update-${update_id}`).click(function() {
                    $.get(`accept_update`, {update_id: update_backend_id}, function(data) {
                        if (data.status == 'ACCEPT_UPDATE_SUCCESS') {
                            annotation_box.find('.nl-submission').text(data.updated_str);
                            annotation_box.find('.edit-pair').show();
                            comment_box.hide();
                        }
                    });
                });

                comment_box.find(`#reject-update-${update_id}`).click(function() {
                    open_comment_panel(comment_box, update_id, 'Leave a comment for rejecting the modification request...');
                });

                /* comment_box.find(`#change-update-${update_id}`).click(function() {
                    open_comment_panel(comment_box, update_id, 'Leave a comment for your changes on the modification request...');
                }); */
            } else {
                // append retract button
                comment_box.append(
                    `<button type="button" class="btn btn-warning btn-sm retract-update" id="retract-update-${update_id}" style="float: right">Retract</button>
                     <br>
                    `);
                comment_box.find(`#retract-update-${update_id}`).click(function() {
                    $.get(`retract_update`, {update_id: update_backend_id}, function(data) {
                        if (data.status == 'RETRACT_UPDATE_SUCCESS') {
                            comment_box.remove();
                        }
                    });
                });
            }
        }
    });
}