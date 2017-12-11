define(['jquery'], function($) {
  var uncommitted_changes = function(elem) {
    var settings = {
      url: '/git/uncommitted_changes',
      type: 'GET',
      contentType: 'applicaton/json',
      success: function(data) {
        if (data.hasOwnProperty('has_uncommitted_changes') && data.has_uncommitted_changes) {
          elem.css('display', 'inline-block');
        } else {
          elem.css('display', 'none');
        }
      },
      error: function() {
        elem.css('display', 'none');
      }
    }

    $.ajax(settings)
  }

  function _on_load() {
    var notificationBox = '<div id="uncommitted_changes" class="notification_widget btn btn-xs navbar-btn" style="display: none"><span>Uncommitted Changes</span></div>'
    $('#notification_trusted').before(notificationBox);
    elem = $('#uncommitted_changes')

    uncommitted_changes(elem);
    window.setInterval(uncommitted_changes, 3000, elem);
  }

  return {load_ipython_extension: _on_load };
})
