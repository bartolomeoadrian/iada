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

	const [chatID, setChatID] = useState<string | null>(null);
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

		axios.get(`${props.url}?message=${message}&chat_id=${chatID}`, {
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
		}).then(response => {
			const data = response.data
			try {
				const parsedData = typeof data === "string" ? JSON.parse(data) : data
				const temporalMessage = newMessages.find(msg => msg.id === id)
				if (temporalMessage) {
					temporalMessage.type = parsedData.type;
					temporalMessage.data = parsedData.response;
					setMessages([...newMessages])
				}
			} catch (e) {
				console.log("Error parsing JSON", e)
			}
		}).finally(() => {
			setLocked(false);
			setLastMessage(lastMessage);
		});
	}

	const drawTable = (message: Message) => {
		if (!Array.isArray(message.data) || message.data.length <= 0) return <>There´s no results for this query</>;

		const first = message.data[0];
		const headers = Object.keys(first);

		return <div className='table_wrapper'>
			<table>
				<thead>
					<tr>
						{headers.map((header, i) => <th key={i}>{header}</th>)}
					</tr>
				</thead>
				<tbody>
					{message.data.map((row, i) => {
						return (
							<tr key={i}>
								{headers.map((header, j) => {
									return (
										<td key={j}>{row[header]}</td>
									)
								})}
							</tr>
						)
					})}
				</tbody>
			</table>
		</div>
	}

	useEffect(() => {
		if (lastMessage) {
			// Expresión regular mejorada para capturar URLs desde texto en formato Markdown
			const urlRegex = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/gi;
			const urls = [];
			let match;
			while ((match = urlRegex.exec(lastMessage)) !== null) {
				urls.push(match[2]); // Captura solo la URL
			}

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

				console.log("redirecting to", redirectUrl)

				setTimeout(() => {
					window?.top?.postMessage(JSON.stringify({
						type: "redirect",
						url: redirectUrl
					}), "*");
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

	useEffect(() => {
		// Recuperar chatID desde session storage al cargar el componente
		const storedChatID = sessionStorage.getItem('chat_id_nagivation');
		if (storedChatID) {
			setChatID(storedChatID);
		} else {
			const newChatID = ulid()
			setChatID(newChatID);
			sessionStorage.setItem('chat_id_nagivation', newChatID);
		}
	}, []);


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
												{msg.type === "table" ? drawTable(msg) : msg.text}
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
