import { ccAPI } from "./connections";

export const getKeywords = async() => {
    // Gets the stored keywords from the API
    try {
        const response = await ccAPI.get("keyword/")

        if (response.status === 200) return await response.data;
        alert(response.data);
        console.log(`getKeywords Error: ${response.data}`)
        return null
    }
    catch (error) {

        if(error.response.status === 401) {
            alert(`You need to login first!`)
            return null
        }

        if(error.response.status === 400){
            console.log(`createKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            alert(`Invalid data: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            return null
        }
        console.log(`createKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}

export const createKeyword = async(this_keyword) => {
    // Creates a new keyword in the API
    try {
    const response = await ccAPI.post("keyword/create/", this_keyword)

        if(response.status === 201) {

            console.log(`createKeyword Response: ${response}`)
            return await response.data
        }
        alert(response.data)
        console.log(`createKeyword Error: ${response.data} - ${response}`)

    }
    catch (error){
        if(error.response.status === 401) {
            alert(`You need to login first!`)
            return null
        }
        if(error.response.status === 400){
            console.log(`createKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            alert(`Invalid data: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            return null
        }
        console.log(`createKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}

export const updateKeyword = async(this_keyword) => {
    // Updates an existing keyword with the API
    try {

        const response = await ccAPI.put(`keyword/${this_keyword.id}/`, this_keyword)

        if(response.status === 201) {
            console.log(`updateKeyword Response: ${response.data}`)
            return await response.data
        }
        alert(response.data)
        console.log(`updateKeyword Error ${response.data} ${response}`)
        return response
    }
    catch (error){
        if(error.response.status === 401) {
            alert(`You need to login first!`)
            return null
        }
        if(error.response.status === 400){
            console.log(`updateKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            alert(`Invalid data: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
            return null
        }
        console.log(`updateKeyword error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        alert(`Error: ${Object.keys(error.response.data).map((err) => `${err} - ${error.response.data[err]}`)}`)
        return null
    }
}