import * as vscode from 'vscode';
import { subscribeToDocumentChanges, PACKAGE_LICENSE_MENTION } from './diagnostics';

const OPEN_DEPENDENCY_LICENSE = 'code-actions-sample.open-dependency-license';

export function activate(context: vscode.ExtensionContext) {


	context.subscriptions.push(
		vscode.languages.registerCodeActionsProvider({ language: 'python', scheme: 'file' }, new CheckLicense(), {
			providedCodeActionKinds: CheckLicense.providedCodeActionKinds
		})
	);

	context.subscriptions.push(
		vscode.commands.registerCommand(OPEN_DEPENDENCY_LICENSE, () => vscode.env.openExternal(vscode.Uri.parse('https://url-of-the-problematic-license.com')))
	);

	const licenseDiagnostics = vscode.languages.createDiagnosticCollection("licenseDiagnostics");
	context.subscriptions.push(licenseDiagnostics);

	subscribeToDocumentChanges(context, licenseDiagnostics);

}

/**
 * Provides code actions corresponding to incompatible license imports.
 */
export class CheckLicense implements vscode.CodeActionProvider {

	public static readonly providedCodeActionKinds = [
		vscode.CodeActionKind.QuickFix
	];

	provideCodeActions(document: vscode.TextDocument, range: vscode.Range | vscode.Selection, context: vscode.CodeActionContext, token: vscode.CancellationToken): vscode.CodeAction[] {
		// for each diagnostic entry that has the matching `code`, create a code action command
		return context.diagnostics
			.filter(diagnostic => diagnostic.code === PACKAGE_LICENSE_MENTION)
			.map(diagnostic => this.createCommandCodeAction(diagnostic));
	}

	private createCommandCodeAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
		const action = new vscode.CodeAction('Open License...', vscode.CodeActionKind.QuickFix);
		action.command = { command: OPEN_DEPENDENCY_LICENSE, title: 'Learn more about emojis', tooltip: 'This will open the unicode emoji page.' };
		action.diagnostics = [diagnostic];
		action.isPreferred = true;
		return action;
	}
}