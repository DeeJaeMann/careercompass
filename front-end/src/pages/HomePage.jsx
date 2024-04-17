import { useState } from "react";
import { useOutletContext } from "react-router-dom";

const HomePage = () => {

    const { user } = useOutletContext();

    return (
        <>
            <div>
                <h1>Career Compass</h1>
                <h2>{user && `${user}`}</h2>
                <p>Welcome to Career Compass!  Let us help you harness the power of AI to discover your next career journey!</p>

            </div>
        </>
    )
}


export default HomePage;