export const getAuthCookie = () => {
    const token = localStorage.getItem('hash');

    return {
        headers: {"Authorization": token}
    }
}

export function isAuth(User, route) {

    return (!User.resultCode && Object.keys(User).length !== 0) && (route.roles.includes(0) || route.roles.includes(User.role_id))
}