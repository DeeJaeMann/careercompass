import { useState } from 'react';
import './App.css';
import { Outlet } from 'react-router-dom';
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import { Tooltip, initTWE } from "tw-elements";

const App = () => {

  const [ user, setUser] = useState("")

  return (
    <>
      <Navbar user = {user} setUser = {setUser} />
      <Outlet context = {{user, setUser}} />
      <Footer />
    </>
  )
}

export default App
