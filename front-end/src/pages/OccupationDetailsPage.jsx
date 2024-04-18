import { useState, useEffect } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { 
    getDetails,
    getKnowledge,
    getEducation,
} from "../lib/occupations";

const OccupationDetailsPage = () => {
    const [ thisJob, setThisJob ] = useState({})
    const [ details, setDetails ] = useState({})
    const [ knowledge, setKnowledge ] = useState([])
    const [ education, setEducation ] = useState({})
    const { occupations } = useOutletContext();

    const { id } = useParams();

    useEffect(() => {
        //Populate the occupation details
        getDetails(id).then(response => {
            if(response) setDetails(response);

        }).catch((error) => alert(error))

        // Populate the occupation knowledge
        getKnowledge(id).then(response => {
            if(response) setKnowledge(response)

        }).catch((error) => alert(error))

        // Populate the occupation education
        getEducation(id).then(response => {
            if(response) setEducation(response)
        }).catch((error) => alert(error))

        const job = occupations.filter((job) => job.id === Number(id))[0] 

        setThisJob(job)

    },[])

    return (
        <>
            <h2 className="text-xl mb-2">{thisJob.name} Details</h2>
            <p>{details.description}</p>
            <span className="text-lg">Also Known As:</span>
            <ol>
                <li>{details.onet_name}</li>
                {!details.alt_names ? (
                    <></>
                ) : (
                    details.alt_names.title.map((title, index) => <li key={index}>{title}</li>))}
            </ol>
            <span className="text-lg">Tasks:</span>
            <ol>
                {!details.tasks ? (
                    <></>
                ) : (
                details.tasks.task.map((job, index) => <li key={index}>{job}</li>)
            )}
            </ol>
            <span className="text-lg">Knowledge:</span>
            <ol>
                {!knowledge ? (
                    <></>
                ):(
                    <>
                    {knowledge.map((know, index) => <li key={index}>{know.category}</li>)}
                    </>
                )}
            </ol>
            <span className="text-lg">Education:</span>
            <ol>
                {!education.description ? (
                    <></>
                ) : (
                    <>
                        <p>To be added later</p>
                    </>

                )
            }
            </ol>
        </>
    )

}

export default OccupationDetailsPage