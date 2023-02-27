export const getAuthCookie = () => {
    const token = localStorage.getItem('hash');

    return {
        headers: {"Authorization": token}
    }
}

export function isAuth(User, route) {

    return (!User.resultCode && Object.keys(User).length !== 0) && (route.roles.includes(0) || route.roles.includes(User.role_id))
}

export function formHandle(setState, {target: {value, type, name, files, checked}}) {

    let setType = value

    if (type === 'file') {
        setType = files
    } else if (type === 'checkbox') {
        setType = checked
    }
    setState(state => {
        return {
            ...state,
            [name]: setType
        }
    })
}