const app = Vue.createApp({
    data() {
        return {
            email: ""
        }
    },
    methods: {
        notify(arg) {
            url = `http://localhost:5100/${arg}`
            // Different json data passed for each notification type
            axios.post(url, {"email": this.email}, { withCredentials: true })
            .then(response =>{
                console.log(response.data)
            })
            .catch(
                error =>{
                    console.log(error.message)
                }
            )
        }
    }
}).mount('#app')