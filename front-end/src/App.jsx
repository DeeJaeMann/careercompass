import { useState } from 'react';
import './App.css';
import { Outlet } from 'react-router-dom';
import Navbar from "./components/Navbar";
import { Tooltip, initTWE } from "tw-elements";

const App = () => {

  return (
    <>
      <Navbar />
      <Outlet />
    </>
  )
}

export default App
