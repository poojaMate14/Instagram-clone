import './App.css';
import React, { useEffect, useState } from 'react';
import Posts from './Posts/Posts';
import NewPost from './NewPost/NewPost';
import { Button, Modal, Input } from '@mui/material';
import { makeStyles } from '@mui/styles'


const BASE_URL = 'http://localhost:8000/'

function getModalStyle() {
	const top = 50;
	const left = 50;

	return {
		top: `${top}%`,
		left: `${left}%`,
		transform: `translate(-${top}%, -${left}%)`,
	};
}

const useStyles = makeStyles(() => ({
	paper: {
		backgroundColor: 'white',
		position: 'absolute',
		width: 400,
		border: '2px solid #000',
		paddingLeft: '20px',
		paddingRight: '20px'
	}
}))

function App() {

  const classes = useStyles();

  const [posts, setPosts] = useState([]);
  const [openSignIn, setOpenSignIn] = useState(false);
  const [openSignUp, setOpenSignUp] = useState(false);
  const [modalStyle, setModalStyle] = useState(getModalStyle);
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [authToken, setAuthToken] = useState(null);
  const [authTokenType, setAuthTokenType] = useState(null);
  const [userId, setUserId] = useState('');
  const [email, setEmail] = useState('');

  // Maintain authentication after webpage reload
  useEffect(() => {
	setAuthToken(window.localStorage.getItem('authToken'))
	setAuthTokenType(window.localStorage.getItem('authTokenType'))
	setUserId(window.localStorage.getItem('userId'))
	setUserName(window.localStorage.getItem('username'))
  }, [])

  // Get all posts
  useEffect(() => {
	fetch(BASE_URL + 'posts/')
		.then(response => {
			const response_json = response.json()
			console.log(response_json);
			if (response.ok) {
				return response_json
			}
			throw response
		})
		.then(data => {
			const sorted_data = data.sort((a, b) => {
				const t_a = a.timestamp.split(/[-T:]/)
				const t_b = b.timestamp.split(/[-T:]/)
				const date_a = new Date(Date.UTC(t_a[0], t_a[1]-1, t_a[2], t_a[3], t_a[4], t_a[5]))	
				const date_b = new Date(Date.UTC(t_b[0], t_b[1]-1, t_b[2], t_b[3], t_b[4], t_b[5]))	
				return date_b - date_a
			})
			return sorted_data
		})
		.then(data => {
			setPosts(data)
		})
		.catch(error => {
			console.log(error);
			alert(error)
		})
  }, [])

  const signIn = (event) => {
	event?.preventDefault();

	let formData = new FormData();
	formData.append('username', username)
	formData.append('password', password)

	const requestOptions = {
		method: 'POST',
		body: formData
	}

	fetch(BASE_URL + 'token', requestOptions)
		.then(response => {
			if (response.ok) {
				return response.json()
			}
			throw response
		})
		.then(data => {
			console.log(data);
			setAuthToken(data.access_token)
			setAuthTokenType(data.token_type)
			setUserId(data.user_id)
			setUserName(data.username)
			window.localStorage.setItem('authToken', data.access_token)
			window.localStorage.setItem('authTokenType', data.token_type)
			window.localStorage.setItem('userId', data.user_id)
			window.localStorage.setItem('username', data.username)
		})
		.catch(error => {
			console.log(error);
			alert(error);
		})
	
	setOpenSignIn(false);
  }

  const signOut = (event) => {
	setAuthToken(null)
	setAuthTokenType(null)
	setUserId('')
	setUserName('')
	window.localStorage.removeItem('authToken')
	window.localStorage.removeItem('authTokenType')
	window.localStorage.removeItem('userId')
	window.localStorage.removeItem('username')
  }

  const signUp = (event) => {
	event?.preventDefault();

	const req_body_json = JSON.stringify({
		username:  username,
		email: email,
		password: password
	})

	const requestOptions = {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: req_body_json
	}

	fetch(BASE_URL + 'users/', requestOptions)
		.then(response => {
			if (response.ok) {
				return response.json();
			}
			throw response
		})
		.then(data => {
			console.log(data);
			signIn();
		})
		.catch(error => {
			console.log(error);
			alert(error);
		})

	setOpenSignUp(false);
  }

  return (
	<div className='app'>

		<Modal open={openSignIn} onClose={() => setOpenSignIn(false)}>
			<div style={modalStyle} className={classes.paper}>
				<form className='app_signin_form'>
					<center>
						<img className='app_header_image' src='https://freepngimg.com/thumb/logo/69662-instagram-media-brand-social-logo-photography.png' alt='Instagram'></img>
					</center>
					<Input placeholder='username' type='text' value={username} 
						onChange={(e) => setUserName(e.target.value)} />
					<Input placeholder='password' type='password' value={password}
						onChange={(e) => setPassword(e.target.value)} />
					<Button type='submit' onClick={signIn}>Login</Button>
				</form>
			</div>
		</Modal>

		<Modal open={openSignUp} onClose={() => setOpenSignUp(false)}>
			<div style={modalStyle} className={classes.paper}>
				<form className='app_signin_form'>
					<center>
						<img className='app_header_image' src='https://freepngimg.com/thumb/logo/69662-instagram-media-brand-social-logo-photography.png' alt='Instagram'></img>
					</center>
					<Input placeholder='username' type='text' value={username} 
						onChange={(e) => setUserName(e.target.value)} />
					<Input placeholder='email' type='text' value={email} 
						onChange={(e) => setEmail(e.target.value)} />
					<Input placeholder='password' type='password' value={password}
						onChange={(e) => setPassword(e.target.value)} />
					<Button type='submit' onClick={signUp}>SignUp</Button>
				</form>
			</div>
		</Modal>

		<div className='app_header'>
			<img className='app_header_image' src='https://freepngimg.com/thumb/logo/69662-instagram-media-brand-social-logo-photography.png' alt='Instagram'></img>
			
			{authToken ? (
				<Button onClick={() => signOut()}>LogOut</Button>
			) : (
				<div>
					<Button onClick={() => setOpenSignIn(true)}>Login</Button>
					<Button onClick={() => setOpenSignUp(true)}>SignUp</Button>
				</div>
			)}
		</div>

		<div className='app_posts'>
			{
				posts.map(post => (
					<Posts post={post} authToken={authToken} authTokenType={authTokenType}/>
				))
			}
		</div>

		{
			authToken ? (
				<NewPost authToken={authToken} authTokenType={authTokenType} />
			) : (
				<h3>LogIn or SignUp to create a new Post or Comment!</h3>
			)
		}
	</div>
  );
}

export default App;
