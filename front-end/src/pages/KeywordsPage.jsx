import { useState, useEffect } from "react";
import { useOutletContext } from "react-router-dom";
import { MDBBtn } from 'mdb-react-ui-kit';
import { 
    getKeywords,
    createKeyword,
    updateKeyword,
} from "../lib/keywords";

const KeywordsPage = () => {

    const [ keywords, setKeywords ] = useState([])
    const [ keywordUpdate, setKeywordUpdate] = useState(false)
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
            setKeywordUpdate(false)
            // console.log(`Keywords: ${response}`)
        }).catch(error => {
            console.log(`Keywords useEffect Error ${error} - ${response}`)
        })
    }, [keywordUpdate])

    const handleUpdate = (event, this_keyword) => {
        event.preventDefault()

        if(this_keyword.name) {
            updateKeyword(this_keyword).then(response => {
                if(response) {
                    console.log(`Updated: ${response.id} ${response.name}`)
                    alert(`Updated: ${response.name}`)
                    setKeywordUpdate(true)
                }
            })
        }
        else {
            alert(`You must enter a value!`)
        }

    }

    const handleCreate = async(event, this_keyword) => {
        event.preventDefault()

        if(this_keyword.name) {
            createKeyword(this_keyword).then(response => {
                if(response){
                    console.log(`Created: ${response.id} ${response.name}`)
                    alert(`Created: ${response.name}`)
                    setKeywordUpdate(true)
                }
            })
        }
        else {
            alert(`You must enter a value!`)
        }
    }

    const displayCreateForm = (this_keyword, index) => {
        return (
            <>
                <form key={index} onSubmit={(event) => handleCreate(event, this_keyword)}>
                    <span>{this_keyword.category}</span>
                    <input className="ml-2 mb-1 rounded-md border-slate-900 border" type="text" placeholder={`Enter ${this_keyword.category}`} defaultValue={this_keyword.name} onChange={(event) => this_keyword.name = event.target.value} />
                    <MDBBtn className="bg-blue-900 ml-2 mb-1 h-7 p-2 pt-1 pb-1">Submit</MDBBtn>
                </form>
            </>
        )
    }

    const displayCreateFields = () => {
        let fieldOutput = [];

        for( let index = 0; index < 6; index++) {
            const this_keyword = {}
            index < 3 ? (
                this_keyword.category = "hobby"
            ) : (
                this_keyword.category = "interest"
            )
            if(keywords[index]) {
                this_keyword.name = keywords[index].name
            }
            fieldOutput.push(displayCreateForm(this_keyword, index))
        }
        return fieldOutput
    }

    return (
        <>
            <h2>Keywords Page</h2>
            <p>{user && `${user}`}</p>
                {keywords.length < 6 ? (
                    <>
                        <p>No Keywords</p>
                        {displayCreateFields()}
                    </>
                ) : (
                <>
                {keywords.map((this_keyword, index) => 
                    <form key={index} onSubmit={(event) => handleUpdate(event, this_keyword)}> 
                        <span>{this_keyword.category}</span>
                        <input className="ml-2 mb-1 rounded-md border-slate-900 border" type="text" name={`${this_keyword.category}${this_keyword.id}`} placeholder={`Enter ${this_keyword.category}`} defaultValue={this_keyword.name} onChange={(event) => this_keyword.name = event.target.value} />
                        <MDBBtn className="bg-blue-900 ml-2 mb-1 h-7 p-2 pt-1 pb-1">Submit</MDBBtn>
                    </form>
                )}
                </>
            )}
        </>
    )
}

export default KeywordsPage