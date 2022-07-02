async function LogoutUser() {

    return fetch('http://localhost:8000/auth/token/logout', {
        method: 'POST',
        headers: {
            'Authorization': 'Token ' + localStorage['auth_token']
        },

    }).then(
        localStorage.removeItem('auth_token'))

}

const Logout = () => {
    LogoutUser()

    window.location.href = '/'
    return (
        <div />
    )
}

export default Logout
