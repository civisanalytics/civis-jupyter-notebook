define(['jquery'], function($) {
  var uncommitted_changes = function(notificationBoxes) {
    var settings = {
      url: '/git/uncommitted_changes',
      type: 'GET',
      contentType: 'applicaton/json',
      success: function(data) {
        if (data.hasOwnProperty('dirty') && data.dirty) {
          notificationBoxes.uncommittedChanges.css('display', 'inline-block');
          notificationBoxes.noChanges.css('display', 'none');
        } else {
          notificationBoxes.noChanges.css('display', 'inline-block');
          notificationBoxes.uncommittedChanges.css('display', 'none');
        }
      },
      error: function() {
        notificationBoxes.uncommittedChanges.css('display', 'none');
        notificationBoxes.noChanges.css('display', 'none');
      }
    }

    $.ajax(settings)
  }

  function _on_load() {
    var uncommittedChangesBox = '<div id="uncommitted_changes" onclick="window.location.href=\'/terminals/1\'" title="Open terminal to commit" class="notification_widget btn btn-xs navbar-btn" style="display: none"><i class="fa fa-circle"></i><span> Uncommitted Changes </span></div>';
    $('#notification_trusted').before(uncommittedChangesBox);

    var noChangesBox = '<div id="noChanges" class="navbar-btn btn btn-xs" style="display: none"><span> Nothing to Commit </span></div>';
    $('#uncommitted_changes').before(noChangesBox);

    var notificationBoxes = {'uncommittedChanges': $('#uncommitted_changes'), 'noChanges': $('#noChanges')}
    uncommitted_changes(notificationBoxes, null);
    window.setInterval(uncommitted_changes, 3000, notificationBoxes);
  }

  return {load_ipython_extension: _on_load };
})
