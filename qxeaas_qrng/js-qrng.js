
require('dotenv').config();
const axios = require('axios')
let token= process.env.ACCESS_TOKEN
let size= "required-size-for-your-application"

let url = "https://qum-backend.azurewebsites.net/t32/quentom-entropy?size=${size}"

axios({
    method: 'get',
    url,
    headers: {
        Authorization: ""
    }
}).then(function (response) {
    console.log(response.data)
}).catch(function (error) {
    console.log(error)
})     