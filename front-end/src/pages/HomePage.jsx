import { useState } from "react";

const HomePage = () => {

    return (
        <>
            <div>
                <h2>Welcome to Career Compass!</h2>
                <p>A great description will go here!</p>
                <div>
                    <p>
                        <a href="https://services.onetcenter.org/" title="This site incorporates information from O*NET Web Services. Click to learn more."><img src="https://www.onetcenter.org/image/link/onet-in-it.svg" alt="O*NET in-it" /></a>
                    </p>
                    <p>This site incorporates information from <a href="https://services.onetcenter.org/">O*NET Web Services</a> by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). O*NET&reg; is a trademark of USDOL/ETA.</p>
                </div>
            </div>
        </>
    )
}


export default HomePage;