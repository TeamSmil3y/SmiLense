import * as vscode from 'vscode';
import { checkPackageValidity } from './isPackageValid';

/** Code that is used to associate diagnostic entries with code actions. */
export const PACKAGE_LICENSE_MENTION = 'package_license_mention';

/** String to detect import package statement in a file. */
const IMPORT_KEYWORD = 'import';

/**
 * Analyzes the text document for problems. 
 * This demo diagnostic problem provider finds all mentions of 'emoji'.
 * @param doc text document to analyze
 * @param licenseDiagnostics diagnostic collection
 */
export function refreshDiagnostics(doc: vscode.TextDocument, licenseDiagnostics: vscode.DiagnosticCollection): void {
	const diagnostics: vscode.Diagnostic[] = [];

	for (let lineIndex = 0; lineIndex < doc.lineCount; lineIndex++) {
		const lineOfText = doc.lineAt(lineIndex);
		if (lineOfText.text.includes(IMPORT_KEYWORD) && lineOfText.text.trim() !== IMPORT_KEYWORD) {
			diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex));
		}
	}

	licenseDiagnostics.set(doc.uri, diagnostics);
}

function createPackageLicenseDiagnostic(doc: vscode.TextDocument, lineOfText: vscode.TextLine, lineIndex: number): vscode.Diagnostic {

	let checkPackage = lineOfText.text.split(" ").pop() || "";

	console.log({ checkPackage })

	checkPackageValidity(checkPackage).then(encodedData => {
		console.log({ checkPackageValidity: encodedData });
	});

	// find where in the line of that the checkPackage is mentioned
	const index = lineOfText.text.indexOf(checkPackage);

	// create range that represents, where in the document the word is
	const range = new vscode.Range(lineIndex, index, lineIndex, index + checkPackage.length);

	const diagnostic = new vscode.Diagnostic(range, "This package's license might be incompatible with your project",
		vscode.DiagnosticSeverity.Information);
	diagnostic.code = PACKAGE_LICENSE_MENTION;
	return diagnostic;
}

export function subscribeToDocumentChanges(context: vscode.ExtensionContext, licenseDiagnostics: vscode.DiagnosticCollection): void {
	if (vscode.window.activeTextEditor) {
		refreshDiagnostics(vscode.window.activeTextEditor.document, licenseDiagnostics);
	}
	context.subscriptions.push(
		vscode.window.onDidChangeActiveTextEditor(editor => {
			if (editor) {
				refreshDiagnostics(editor.document, licenseDiagnostics);
			}
		})
	);

	context.subscriptions.push(
		vscode.workspace.onDidChangeTextDocument(e => refreshDiagnostics(e.document, licenseDiagnostics))
	);

	context.subscriptions.push(
		vscode.workspace.onDidCloseTextDocument(doc => licenseDiagnostics.delete(doc.uri))
	);

}