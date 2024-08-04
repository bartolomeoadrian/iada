import './index.css'
import "react-chat-elements/dist/main.css"

import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Proyects from './pages/proyects/Proyects'
import Navigator from './pages/navigator/Navigator'

const router = createBrowserRouter([
	{
		path: "/",
		element: <></>,
	},
	{
		path: "/proyects",
		element: <Proyects />,
	},
	{
		path: "/navigator",
		element: <Navigator />,
	},
], {
	basename: "/chat",
});

ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
)
