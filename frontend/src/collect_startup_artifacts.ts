import * as fs from 'fs';
import * as yaml from 'js-yaml';
import { Uri, workspace } from 'vscode';

const LICENSE_MANIFEST_FILE = "license-manifest.yaml";
const LICENSE_FILE = "LICENSE";
const REQUIREMENTS_FILE = "requirements.txt";
const CHECK_PACKAGE = "checkPackage";

// interface Manifest {
//     license: string;
// }

export async function findFileInWorkspace(pattern: string): Promise<Uri | undefined> {
    const files = await workspace.findFiles(pattern);
    if (files.length > 0) {
        return files[0];
    }
    return undefined;
}

export async function collectArtifacts(checkPackage: string): Promise<any> {
    let artifacts: any = {};
    artifacts.checkPackageName = checkPackage

    // Read license manifest file
    const manifestFileUri = await findFileInWorkspace(LICENSE_MANIFEST_FILE);

    if (!manifestFileUri) {
        console.error(`${LICENSE_MANIFEST_FILE} file not found.`);
    } else {
        const manifestFilePath = manifestFileUri.fsPath;
        const manifestFileContent = fs.readFileSync(manifestFilePath, 'utf8');
        const manifestBase64Content = Buffer.from(manifestFileContent).toString('base64');
        artifacts[LICENSE_MANIFEST_FILE] = manifestBase64Content

    }
    
    return artifacts;

}
