import { useState } from "react";
import { Link, useNavigate} from "react-router-dom";
import { 
    MDBContainer,
    MDBNavbar,
    MDBNavbarBrand,
    MDBNavbarLink,
    MDBBtn,
} from 'mdb-react-ui-kit';
import ccLogo from "../assets/logo2.png"

const Navbar = () => {

    return (
        <>
            <MDBNavbar expand='lg' className='rounded-lg bg-slate-300 mb-5'>
                <MDBContainer fluid>
                    <Link to="#">
                        <MDBNavbarBrand>
                            <img
                                src={ccLogo}
                                alt='Career Compass Logo'
                                loading='lazy'
                                className='h-20 rounded-full border dark:border-neutral-700 dark:bg-neutral-800'
                                />
                            Career Compass
                        </MDBNavbarBrand>
                    </Link>
                </MDBContainer>
                <MDBContainer className="justify-evenly" fluid>
                    <MDBNavbarLink>Interests and Hobbies</MDBNavbarLink>
                    <MDBNavbarLink>Occupations</MDBNavbarLink>
                </MDBContainer>
                <MDBContainer className="d-flex justify-end w-auto mr-5" fluid>
                    <MDBBtn className="bg-blue-700 mr-3">Login</MDBBtn>
                    <MDBBtn className="bg-blue-700">SignUp</MDBBtn>
                </MDBContainer>
            </MDBNavbar>
        </>
    )
}

export default Navbar