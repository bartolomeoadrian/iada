import './Navigator.css'
import Chat from '../../components/Chat'

function Navigator() {
	return (
		<div style={{
			width: "100dvw",
			height: "100dvh",
		}}>
			<Chat url='/api/chat/navigator' />
		</div>
	)
}

export default Navigator
