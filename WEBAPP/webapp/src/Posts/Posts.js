import React, { useEffect, useState } from "react";
import { Avatar, Button, Input } from "@mui/material" 
import './Posts.css'

const BASE_URL = 'http://localhost:8000/'

function Posts({post, authToken, authTokenType}) {

    const [imageUrl, setImageUrl] = useState('')
    const [comments, setComments] = useState([])
    const [newComment, setNewComment] = useState('')

    useEffect(() => {
        setImageUrl(BASE_URL + post.image_path)
    }, [])

    useEffect(() => {
        setComments(post.comments)
    }, [])

    const handleDelete = (event) => {
        event?.preventDefault();

        const requestOptions = {
            method: 'DELETE',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken
            })
        }

        fetch(BASE_URL + 'posts/' + post.id, requestOptions)
            .then(response => {
                if (response.ok) {
                    window.location.reload()
                }
                throw response
            })
            .catch(error => {
                console.log(error);
            })
    }

    const createNewComment = (event) => {
        event?.preventDefault();

        const req_body_json = JSON.stringify({
            post_id: post.id,
            comment_text: newComment
        })

        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken,
                'Content-Type': 'application/json'
            }),
            body: req_body_json
        }

        fetch(BASE_URL + 'comments/', requestOptions)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw response
            })
            .then(data => {
                refreshComments()
            })
            .catch(error => {
                console.log(error);
            })
            .finally(() => {
                setNewComment('')
            })
    }

    const refreshComments = () => {
        const requestOptions = {
            method: 'GET'
        }

        fetch(BASE_URL + 'comments/post/' + post.id)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
            })
            .then(data => {
                setComments(data)
            })
            .catch(error => {
                console.log(error);
            })
    }

    return (
        <div className="post">
            <div className="post_header">
                <Avatar alt="DefaultAvatar" src=""></Avatar>
                <div className="post_header_info">
                    <h3>{post.author.username}</h3>
                    <Button className="post_delete" onClick={handleDelete}>Delete</Button>
                </div>
            </div>

            <img className="post_image" src={imageUrl}></img>
            
            <h4 className="post_caption">{post.caption}</h4>
            <div className="post_comments">
                {
                    comments.map((comment) => (
                        <p>
                            <strong>{comment.comment_author.username}:</strong> {comment.comment_text}
                        </p>
                    ))
                }
            </div>

            {authToken && (
                <form className="post_comment_box">
                    <input placeholder='Add a comment' type='text' value={newComment}
                        className='post_comment_input' onChange={(e) => setNewComment(e.target.value)} />
                    <button className="post_new_comment_button" type="submit" disabled={!newComment}
                        onClick={createNewComment}>Post</button>
                </form>
            )}
        </div>
    )
}

export default Posts