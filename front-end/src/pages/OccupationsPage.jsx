import { useState, useEffect } from "react";
import { useOutletContext } from "react-router-dom";
import { getOccupations } from "../lib/occupations";

const OccupationsPage = () => {
    const { user } = useOutletContext();
    const [ occupations, setOccupations ] = useState([])

    useEffect(() => {
        getOccupations().then(response => {
            if(response) {
                response = response.sort((a, b) => {
                    const nameA = a.name.toUpperCase();
                    const nameB = b.name.toUpperCase();
                    return nameA.localeCompare(nameB);
                });

                setOccupations(response)
            }
        }).catch(error => {
            console.log(`Occupations useEffect Error ${error}`)
        })
    }, [])

    return (
        <>
            <h2>Occupations Page</h2>
            <ol>
                {occupations.map((job, index) =>
                <li key={index}>{job.name}</li>
                )}
            </ol>
        </>
    )
}

export default OccupationsPage;