define(['base/js/namespace'], function(Jupyter) {
  function _on_load() {
    var action = {
      icon: 'fa-terminal',
      help: 'Open Terminal',
      handler: function(env, event) {
        env.notebook.save_checkpoint();
        if (event) {
          event.preventDefault();
        }
        window.location.href = "/terminals/1";
      }
    };

    var prefix = 'terminal';
    var action_name = 'open-terminal';
    var full_action_name = Jupyter.actions.register(action, action_name, prefix);
    Jupyter.toolbar.add_buttons_group([full_action_name]);
  }

  return { load_ipython_extension: _on_load };
});
