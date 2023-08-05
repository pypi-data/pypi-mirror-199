import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { ILatexTypesetter } from '@jupyterlab/rendermime';

// MathJax core
import { mathjax } from 'mathjax-full/js/mathjax';

// TeX input
import { TeX } from 'mathjax-full/js/input/tex';

// HTML output
import { CHTML } from 'mathjax-full/js/output/chtml';

import { TeXFont } from 'mathjax-full/js/output/chtml/fonts/tex';

import { AllPackages } from 'mathjax-full/js/input/tex/AllPackages';

import { SafeHandler } from 'mathjax-full/js/ui/safe/SafeHandler';

import { HTMLHandler } from 'mathjax-full/js/handlers/html/HTMLHandler';

import { browserAdaptor } from 'mathjax-full/js/adaptors/browserAdaptor';

import 'mathjax-full/js/input/tex/require/RequireConfiguration';

mathjax.handlers.register(SafeHandler(new HTMLHandler(browserAdaptor())));

class emptyFont extends TeXFont {}
(emptyFont as any).defaultFonts = {};

export class MathJax3Typesetter implements ILatexTypesetter {
  constructor(app: JupyterFrontEnd) {
    const chtml = new CHTML({
      font: new emptyFont()
    });
    const tex = new TeX({
      packages: AllPackages.concat('require'),
      inlineMath: [
        ['$', '$'],
        ['\\(', '\\)']
      ],
      displayMath: [
        ['$$', '$$'],
        ['\\[', '\\]']
      ],
      processEscapes: true,
      processEnvironments: true,
      maxBuffer: 5000000000 * 1024
    });
    this._mathDocument = mathjax.document(window.document, {
      InputJax: tex,
      OutputJax: chtml
    });
    console.log(tex);
    const mjclipboard = 'mathjax:clipboard';
    const mjscale = 'mathjax:scale';

    app.commands.addCommand(mjclipboard, {
      execute: (args: any) => {
        const md = this._mathDocument;
        const oJax: any = md.outputJax;
        navigator.clipboard.writeText(oJax.math.math);
      },
      label: 'MathJax Copy Latex'
    });

    app.commands.addCommand(mjscale, {
      execute: (args: any) => {
        const scale = args['scale'] || 1.0;
        const md = this._mathDocument;
        md.outputJax.options.scale = scale;
        md.rerender();
      },
      label: (args: any) =>
        'Mathjax Scale ' + (args['scale'] ? `x${args['scale']}` : 'Reset')
    });
  }

  /**
   * Typeset the math in a node.
   */
  typeset(node: HTMLElement): void {
    this._mathDocument.options.elements = [node];
    this._mathDocument.clear().render();
    delete this._mathDocument.options.elements;
  }

  private _mathDocument: ReturnType<typeof mathjax.document>;
}

/**
 * Initialization data for the jijzeptlab-mathjax extension.
 */
const plugin: JupyterFrontEndPlugin<ILatexTypesetter> = {
  id: 'jijzeptlab-mathjax:plugin',
  autoStart: true,
  // optional: [ISettingRegistry],
  provides: ILatexTypesetter,
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) =>
    new MathJax3Typesetter(app)
};

export default plugin;
