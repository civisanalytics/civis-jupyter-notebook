import { JupyterFrontEnd } from '@jupyterlab/application';

export const initScreenSettings = (app: JupyterFrontEnd) => {
  setTimeout(() => {
    if (
      !document
        .getElementById('jp-top-panel')
        ?.classList.contains('lm-mod-hidden')
    ) {
      app.commands.execute('application:toggle-header');
    }
    if (
      !document
        .getElementById('jp-main-statusbar')
        ?.classList.contains('lm-mod-hidden')
    ) {
      app.commands.execute('statusbar:toggle');
    }
  }, 250);
};
