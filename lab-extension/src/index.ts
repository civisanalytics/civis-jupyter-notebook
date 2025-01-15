import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
  // Router
  // IRouter
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import {
  terminalIcon,
  caretLeftIcon,
  Spinner,
  ToolbarButton,
  keyboardIcon
} from '@jupyterlab/ui-components'; //
import { TerminalManager, TerminalAPI } from '@jupyterlab/services';
import { Terminal } from '@jupyterlab/terminal';
// import { ITerminal } from '@jupyterlab/services/lib/terminal/terminal';
// import { Widget } from '@lumino/widgets';
import { MainAreaWidget} from '@jupyterlab/apputils';

// import { NotebookActions } from '@jupyterlab/notebook';
import { Dialog } from '@jupyterlab/apputils';

import { initScreenSettings } from './intialLoad';

// "jupyter.lab.menus": {
//   "main": [
//     {
//     "id": "jp-mainmenu-run",
//     "disabled": true
//     }, 
//     {
//       "id": "jp-mainmenu-kernel",
//       "items": [
//         {
//           "command": "kernelmenu:change",
//           "disabled": true
//         }, 
//         {
//           "command": "kernelmenu:shutdownAll",
//           "disabled": true
//         }
//       ]
//     }, 
//     {
//       "id": "jp-mainmenu-file",
//       "items": [
//         {
//           "type": "submenu",
//           "submenu": {
//               "id": "jp-mainmenu-file-new"
//           },
//           "disabled": true
//         },
//         {
//           "command": "notebook:create-new",
//           "disabled": true
//         },
//         {
//           "command": "filemenu:create-console",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:open",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:save",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:save-as",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:close",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:clone",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:rename",
//           "disabled": true
//         },
//         {
//           "command":"application:close", 
//           "disabled": true
//         },
//         {
//           "command": "docmanager:reload",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:duplicate",
//           "disabled": true
//         },
//         {
//           "command": "docmanager:restore-rename",
//           "disabled":true
//         },
//         {
//           "command": "docmanager:restore-checkpoint",
//           "disabled":true
//         },
//         {
//           "command": "filebrowser:open-path",
//           "disabled": true
//         },
//         {
//           "command": "jp-mainmenu-file-new",
//           "disabled": true
//         },
//         {
//           "command": "launcher:create",
//           "disabled": true
//         },
//         {
//           "command": "application:close-all",
//           "disabled": true
//         },
//         {
//           "command": "hub:control-panel", 
//           "disabled":true
//         },
//         {
//           "type": "submenu",
//           "submenu": {
//             "id": "jp-mainmenu-file-workspaces"
//           },
//           "disabled": true
//         },
//         {
//           "command": "workspace-ui",
//           "disabled": true
//         }, 
//         {
//           "command": "filemenu:shutdown",
//           "disabled": true
//         }, 
//         {
//           "command": "filemenu:logout",
//           "disabled": true
//         }
//       ]
//     }, 
//     {
//       "id": "jp-mainmenu-tabs",
//       "disabled": true
//     }, 
//     {
//       "id": "jp-mainmenu-view",
//       "items": [
//         {
//           "command": "apputils:display-notifications",
//           "disabled": true
//         },
//         {
//           "command": "logconsole:open",
//           "disabled": true
//         },
//         {
//           "command": "application:toggle-presentation-mode",
//           "disabled": true
//         }
//       ]
//     }
//   ]
// },


// import { MainAreaWidget } from '@jupyterlab/apputils';
// import { Widget } from '@lumino/widgets';

// import {} from '@jupyterlab/terminal-extension';

/**
 * Initialization data for the civis-jupyter-notebook-extensions extension.
 */

// extension examples: https://github.com/jupyterlab/extension-examples

// commands
// https://jupyterlab.readthedocs.io/en/stable/user/commands.html

// classes
// https://jupyterlab.readthedocs.io/en/stable/api/classes/ui_components.ToolbarButton.html

// icons
// https://github.com/jupyterlab/jupyterlab/blob/main/packages/ui-components/src/icon/iconimports.ts

// extension points
// https://jupyterlab.readthedocs.io/en/latest/extension/extension_points.html#toolbar-item

// interface (toolbars, menus, etc) customization
// https://jupyterlab.readthedocs.io/en/latest/user/interface_customization.html

// disable extensions
// https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#disabling-other-extensions
//    "jupyterlab": {
//       "disabledExtensions": ["@jupyterlab/filebrowser-extension:share-file"]
//    }

// list of extensions
// https://jupyterlab.readthedocs.io/en/4.2.x/user/commands.html


const plugin: JupyterFrontEndPlugin<void> = {
  id: 'civis-jupyter-notebook-extensions:plugin',
  description: 'Extensions for use in Jupyter Notebook in Civis Platform.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('Civis JupyterLab extension is activated!');
    //load settings from the setting registry /schema/plugin.json
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log(
            'Civis JupyterLab extension settings loaded:',
            settings.composite
          );
          
          initScreenSettings(app);
          // app.commands.execute('civis-open-notebook');
          // app.commands.execute('civis:init-screen-settings');
        })
        .catch(reason => {
          console.error(
            'Failed to load Civis JupyterLab extension settings.',
            reason
          );
        });
    }
    const { commands } = app;
    
    // app.formatChanged.connect(() => {
    //   console.log('format changed');
    // });
    // app.started.then(() => {
    //   // const headerTopPanel = document.getElementById('jp-top-panel');
    //   // const main = document.getElementById('main');
    //   // console.log('headerTopPanel', headerTopPanel);
    //   // if (headerTopPanel && main) {
    //   //   headerTopPanel.style.display = 'none';
    //   //   main.style.minHeight = '112px';
    //   // }
    //   // const statusBarPanel = document.getElementById('jp-main-statusbar');
    //   // if (statusBarPanel) {
    //   //   statusBarPanel.style.display = 'none';
    //   // } 
    //   // console.log('app started');
    //   setTimeout(() => {
    //     console.log(commands.execute('application:toggle-header'));
    //     commands.execute('application:toggle-header');
    //     console.log('header toggled');
    //   }, 10000);
    // });
    
    // commands.execute('application:toggle-header');
    // create close terminal button and it's function for use in terminal "toolbar"
    // try to get this into the actual toolbar available from MainWidgetArea,
    // possibly using this as reference: https://github.com/jupyterlab/extension-examples/blob/main/contentheader/README.md
    const closeTerminalButton = new ToolbarButton({ label: 'Close Terminal' });
    closeTerminalButton.id = 'civis-close-terminal-button';
    closeTerminalButton.node.innerHTML = 'Notebook';
    closeTerminalButton.node.prepend(
      caretLeftIcon.element({
        tag: 'span',
        className: 'civis-jp-Icon civis-jp-Icon-20'
      })
    );
    closeTerminalButton.node.onclick = () => {
      const terminalPanel = app.shell.currentWidget;
      if (terminalPanel) {
        terminalPanel.dispose();
      }
    };
    commands.addCommand('civis-open-notebook', {
      label: 'Open Notebook',
      icon: terminalIcon,
      execute: async () => {
        commands.execute('docmanager:open', {
          path: 'Untitled.ipynb'
        });
      }
    });
    commands.addCommand('civis:show-keyboard-shortcuts', {
      label: 'Show Keyboard Shortcuts',
      icon: keyboardIcon,
      execute: async () => {
        // commands.execute('settingeditor:open', { plugin: 'jupyterlab-keyboard-shortcuts:plugin' });
        commands.execute('apputils:display-shortcuts');


      }
    });
    // create a widget to hold the close terminal button
    // const civisTerminalToolbarWidget = new Widget();
    // civisTerminalToolbarWidget.id = 'civis-terminal-toolbar';
    // civisTerminalToolbarWidget.title.label = 'Terminal Toolbar';
    // civisTerminalToolbarWidget.node.appendChild(closeTerminalButton.node);
    const manager = new TerminalManager();

    // commands.addCommand('civis:init-screen-settings', {
    //   label: 'Toggle Header',
    //   icon: terminalIcon,
    //   execute: async () => {
    //     app.started.then(() => {
    //       setTimeout(() => {
    //         if (
    //           !document
    //             .getElementById('jp-top-panel')
    //             ?.classList.contains('lm-mod-hidden')
    //         ) {
    //           commands.execute('application:toggle-header');
    //         }
    //         if (
    //           !document
    //             .getElementById('jp-main-statusbar')
    //             ?.classList.contains('lm-mod-hidden')
    //         ) {
    //           console.log(document.getElementById('jp-main-statusbar'));
    //           commands.execute('statusbar:toggle');
    //         }
    //       }, 250);
    //     });
    //   }
    // });
    // add command to open terminal, which is called in plugin.json
    commands.addCommand('civis:open-terminal', {
      label: 'Open Teminal',
      iconLabel: 'Open Terminal',
      icon: terminalIcon,
      execute: async () => {
        // create a dialog box to show while terminal is loading
        const terminalMessage = new Dialog({
          title: 'Loading Terminal',
          body: new Spinner(),
          buttons: []
        });
        terminalMessage.launch();

        // open existing terminal if api returns terminals or create a new one and load it in the main area of the widget
        try {
          // const manager = new TerminalManager();

          const api = TerminalAPI;
          const terminalList = await api.listRunning();
          console.log('terminalList', terminalList);  
          // commands.execute('application:toggle-header');
          // create widget to hold terminal toolbar and add it to MainAreaWidget
          // reference: https://github.com/jupyterlab/extension-examples/tree/main/custom-log-console
          let terminal: Terminal | null = null;

          if (terminalList.length > 0) {
            terminal = new Terminal(
              manager.connectTo({
                model: { name: terminalList[0].name }
              })
            );
          } else {
            const termPanel = await manager.startNew();
            console.log('termPanel', termPanel);
            terminal = new Terminal(
              manager.connectTo({ model: termPanel.model })
            );
          }
          // add the terminal toolbar to the terminal widget
          // terminal.node.appendChild(civisTerminalToolbarWidget.node);
          const terminalPanelWidget = new MainAreaWidget({
            content: terminal
          });
          // close the dialog box and open the terminal in the main area
          terminalMessage.reject();
          terminalMessage.dispose();
          app.shell.add(terminalPanelWidget, 'main');
        } catch (error) {
          // to do: add better error handling, including error message to Notifications
          // notifications: https://github.com/jupyterlab/extension-examples/tree/main/notifications
          console.error('Error opening terminal:', error);
          terminalMessage.reject();
          terminalMessage.dispose();
        }

        // message.launch();
        // if (terminalList.length > 0) {
        //   console.log('Connecting to existing terminal:', terminalList[0].name);
        //   manager.connectTo({
        //     model: { name: terminalList[0].name.toString() }
        //   });
        //   const node = document.createElement('div');
        //   node.textContent = 'Hello World';

        //   const main = app.shell.currentWidget;
        //   if (main instanceof MainAreaWidget) {
        //     // Create a widget
        //     // const widget = new Widget();
        //     // widget.addClass('example-extension-contentheader-widget');
        //     // widget.node.textContent = "hello world!";
        //     // widget.node.style.color = 'red';
        //     // widget.node.style.backgroundColor = 'yellow';
        //     // widget.node.style.position = 'relative';
        //     // // set the height so that it is visible
        //     // widget.node.style.minHeight = '20px';
        //     // widget.node.style.display = 'block';
        //     // // const mainPanel = document.getElementById('jp-main-dock-panel');
        //     // // and insert it into the header
        //     // commands.execute('terminal:open');
        //     // document.insertBefore(widget.node, mainPanel);
        //     // const mainMenu = document.getElementById('jp-MainMenu');
        //     // mainMenu?.insertAdjacentElement('beforeend', widget.node);

        //     // setTimeout(() => {
        //     //   const mainPanel = document.getElementById('jp-main-dock-panel');
        //     //   mainPanel?.parentElement?.appendChild(widget.node);
        //     //   const terminalDisplay =
        //     //     mainPanel && mainPanel.querySelector('[role]="tabpanel"');
        //     //   if (terminalDisplay) {
        //     //     (terminalDisplay as HTMLElement).style.top = '20px';
        //     //   }
        //     // }, 15000);
        //   }

        //   // Create the widget
        //   // const widget = new Widget({ node });
        //   // const TOP_AREA_CSS_CLASS = 'jp-TopAreaText';
        //   // widget.id = DOMUtils.createDomID();
        //   // widget.addClass(TOP_AREA_CSS_CLASS);

        //   // // Add the widget to the top area
        //   // app.shell.add(widget, 'top', { rank: 1000 });

        //   // console.log('window location', window.location.href);

        //   // const start = api.startNew();
        //   // start.then((model: any) => {
        //   //   console.log('model', model);
        //   //   model.name = terminalList[0].name;
        //   //   manager.connectTo({
        //   //     model: model
        //   //   });
        //     // const terminal = manager.connectTo({ model: model });

        //     // const widget = new MainAreaWidget({ content: terminal });
        //     // app.shell.add(widget);
        //     // console.log('router', router);
        //     // router.navigate('/terminals/' + model.name, { hard: true });
        // } else {
        //   console.log('starting new terminal');

        //   manager.startNew();
        // }
        // setTimeout(() => {
        //   message.dispose();
        // }, 2000);
      }
    });
  }
};

export default plugin;
