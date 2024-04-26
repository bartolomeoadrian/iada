import { ChangeEvent, useEffect, useRef, useState } from 'react'
import { MessageBox } from 'react-chat-elements';
import './Chat.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';
import axios from 'axios';
import { faLock } from '@fortawesome/free-solid-svg-icons';

type Message = {
	id?: string,
	title: string,
	position: string,
	type: "text" | "file" | "system" | "table",
	text?: string,
	data?: unknown,
	date: Date,
}

function Chat() {
	const box = useRef<HTMLDivElement>(null);
	const input = useRef<HTMLInputElement>(null);

	const [message, setMessage] = useState("");
	const [locked, setLocked] = useState(false);
	const [messages, setMessages] = useState<Array<Message>>([]);

	const chat = () => {
		if (!message) return;
		if (locked) return;

		const newMessages: Array<Message> = [...messages, {
			title: 'You',
			position: 'right',
			type: 'text',
			text: message,
			date: new Date(),
		}];

		setMessages(newMessages)

		setMessage("");

		send(message, newMessages);
	}


	const send = (message: string, messages: Array<Message>) => {
		setLocked(true);

		const id = Math.random().toString(36).substring(7);

		const newMessages: Array<Message> = [...messages, {
			id: id,
			title: 'Bot',
			position: 'left',
			type: 'text',
			text: "",
			date: new Date(),
		}];

		setMessages(newMessages)

		axios.get(`/api/chat?message=${message}`, {
			responseType: 'stream',
			onDownloadProgress: progressEvent => {
				const xhr = progressEvent.event.target
				const { responseText } = xhr
				const temporalMessage = newMessages.find(msg => msg.id === id)
				if (temporalMessage) {
					temporalMessage.text = responseText
					setMessages([...newMessages])
				}
			}
		}).then(response => {
			const data = response.data
			try {
				const parsedData = JSON.parse(data)
				const temporalMessage = newMessages.find(msg => msg.id === id)
				if (temporalMessage) {
					temporalMessage.type = parsedData.type;
					temporalMessage.data = parsedData.response;
					setMessages([...newMessages])
				}
			} catch (e) {
				//NO ES JSON
			}
		}).finally(() => {
			setLocked(false);
		});
	}

	const drawTable = (message: Message) => {
		if (!Array.isArray(message.data)) return <></>;

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
		if (box.current) {
			box.current.scrollIntoView({ behavior: "smooth" });
			//Debería ser antes del ultimo mensaje recibido
			if (input.current) {
				input.current.focus();
			}
		}
	}, [messages])

	return (
		<>
			<div className='chat_wrapper'>
				<div className="body">
					<div className="messages">
						{messages ? messages.map((msg, i) => {
							return (
								<div key={i} className="message">
									{msg.type === "text" &&
										<MessageBox
											position={msg.position}
											type={msg.type}
											title={msg.title}
											text={msg.text || ""}
											date={msg.date}
											id={i}
											focus={false}
											titleColor={'#000000'}
											forwarded={false}
											replyButton={false}
											removeButton={false}
											status='sent'
											notch={false}
											retracted={false}
										/>
									}
									{msg.type === "table" &&
										drawTable(msg)
									}
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
