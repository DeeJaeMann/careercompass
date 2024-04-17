import { useState, useEffect } from "react";
import { useOutletContext } from "react-router-dom";
import { MDBBtn } from 'mdb-react-ui-kit';
import { getKeywords } from "../lib/keywords";

const KeywordsPage = () => {

    const [ keywords, setKeywords ] = useState([])
    const { user } = useOutletContext();

    useEffect(() => {
        getKeywords().then(response=> {
            // Sort the response by category
            response = response.sort((a, b) => {
                const catA = a.category.toUpperCase();
                const catB = b.category.toUpperCase();
                // localeCompare returns a number indicating whether the string (catB) comes before, after or is the same as the given string (catA) not recommended for large numbers of strings
                return catA.localeCompare(catB);
            });
            setKeywords(response)
            console.log(`Keywords: ${response}`)
        }).catch(error => {
            console.log(`Keywords useEffect Error ${error} - ${resposne}`)
        })
    }, [])

    const handleSubmit = (event, keyword) => {
        event.preventDefault()

        alert(`Submit! ID: ${keyword.id} ${keyword.name}`)
    }

    return (
        <>
            <h2>Keywords Page</h2>
            <p>{user && `${user}`}</p>
                {!keywords.length ? (
                    <>
                        <p>No Keywords</p>
                    </>
                ) : (
                <>
                {keywords.map((keyword, index) => 
                    <form key={index} onSubmit={(event) => handleSubmit(event, keyword)}> 
                        <span>{keyword.category}</span>
                        <input className="ml-2 mb-1 rounded-md border-slate-900 border" type="text" name={`${keyword.category}${keyword.id}`} placeholder={`Enter ${keyword.category}`} defaultValue={keyword.name} onChange={(event) => keyword.name = event.target.value} />
                        <MDBBtn className="bg-blue-900 ml-2 mb-1 h-7 p-2 pt-1 pb-1">Submit</MDBBtn>
                    </form>
                )}
                </>
            )}
        </>
    )
}

export default KeywordsPage