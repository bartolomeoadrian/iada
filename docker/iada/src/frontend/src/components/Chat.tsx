import './Chat.css'

import axios from 'axios';
import Markdown from 'react-markdown';
import { ChangeEvent, useEffect, useRef, useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import { ulid } from 'ulid';


type Message = {
	id?: string,
	title: string,
	position: string,
	type: "text" | "file" | "system" | "table",
	text?: string | JSX.Element,
	data?: unknown,
	date: Date,
}

function Chat(props: { url: string }) {
	const box = useRef<HTMLDivElement>(null);
	const messagesWrapper = useRef<HTMLDivElement>(null);
	const input = useRef<HTMLInputElement>(null);

	const [message, setMessage] = useState("");
	const [lastMessage, setLastMessage] = useState("");
	const [locked, setLocked] = useState(false);
	const [messages, setMessages] = useState<Array<Message>>([]);

	const chat = () => {
		if (!message) return;
		if (locked) return;

		const newMessages: Array<Message> = [...messages, {
			title: 'Usted',
			position: 'right',
			type: 'text',
			text: message,
			date: new Date(),
		}];

		setMessages(newMessages)

		setMessage("");

		send(message, newMessages);
	}


	const send = async (message: string, messages: Array<Message>) => {
		setLocked(true);

		const id = Math.random().toString(36).substring(7);

		const newMessages: Array<Message> = [...messages, {
			id: id,
			title: 'HCDN',
			position: 'left',
			type: 'text',
			text: "",
			date: new Date(),
		}];

		setMessages(newMessages)
		let lastMessage = ""

		axios.get(`${props.url}?message=${message}&chat_id=${ulid()}`, {
			onDownloadProgress: progressEvent => {
				const xhr = progressEvent.event.target
				const { responseText } = xhr
				const temporalMessage = newMessages.find(msg => msg.id === id)
				if (temporalMessage) {
					temporalMessage.text = <Markdown>{responseText}</Markdown>
					setMessages([...newMessages])
					lastMessage = responseText
				}
			}
		}).finally(() => {
			setLocked(false);
			setLastMessage(lastMessage);
		});
	}

	useEffect(() => {
		if (lastMessage) {
			const urlRegex = /(https?:\/\/[^\s]+)/g;
			const urls = lastMessage.match(urlRegex);
			console.log("urls", urls, lastMessage)

			if (urls && urls.length > 0) {
				const redirectUrl = urls[0];

				const newMessages: Array<Message> = [...messages, {
					id: Math.random().toString(36).substring(7),
					title: 'NYVA',
					position: 'left',
					type: 'text',
					text: "Redirecting you in 5 seconds...",
					date: new Date(),
				}];

				setMessages(newMessages)

				setTimeout(() => {
					window.location.href = redirectUrl;
				}, 5000);
			}
		}
	}, [lastMessage])

	useEffect(() => {
		if (box && box.current && messagesWrapper && messagesWrapper.current) {
			messagesWrapper.current.scrollTop = box.current.offsetTop;
		}

		if (input.current && messages.length > 0) {
			input.current.focus();
		}
	}, [messages])

	return (
		<>
			<div className='chat_wrapper'>
				<div className="body" ref={messagesWrapper}>
					<div className="messages">
						{messages ? messages.map((msg, i) => {
							return (
								<div key={i} className="message-wrapper">
									<div className={`message ${msg.position}`}>
										<div className="header">
											<p className="title">{msg.title}</p>
										</div>
										<div className="body">
											<div className="text">
												{msg.text}
											</div>
										</div>
										<div className="footer">
											<p className="date">{msg.date.toLocaleTimeString()}</p>
										</div>
									</div>
								</div>
							)
						}) : null}
						<div ref={box}></div>
					</div>
				</div>
				<div className="footer">
					<div className="input">
						<input
							placeholder="Escriba su mensaje aquí..."
							value={message}
							disabled={locked}
							onChange={(e: ChangeEvent<HTMLInputElement>) => {
								setMessage(e.currentTarget.value)
							}}
							onKeyDown={(e) => {
								if (e.key === "Enter") {
									chat()
								}
							}}
							ref={input}
						/>
						<button onClick={chat} title="Send" >
							{locked ? <FontAwesomeIcon icon={faLock} color='#FFF' /> : <FontAwesomeIcon icon={faPaperPlane} color='#FFF' />}
						</button>
					</div>
				</div>
			</div>
		</>
	)
}

export default Chat
