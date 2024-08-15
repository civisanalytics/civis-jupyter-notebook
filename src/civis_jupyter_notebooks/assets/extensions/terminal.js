define(['base/js/namespace'], function(Jupyter) {
  function _on_load() {

    /*
    The following helper functions _ajax, _add_auth_header, and _get_cookie are from
    https://github.com/jupyter/nbclassic/blob/b6257e966f47951b49f661bd129de1fc794079c2/nbclassic/static/base/js/utils.js.

    Copyright (c) Jupyter Development Team.
    Distributed under the terms of the Modified BSD License.

    There does not appear to be an easier way to create a new terminal using the Jupyter API.
    */
    let _ajax = function (url, settings) {
      // like $.ajax, but ensure XSRF or Authorization header is set
      if (typeof url === "object") {
          // called with single argument: $.ajax({url: '...'})
          settings = url;
          url = settings.url;
          delete settings.url;
      }
      settings = _add_auth_header(settings);
      return $.ajax(url, settings);
    };

    let _add_auth_header = function (settings) {
      /**
       * Adds auth header to jquery ajax settings
       */
      settings = settings || {};
      if (!settings.headers) {
          settings.headers = {};
      }
      if (!settings.headers.Authorization) {
          let xsrf_token = _get_cookie('_xsrf');
          if (xsrf_token) {
              settings.headers['X-XSRFToken'] = xsrf_token;
          }
      }
      return settings;
    };

    let _get_cookie = function (name) {
      // from tornado docs: http://www.tornadoweb.org/en/stable/guide/security.html
      let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    }

    let terminalLoading = false;

    let action = {
      icon: 'fa-terminal',
      help: 'Open Terminal',
      handler: function(env) {
        if (terminalLoading) {
          // Avoid creating a bunch of terminals if the user clicks
          // multiple times before the redirect happens.
          return;
        }

        terminalLoading = true;
        env.notebook.save_checkpoint();
        env.notebook.set_dirty(false);

        // stop pop up from displaying
        window.onbeforeunload = function(){}
        let _errorHandler = function(jqXHR, status, error) {
          w.close();
          console.log(jqXHR);
          terminalLoading = false;
        };

        let w = window.open('#', IPython._target);
        _ajax('/api/terminals', {
          type: "GET",
          dataType: "json",
          success: function(terminalList) {
            if (terminalList.length > 0) {
              // If there's already a terminal, go to it.
              w.location = `/terminals/${terminalList[0].name}`;
              terminalLoading = false;
            } else {
              // Otherwise, create a new one first.
              _ajax('/api/terminals', {
                type: "POST",
                dataType: "json",
                success: function(response) {
                  w.location = `/terminals/${response.name}`;
                  terminalLoading = false;
                },
                error: _errorHandler
              });
            };

          },
          error: _errorHandler
        });
      }
    };

    let prefix = 'terminal';
    let action_name = 'open-terminal';
    let full_action_name = Jupyter.actions.register(action, action_name, prefix);
    Jupyter.toolbar.add_buttons_group([full_action_name], 'terminal');
  }

  return { load_ipython_extension: _on_load };
});
