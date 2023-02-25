import React from 'react';

const User = ({user, setTarget, roles}) => {
    console.log(roles)
    return (
        <div className="d-flex text-muted pt-3" id={user.id} style={{cursor:'pointer'}} data-bs-toggle="modal"
             data-bs-target="#staticBackdrop" onClick={() => {setTarget({last_name:user.last_name, first_name:user.first_name,id:user.id,role_id: user.role_id})}}>
            <img src={user.photo_code} width="64" height="64" className="m-1" style={{borderRadius: '50%', objectFit: 'cover'}}/>
            <div className="pb-3 mb-0 small lh-sm border-bottom w-100 my-auto ms-2">
                <div className="d-flex justify-content-between">
                    <strong className="text-gray-dark h6">@{user.username}</strong>
                </div>
                <span className="d-block">{user.first_name} {user.last_name} ({roles.filter(role => role.id === user.role_id)[0]?.name})</span>
            </div>
        </div>
    )
}

export default User;