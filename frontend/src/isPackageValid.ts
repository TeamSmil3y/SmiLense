import axios from 'axios';
import { collectArtifacts } from './collect_startup_artifacts';

const API_ENDPOINT = "https://9527-185-63-131-242.ngrok-free.app"

export async function checkPackageValidity(checkPackage: string) {

    const { artifacts } = await collectArtifacts(checkPackage);

    try {
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
