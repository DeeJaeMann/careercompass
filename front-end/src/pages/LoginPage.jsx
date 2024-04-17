import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { MDBBtn } from 'mdb-react-ui-kit'
import { userLogin } from "../lib/connections";

const LoginPage = () => {
    const [emailInput, setEmailInput] = useState("");
    const [passwordInput, setPasswordInput] = useState("");
    const { setUser } = useOutletContext();

    const handleLogin = async(event) => {
        event.preventDefault();

        setUser(await userLogin(emailInput, passwordInput));
        setEmailInput("")
        setPasswordInput("")
    }

    return (
        <>
            <h2>Login Page</h2>
            <form onSubmit={handleLogin}>
                <span>E-Mail Address: </span>
                <input className="rounded-md border-slate-900 border" type="email" name="email" placeholder="Enter Email" value={emailInput} onChange={(event) => setEmailInput(event.target.value)} />
                <span className="ml-2">Password: </span>
                <input className="rounded-md border-slate-900 border" type="password" name="password" placeholder="Password" value={passwordInput} onChange={(event) => setPasswordInput(event.target.value)} />
                <MDBBtn className="bg-blue-900 ml-2">Submit</MDBBtn>
            </form>
        </>
    )
}

export default LoginPage;