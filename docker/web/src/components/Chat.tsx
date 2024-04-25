import { ChangeEvent, useEffect, useRef, useState } from 'react'
import { MessageBox } from 'react-chat-elements';
import './Chat.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';

type Message = {
	title: string,
	position: string,
	type: "text" | "file" | "system" | "table",
	text?: string,
	data?: unknown,
	date: Date,
}

type SystemMessage = {
	response: string,
	type: "text" | "table",
}

function Chat() {
	const box = useRef<HTMLDivElement>(null);

	const [message, setMessage] = useState("");
	const [ready, setReady] = useState(false);
	const [messages, setMessages] = useState<Array<Message>>([]);

	const chat = () => {
		if (!message) return;

		setMessages([...messages, {
			title: 'You',
			position: 'right',
			type: 'text',
			text: message,
			date: new Date(),
		}])

		setReady(true)
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
		if (!ready) return;

		setReady(false);

		const drawSystemMessage = (message: SystemMessage) => {
			if (message.type === "table") {
				setMessages([...messages, {
					title: 'Bot',
					position: 'left',
					type: 'table',
					data: message.response,
					date: new Date(),
				}])
			} else {
				setMessages([...messages, {
					title: 'Bot',
					position: 'left',
					type: 'text',
					text: JSON.stringify(message.response),
					date: new Date(),
				}])
			}
		}

		const send = () => {
			setMessage("")

			fetch(`/api/chat?message=${message}`, {
				method: 'GET',
			}).then(res => res.json()).then(data => {
				drawSystemMessage(data);
			}).catch(err => {
				console.error(err)
			});
		}

		send()
	}, [ready, message, messages])

	useEffect(() => {
		if (box.current) {
			//box.current.scrollIntoView({ behavior: "smooth" });
			//Debería ser antes del ultimo mensaje recibido
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
							onChange={(e: ChangeEvent<HTMLInputElement>) => {
								setMessage(e.currentTarget.value)
							}}
							onKeyDown={(e) => {
								if (e.key === "Enter") {
									chat()
								}
							}}
						/>
						<button onClick={chat} title="Send" >
							<FontAwesomeIcon icon={faPaperPlane} color='#FFF' />
						</button>
					</div>
				</div>
			</div>
		</>
	)
}

export default Chat
