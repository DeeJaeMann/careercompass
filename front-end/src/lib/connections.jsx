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
            const { user, token } = response.data;
            localStorage.setItem("token", token);
            ccAPI.defaults.headers.common["Authorization"] = `Token ${token}`;
            userLogin(email, password);
            return user
        }
    }
    catch (error) {
        console.log(error)
        alert(`Email: ${error.response.data.email} \nPassword: ${error.response.data.password}`);
        return null;
    }

}

export const userLogin = async (email, password) => {
    const response = await ccAPI.post("user/login/", {
        email: email,
        password: password
    });
    if (response.status === 200) {
        const { user, token } = response.data;
        localStorage.setItem("token", token);
        ccAPI.defaults.headers.common["Authorization"] = `Token ${token}`;
        return user;
    }
    alert(response.data);
    return null;
}