import { ccAPI } from "./connections";
import { getKeywords } from "./keywords";

export const getOccupations = async() => {
    // Requests list of occupations from API
    try {
        // Check for 6 keywords first
        const keyword_response = await getKeywords();

        if(keyword_response.length === 6) {
            const response = await ccAPI.get("occupation/");
            return await response.data;
        }
        else {
            console.log(`Not enough keywords: counted ${keyword_response.length}`);
            alert(`You must have 3 hobbies and 3 interests!`);
            return null;
        }
    }
    catch (error) {
        console.log(`getOccupation catch ${error}`);

        if(error.response.status === 401) {
            alert(`You need to login first!`);
            return null;
        }

        console.log(`getOccupations error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`);
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`);
        return null;
    }
}

export const getDetails = async(id) => {
    try {
        const response = await ccAPI.get(`details/${id}/`);
        return response.data
    }
    catch (error) {
        if(error.response.status === 404) {
            console.log(`getDetails catch ${error} ID: ${id}`)
            alert(`Error ${error}`)
            return null
        }
        console.log(`getDetails error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}

export const getKnowledge = async(id) => {
    try {
        const response = await ccAPI.get(`details/knowledge/${id}/`)
        return response.data
    }
    catch (error) {
        if(error.response.status === 404) {
            console.log(`getKnowledge catch ${error} ID: ${id}`)
            alert(`Error ${error}`)
            return null
        }
        console.log(`getKnowledge error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}