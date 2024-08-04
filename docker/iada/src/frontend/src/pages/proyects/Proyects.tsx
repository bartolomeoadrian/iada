import './Proyects.css'
import Chat from '../../components/Chat'

function Proyects() {
	return (
		<div style={{
			width: "100dvw",
			height: "100dvh",
		}}>
			<Chat url='/api/chat/proyects' />
		</div>
	)
}

export default Proyects
