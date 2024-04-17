import { useState } from "react";
import { Link, useNavigate} from "react-router-dom";
import { 
    MDBContainer,
    MDBNavbar,
    MDBNavbarBrand,
    MDBNavbarLink,
    MDBBtn,
    MDBBadge,
} from 'mdb-react-ui-kit';
import ccLogo from "../assets/logo2.png"
import { userLogout } from "../lib/connections";

const Navbar = ({user, setUser}) => {

    return (
        <>
            <MDBNavbar expand='lg' className='rounded-lg bg-slate-300 mb-5'>
                <MDBContainer fluid>
                    <MDBNavbarBrand tag={Link} to="/">
                        <img
                            src={ccLogo}
                            alt='Career Compass Logo'
                            loading='lazy'
                            className='h-20 rounded-full border dark:border-neutral-700 dark:bg-neutral-800'
                            />
                        Career Compass
                    </MDBNavbarBrand>
                </MDBContainer>
                <MDBContainer className="d-flex justify-end w-auto mr-5" fluid>
                    {!user ? (
                        <>
                            <Link to="login/">
                                <MDBBtn className="bg-blue-900 mr-3">Login</MDBBtn>
                            </Link>
                            <Link to="signup/">
                                <MDBBtn className="bg-blue-900">SignUp</MDBBtn>
                            </Link>
                        </>
                        ) : (
                        <>
                            <Link to="login/">
                                <MDBBtn className="bg-red-900" onClick={async () => setUser(await userLogout())}>Logout</MDBBtn>
                            </Link>
                        </>
                    )}
                </MDBContainer>
                <MDBContainer className="justify-start mt-3" fluid>
                    {user ? (
                        <>
                            <MDBNavbarLink tag={Link} to="/signup">Interests and Hobbies</MDBNavbarLink>
                            <MDBNavbarLink tag={Link} to="/signup">Occupations</MDBNavbarLink>
                            <MDBBadge color="info" className="ms-2">{user}</MDBBadge>
                        </>
                    ) : (
                        <></>
                    )}
                </MDBContainer>

            </MDBNavbar>
        </>
    )
}

export default Navbar