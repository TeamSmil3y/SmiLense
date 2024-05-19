import * as vscode from 'vscode';
import { checkPackageValidity } from './isPackageValid';

// 0 : compatible (no-colour)
// 1 : almost compatible (blue)
// 2 : might be compatible (yellow)
// 3 : incompatible (red)
// 4 : not found (orange)
export const LICENSE_COMPATIBLE = '0';
export const LICENSE_ALMOST_COMPATIBLE = '1';
export const LICENSE_MIGHT_BE_COMPATIBLE = '2';
export const LICENSE_INCOMPATIBLE = '3';
export const LICENSE_NOT_FOUND = '4';

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
export async function refreshDiagnostics(doc: vscode.TextDocument, licenseDiagnostics: vscode.DiagnosticCollection): Promise<void> {
	const diagnostics: vscode.Diagnostic[] = [];

	for (let lineIndex = 0; lineIndex < doc.lineCount; lineIndex++) {
		const lineOfText = doc.lineAt(lineIndex);
		if (lineOfText.text.includes(IMPORT_KEYWORD) && lineOfText.text.trim() !== IMPORT_KEYWORD) {

			// check if its a valid package
			let checkPackage = lineOfText.text.split(" ").pop() || "";

			let checkPackageOutput: any = await checkPackageValidity(checkPackage)
			let isValidPackage = checkPackageOutput === "0";

			if (!isValidPackage) {
				diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex, checkPackageOutput));
			}

		}
	}

	licenseDiagnostics.set(doc.uri, diagnostics);
}

function createPackageLicenseDiagnostic(doc: vscode.TextDocument, lineOfText: vscode.TextLine, lineIndex: number, checkPackageOutput: any): vscode.Diagnostic {

	let checkPackage = lineOfText.text.split(" ").pop() || "";

	// find where in the line of that the checkPackage is mentioned
	const index = lineOfText.text.indexOf(checkPackage);

	// create range that represents, where in the document the word is
	const range = new vscode.Range(lineIndex, index, lineIndex, index + checkPackage.length);

	let diagnosticSeverity: vscode.DiagnosticSeverity = vscode.DiagnosticSeverity.Information
	let diagnosticMessages = []
	let totalProblems = 0

	if (checkPackageOutput.hasOwnProperty("1")) {
		diagnosticSeverity = vscode.DiagnosticSeverity.Information
		diagnosticMessages.push(`${checkPackageOutput["1"].length} license(s) almost compatible`)
		totalProblems += checkPackageOutput["1"].length
	}
	
	if (checkPackageOutput.hasOwnProperty("2")) {
		diagnosticSeverity = vscode.DiagnosticSeverity.Hint
		diagnosticMessages.push(`${checkPackageOutput["2"].length} license(s) might be compatible`)
		totalProblems += checkPackageOutput["2"].length
	}
	
	if (checkPackageOutput.hasOwnProperty("4")) {
		diagnosticSeverity = vscode.DiagnosticSeverity.Warning
		diagnosticMessages.push(`${checkPackageOutput["4"].length} license(s) not found`)
		totalProblems += checkPackageOutput["4"].length
	}
	
	if (checkPackageOutput.hasOwnProperty("3")) {
		diagnosticSeverity = vscode.DiagnosticSeverity.Error
		diagnosticMessages.push(`${checkPackageOutput["3"].length} license(s) incompatible`)
		totalProblems += checkPackageOutput["3"].length
	}

	const diagnostic = new vscode.Diagnostic(range, `This package's license has ${totalProblems} problem(s)`,
	diagnosticSeverity);
	diagnostic.code = "1";
	diagnostic.message = diagnosticMessages.reverse().join('\n');
	return diagnostic;
}

export async function subscribeToDocumentChanges(context: vscode.ExtensionContext, licenseDiagnostics: vscode.DiagnosticCollection): Promise<void> {
	if (vscode.window.activeTextEditor) {
		await refreshDiagnostics(vscode.window.activeTextEditor.document, licenseDiagnostics);
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