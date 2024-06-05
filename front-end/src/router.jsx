import { createBrowserRouter } from "react-router-dom";
import App from "./App.jsx"
import HomePage from "./pages/HomePage.jsx";
import SignupPage from "./pages/SignupPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import KeywordsPage from "./pages/KeywordsPage.jsx";
import OccupationsPage from "./pages/OccupationsPage.jsx";
import OccupationDetailsPage from "./pages/OccupationDetailsPage.jsx";

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
            {
                path: "keywords/",
                element: <KeywordsPage />,
            },
            {
                path: "occupations/",
                element: <OccupationsPage />,
            },
            {
                path: "details/:id",
                element: <OccupationDetailsPage />,
            },
        ],
    },
]);

export default router;
