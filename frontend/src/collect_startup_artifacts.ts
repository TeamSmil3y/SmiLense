import * as fs from 'fs';
import * as yaml from 'js-yaml';
import { Uri, workspace } from 'vscode';

const LICENSE_MANIFEST_FILE = "license-manifest.yaml";
const LICENSE_FILE = "LICENSE";
const REQUIREMENTS_FILE = "requirements.txt";
const CHECK_PACKAGE = "checkPackage";

interface Manifest {
    license: string;
}

export async function findFileInWorkspace(pattern: string): Promise<Uri | undefined> {
    const files = await workspace.findFiles(pattern);
    if (files.length > 0) {
        return files[0];
    }
    return undefined;
}

export async function collectArtifacts(checkPackage: string): Promise<any> {
    // const artifacts = { artifacts: {} };

    // Read license manifest file
    const manifestFileUri = await findFileInWorkspace(LICENSE_MANIFEST_FILE);

    if (!manifestFileUri) {
        console.error(`${LICENSE_MANIFEST_FILE} file not found.`);
        return null;
    }

    // // Read license file
    // const licenseFileUri = await findFileInWorkspace(LICENSE_FILE);

    // if (!licenseFileUri) {
    //     console.error(`${LICENSE_FILE} file not found.`);
    //     return artifacts;
    // }

    // // Read requirements file
    // const requirementsFileUri = await findFileInWorkspace(REQUIREMENTS_FILE);

    // if (!requirementsFileUri) {
    //     console.error(`${REQUIREMENTS_FILE} file not found.`);
    //     return artifacts;
    // }

    try {
        // Read license manifest file
        const manifestFilePath = manifestFileUri.fsPath;
        const manifestFileContent = fs.readFileSync(manifestFilePath, 'utf8');
        // const manifest: Manifest = yaml.load(manifestFileContent) as Manifest;

        // // Read license file
        // const licenseFilePath = licenseFileUri.fsPath;
        // const licenseFileContent = fs.readFileSync(licenseFilePath, 'utf8');

        // // Read requirements file
        // const requirementsFilePath = requirementsFileUri.fsPath;
        // const requirementsFileContent = fs.readFileSync(requirementsFilePath, 'utf8');

        // Encode contents to base64
        const manifestBase64Content = Buffer.from(manifestFileContent).toString('base64');
        // const licenseBase64Content = Buffer.from(licenseFileContent).toString('base64');
        // const requirementsBase64Content = Buffer.from(requirementsFileContent).toString('base64');
        // const checkPackageBase64Content = Buffer.from(checkPackage).toString('base64');

        // Create artifacts object
        const result: any = {
            [LICENSE_MANIFEST_FILE]: manifestBase64Content,
            checkPackageName: checkPackage
            // [LICENSE_FILE]: licenseBase64Content,
        };

        return result;

    } catch (error) {
        console.error('Error reading file:', error);
        return { artifacts: {} };
    }
}
