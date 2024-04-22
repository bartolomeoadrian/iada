import { useState } from 'react'
import './Chat.css'

function Chat() {
	const [message, setMessage] = useState("");
	const [response, setResponse] = useState("");

	const send = () => {
		fetch(`/api/chat?message=${message}`, {
			method: 'GET',
		}).then(res => res.json()).then(data => {
			setResponse(JSON.stringify(data.response))
		}).catch(err => {
			console.error(err)
		});
	}

	return (
		<>
			<div className='chat_wrapper'>
				<div className="body">
					{response}
				</div>
				<div className="footer">
					<input type="text" onInput={e => {
						setMessage(e.currentTarget.value)
					}} />
					<button onClick={send}>Send</button>
				</div>
			</div>
		</>
	)
}

export default Chat
