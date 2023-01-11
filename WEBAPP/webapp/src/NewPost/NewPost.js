import React, { useState } from "react";
import { Button } from "@mui/material";
import './NewPost.css'

const BASE_URL = 'http://localhost:8000/'

function NewPost({authToken, authTokenType}) {
    
    const[image, setImage] = useState(null)
    const[caption, setCaption] = useState('')

    const handleImageUpload = (e) => {
        if (e.target.files[0]) {
            setImage(e.target.files[0])
        }
    }

    const handleCreate = (e) => {
        e?.preventDefault()

        const formData = new FormData();
        formData.append('image', image)

        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken
            }),
            body: formData
        }

        const query_params = new URLSearchParams({
            'caption': caption 
        })

        fetch(BASE_URL + 'posts?' + query_params, requestOptions)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw response
            })
            .then(data => {
                window.location.reload()
                window.scrollTo(0, 0)
            })
            .catch(error => {
                console.log(error);
            })
            .finally(() => {
                setCaption('')
                setImage(null)
                document.getElementById('fileInput').value = null
            })
    }

    return (
        <div className="newpost">
            <input type="text" placeholder="Caption" value={caption} 
                   onChange={(event) => setCaption(event.target.value)} />
            <input type="file" id="fileInput" onChange={handleImageUpload} />
            <Button className="create_button" onClick={handleCreate}>Create</Button>
        </div>
    )

}

export default NewPost;
