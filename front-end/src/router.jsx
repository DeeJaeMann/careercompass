import { createBrowserRouter } from "react-router-dom";
import App from "./App.jsx"
import HomePage from "./pages/HomePage.jsx";
import SignupPage from "./pages/SignupPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                index: true,
                element: <HomePage />,
            },
            {
                path: "signup/",
                element: <SignupPage />,
            },
            {
                path: "login/",
                element: <LoginPage />,
            },
        ],
    },
]);

export default router;
