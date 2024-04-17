import axios from "axios";

export const ccAPI = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1/",
})

export const signupUser = async(email, password) => {
    try {
        const response = await ccAPI.post("user/signup/", {
            email: email,
            password: password
        });

        if (response.status === 201) {
            console.log(`Connections: User ${email} signed up, response: ${response.data}`);
            const { username, token } = response.data;
            localStorage.setItem("token", token);
            ccAPI.defaults.headers.common["Authorization"] = `Token ${token}`;
            userLogin(email, password);
            return username
        }
    }
    catch (error) {
        console.log(error)
        alert(`Email: ${error.response.data.email} \nPassword: ${error.response.data.password}`);
        return null;
    }

}

export const userLogin = async (email, password) => {

    try {
        const response = await ccAPI.post("user/login/", {
            email: email,
            password: password
        });
        if (response.status === 200) {
            const { username, token } = response.data;
            console.log(response.data)
            localStorage.setItem("token", token);
            ccAPI.defaults.headers.common["Authorization"] = `Token ${token}`;
            console.log(`${username} logged in token ${token}`)
            return username;
        }
    }
    catch (error) {
        console.log(error)
        alert(`${error.response.data}`);
        return null;
    }
}

export const userLogout = async () => {
    try {
        const response = await ccAPI.post("user/logout/");

        if (response.status === 204) {
            localStorage.removeItem("token");
            delete ccAPI.defaults.headers.common["Authorization"];
            return null;
        }
        alert("Logout failed!");
    }
    catch (error) {
        console.log(error)
        alert(`${error.response.data}`)
    }
}