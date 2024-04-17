import { useState, useEffect } from 'react';
import './App.css';
import { 
  Outlet,
  useLocation,
  useNavigate,
 } from 'react-router-dom';
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import { Tooltip, initTWE } from "tw-elements";

const App = () => {

  const [ user, setUser] = useState("")
  const location = useLocation();
  const navigate = useNavigate();

  // Redirect users to the homepage if they are not logged in
  useEffect(() => {
    const nullUserUrls = ["/login/", "/signup/"];
    let isAllowed = nullUserUrls.includes(location.pathname);

    if (user && isAllowed) {
      navigate("/");
    } else if (!user && !isAllowed){
      navigate("/");
    }
  }, [location.pathname, user])

  return (
    <>
      <Navbar user = {user} setUser = {setUser} />
      <Outlet context = {{user, setUser}} />
      <Footer />
    </>
  )
}

export default App
