import axios from 'axios';
import { collectArtifacts } from './collect_startup_artifacts';

const API_ENDPOINT = "https://9527-185-63-131-242.ngrok-free.app"

// 0 : compatible (no-colour)
// 1 : almost compatible (blue)
// 2 : might be compatible (yellow)
// 3 : incompatible (red)
// 4 : not found (orange)

export async function checkPackageValidity(checkPackage: string) {

    const artifacts = await collectArtifacts(checkPackage);

    try {

        return getDemoData(checkPackage)

        const response = await axios.post(API_ENDPOINT, artifacts);

        if (response.status === 200) {
            const responseData = response.data;
            console.log(responseData);
        } else {
            console.error('Failed to check package validity. Status:', response.status);
        }
    } catch (error) {
        console.error('Error occurred while checking package validity:', error);
    }
}

function getDemoData(postdata: any) {
    if (postdata.checkPackageName === "correctPackage") {
        return "0"
    } else {
        return {
            "1": [["package1", "1.2.3"], ["package2", "4.5.6"]],
            "2": [["package2", "4.5.6"], ["package1", "4.5.6"], ["package1", "4.5.6"]],
            "3": [["package2", "4.5.6"], ["package1", "4.5.6"], ["package1", "4.5.6"]],
            "4": [["package2", "4.5.6"], ["package1", "4.5.6"], ["package1", "4.5.6"]]
        };
    }
}
