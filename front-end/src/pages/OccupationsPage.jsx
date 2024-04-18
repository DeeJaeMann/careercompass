import { useState, useEffect } from "react";
import { useOutletContext, Link } from "react-router-dom";
import { getOccupations, getDetails } from "../lib/occupations";

const OccupationsPage = () => {
    const { occupations, setOccupations } = useOutletContext();

    useEffect(() => {
        getOccupations().then(response => {
            if(response) {
                response = response.sort((a, b) => {
                    const nameA = a.name.toUpperCase();
                    const nameB = b.name.toUpperCase();
                    return nameA.localeCompare(nameB);
                });
                //TODO: Figure this out: none of these work
                // for(let job of response){
                //     getDetails(job.id).then(thisResponse => setThisDetail([...thisDetail, thisResponse]))
                //     console.log(`Job: ${job.id}`)
                //     console.log(`Detail Response: ${thisDetail}`)
                    // job.details = thisDetail.description
                // }
                // response = response.map((job) => {
                //     getDetails(job.id).then(detail_response => {
                //         job['details'] = detail_response.description
                //         job['alt_names'] = detail_response.alt_names
                //         job['tasks'] = detail_response.tasks
                //         job['id'] = job.id
                //         job['name'] = job.name
                //     })
                // console.log(`Response object keys: ${Object.keys(response)}`)
                // })
                setOccupations(response)
            }
        }).catch(error => {
            console.log(`Occupations useEffect Error ${error}`)
        })
    }, [])


    return (
        <>
            <h2>Here is what I found for you:</h2>
            <ol>
                {occupations.map((job, index) =>
                <li key={index}><Link to={`/details/${job.id}`}>{job.name}</Link></li>
                )}
            </ol>
        </>
    )
}

export default OccupationsPage;