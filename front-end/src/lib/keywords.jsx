import { ccAPI } from "./connections";

export const getKeywords = async() => {
    try {
        const response = await ccAPI.get("keyword/")

        if (response.status === 200) {

        console.log(`Keyword Connection ${await response.status} ${await response.data} ${await response}`)
        console.log(await response.data)

        return await response.data;
        }
        alert(response.data);
        console.log(`Error: ${response.data}`)
        return []
    }
    catch (error) {

        if(response.status === 401) {
            console.log(`User not logged in!`);
            alert(`You need to login first!`)
            return []
        }

        console.log(`Error ${error} ${response.data}`)
        alert(`${error}`)
        return []
    }
}