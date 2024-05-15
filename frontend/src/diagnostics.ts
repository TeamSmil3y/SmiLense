import * as vscode from 'vscode';
import { checkPackageValidity } from './isPackageValid';

/** Code that is used to associate diagnostic entries with code actions. */
export const PACKAGE_LICENSE_MENTION = 'package_license_mention';
export const LICENSE_NOT_FOUND = '1';
export const LICENSE_INCOMPATIBLE = '0';
// export const LICENSE_COMPATIBLE = '1';

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
			// checkPackageValidity(checkPackage).then(encodedData => {
			// 	console.log({ checkPackageValidity: encodedData });
			// });
			let checkPackageOutput = await checkPackageValidity(checkPackage)
			console.log({ checkPackageOutput })
			let isValidPackage = false;

			if (!isValidPackage) {
				diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex));
			}

		}
	}

	licenseDiagnostics.set(doc.uri, diagnostics);
}

function createPackageLicenseDiagnostic(doc: vscode.TextDocument, lineOfText: vscode.TextLine, lineIndex: number): vscode.Diagnostic {

	let checkPackage = lineOfText.text.split(" ").pop() || "";

	// console.log({ checkPackage })

	// checkPackageValidity(checkPackage).then(encodedData => {
	// 	console.log({ checkPackageValidity: encodedData });
	// });


	// find where in the line of that the checkPackage is mentioned
	const index = lineOfText.text.indexOf(checkPackage);

	// create range that represents, where in the document the word is
	const range = new vscode.Range(lineIndex, index, lineIndex, index + checkPackage.length);

	const diagnosticSeverity = LICENSE_NOT_FOUND;

	if (diagnosticSeverity === LICENSE_NOT_FOUND) {
		const diagnostic = new vscode.Diagnostic(range, "This package's license might be incompatible with your project",
			vscode.DiagnosticSeverity.Error);
		diagnostic.code = LICENSE_NOT_FOUND;
		diagnostic.message = "6 incompatible licenses\n4 dependencies with no licenses";
		return diagnostic;
	} else {
		const diagnostic = new vscode.Diagnostic(range, "This package's license might be incompatible with your project",
			vscode.DiagnosticSeverity.Warning);
		diagnostic.code = LICENSE_INCOMPATIBLE;
		diagnostic.message = "6 incompatible licenses\n4 dependencies with no licenses";
		return diagnostic;
	}
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