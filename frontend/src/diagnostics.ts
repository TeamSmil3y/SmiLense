/*---------------------------------------------------------
 * Copyright (C) Microsoft Corporation. All rights reserved.
 *--------------------------------------------------------*/

/** To demonstrate code actions associated with Diagnostics problems, this file provides a mock diagnostics entries. */

import * as vscode from 'vscode';

/** Code that is used to associate diagnostic entries with code actions. */
// export const EMOJI_MENTION = 'emoji_mention';
export const PACKAGE_LICENSE_MENTION = 'package_license_mention';

/** String to detect in the text document. */
// const EMOJI = 'emoji';

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
		// if (lineOfText.text.includes(EMOJI)) {
			// 	diagnostics.push(createDiagnostic(doc, lineOfText, lineIndex));
			// }
			
		if (lineOfText.text.includes(IMPORT_KEYWORD) && lineOfText.text.trim() !== IMPORT_KEYWORD) {
			diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex));
		}

		// if (lineOfText.text.includes(IMPORT_KEYWORD)) {
		// 	diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex));
		// }
	}

	licenseDiagnostics.set(doc.uri, diagnostics);
}

// export function refreshDiagnostics(doc: vscode.TextDocument, licenseDiagnostics: vscode.DiagnosticCollection): void {
// 	const diagnostics: vscode.Diagnostic[] = [];

// 	for (let lineIndex = 0; lineIndex < doc.lineCount; lineIndex++) {
// 		const lineOfText = doc.lineAt(lineIndex);
// 		if (lineOfText.text.includes(EMOJI)) {
// 			diagnostics.push(createDiagnostic(doc, lineOfText, lineIndex));
// 		}

// 		if (lineOfText.text.includes(IMPORT_KEYWORD)) {
// 			diagnostics.push(createPackageLicenseDiagnostic(doc, lineOfText, lineIndex));
// 		}
// 	}

// 	licenseDiagnostics.set(doc.uri, diagnostics);
// }

// function createDiagnostic(doc: vscode.TextDocument, lineOfText: vscode.TextLine, lineIndex: number): vscode.Diagnostic {
// 	// find where in the line of that the 'emoji' is mentioned
// 	const index = lineOfText.text.indexOf(EMOJI);

// 	// create range that represents, where in the document the word is
// 	const range = new vscode.Range(lineIndex, index, lineIndex, index + EMOJI.length);

// 	const diagnostic = new vscode.Diagnostic(range, "When you say 'emoji', do you want to find out more?",
// 		vscode.DiagnosticSeverity.Information);
// 	diagnostic.code = EMOJI_MENTION;
// 	return diagnostic;
// }

function createPackageLicenseDiagnostic(doc: vscode.TextDocument, lineOfText: vscode.TextLine, lineIndex: number): vscode.Diagnostic {

	let packageName = lineOfText.text.split(" ").pop() || "";

	console.log({packageName})

	// find where in the line of that the packageName is mentioned
	const index = lineOfText.text.indexOf(packageName);

	// create range that represents, where in the document the word is
	const range = new vscode.Range(lineIndex, index, lineIndex, index + packageName.length);

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