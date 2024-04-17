import { createBrowserRouter } from "react-router-dom";
import App from "./App.jsx"
import HomePage from "./pages/HomePage.jsx";
import SignupPage from "./pages/SignupPage.jsx";

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
        ],
    },
]);

export default router;
