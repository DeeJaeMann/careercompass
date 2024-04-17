import { ccAPI } from "./connections";
import { getKeywords } from "./keywords";

export const getOccupations = async() => {
    // Requests list of occupations from API
    try {
        // Check for 6 keywords first
        const keyword_response = await getKeywords();

        // if (keyword_response.status === 200 || keyword_response.status === 201) {
        console.log(`getOccupation loaded keywords`)
        if(keyword_response.length === 6) {
            console.log(`getOccupation has enough keywords`)
            const response = await ccAPI.get("occupation/")
            return await response.data;
        }
        else {
            console.log(`Not enough keywords: counted ${keyword_response.length}`)
            alert(`You must have 3 hobbies and 3 interests!`)
            return null
        }
        // }
        console.log(`getOccupations keyword ${keyword_response}`)
        console.log(`getOccupations Error: ${keyword_response.data}`)
        console.log(`getOccupations status ${await keyword_response.status}`)
        alert(`getOccupations Error: ${keyword_response.data}`);
        return null;
    }
    catch (error) {
        console.log(`getOccupation catch ${error}`)

        if(error.response.status === 401) {
            alert(`You need to login first!`)
            return null
        }

        console.log(`getOccupations error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}